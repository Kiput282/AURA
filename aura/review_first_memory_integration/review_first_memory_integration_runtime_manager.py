"""Sprint 265 review-first memory integration runtime.

This manager owns an in-process, non-durable candidate queue for explicit
browser review. It composes the existing deterministic extraction, privacy,
importance, review-queue, and permission-gate previews. It never constructs
or mutates MemoryStore.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from threading import RLock
from typing import Any, Callable
from uuid import uuid4
import re

from aura.memory_extraction_dry_run.aura_memory_extraction_dry_run_manager import (
    AuraMemoryExtractionDryRunManager,
)
from aura.memory_importance_pinning_policy.aura_memory_importance_pinning_policy_manager import (
    AuraMemoryImportancePinningPolicyManager,
)
from aura.memory_privacy_redaction_layer.aura_memory_privacy_redaction_layer_manager import (
    AuraMemoryPrivacyRedactionLayerManager,
)
from aura.memory_review_queue.aura_memory_review_queue_manager import (
    AuraMemoryReviewQueueManager,
)
from aura.memory_write_permission_gate.aura_memory_write_permission_gate_manager import (
    AuraMemoryWritePermissionGateManager,
)


class ReviewFirstMemoryIntegrationError(RuntimeError):
    """Base Sprint 265 memory review runtime error."""


class ReviewFirstMemoryValidationError(
    ReviewFirstMemoryIntegrationError
):
    """Invalid review request or candidate field."""


class ReviewFirstMemoryNotFoundError(
    ReviewFirstMemoryIntegrationError
):
    """Transient candidate was not found."""


class ReviewFirstMemoryConflictError(
    ReviewFirstMemoryIntegrationError
):
    """Candidate state or revision conflicts with the request."""


class ReviewFirstMemoryIntegrationRuntimeManager:
    """Manage explicit transient memory candidates without durable writes."""

    name = "review_first_memory_integration_runtime"
    component_version = "0.1.0-alpha"
    schema_version = "1.0"
    sprint = 265

    MAX_CANDIDATES = 32
    MAX_CONTENT_CHARS = 4000
    MAX_CONTENT_BYTES = 12000

    CATEGORIES = frozenset(
        {
            "note",
            "preference",
            "project_fact",
            "instruction",
            "milestone",
            "relationship",
            "other",
        }
    )
    IMPORTANCE_BANDS = frozenset(
        {
            "ephemeral",
            "normal",
            "important",
            "critical_review",
        }
    )
    REVIEW_STATES = frozenset(
        {
            "pending_review",
            "privacy_hold",
            "approved_write_preview",
        }
    )

    _CANDIDATE_ID_RE = re.compile(
        r"^memory_candidate_[0-9a-f]{24}$"
    )
    _SESSION_ID_RE = re.compile(
        r"^chat_[0-9a-f]{32}$"
    )
    _MESSAGE_ID_RE = re.compile(
        r"^message_[0-9a-f]{32}$"
    )

    _REDACTION_PATTERNS = (
        (
            "private_key",
            re.compile(
                r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
                re.IGNORECASE,
            ),
            "[REDACTED_PRIVATE_KEY]",
        ),
        (
            "bearer_token",
            re.compile(
                r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}",
                re.IGNORECASE,
            ),
            "[REDACTED_BEARER_TOKEN]",
        ),
        (
            "credential_assignment",
            re.compile(
                r"\b(?:password|passwd|secret|api[_-]?key|token)"
                r"\s*[:=]\s*[^\s,;]{4,}",
                re.IGNORECASE,
            ),
            "[REDACTED_CREDENTIAL]",
        ),
        (
            "email",
            re.compile(
                r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
                re.IGNORECASE,
            ),
            "[REDACTED_EMAIL]",
        ),
        (
            "ipv4",
            re.compile(
                r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
            ),
            "[REDACTED_IPV4]",
        ),
        (
            "phone",
            re.compile(
                r"(?<!\w)(?:\+?\d[\d .()-]{7,}\d)(?!\w)"
            ),
            "[REDACTED_PHONE]",
        ),
        (
            "payment_card_like",
            re.compile(
                r"\b(?:\d[ -]*?){13,19}\b"
            ),
            "[REDACTED_PAYMENT_CARD]",
        ),
    )

    def __init__(
        self,
        *,
        project_root: str | Path | None = None,
        now_factory: Callable[[], datetime] | None = None,
        id_factory: Callable[[], str] | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()
        self._now_factory = (
            now_factory
            or (lambda: datetime.now(timezone.utc))
        )
        self._id_factory = id_factory or (
            lambda: uuid4().hex[:24]
        )
        self._lock = RLock()
        self._candidates: dict[str, dict[str, Any]] = {}

        self.extraction_manager = (
            AuraMemoryExtractionDryRunManager(
                project_root=self.project_root
            )
        )
        self.privacy_manager = (
            AuraMemoryPrivacyRedactionLayerManager(
                project_root=self.project_root
            )
        )
        self.importance_manager = (
            AuraMemoryImportancePinningPolicyManager(
                project_root=self.project_root
            )
        )
        self.review_queue_manager = (
            AuraMemoryReviewQueueManager(
                project_root=self.project_root
            )
        )
        self.permission_manager = (
            AuraMemoryWritePermissionGateManager(
                project_root=self.project_root
            )
        )

    def _now(self) -> str:
        value = self._now_factory()
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(
            timezone.utc
        ).isoformat()

    @staticmethod
    def _normalize(value: Any) -> str:
        return " ".join(str(value or "").strip().split())

    def _validate_content(self, value: Any) -> str:
        normalized = self._normalize(value)
        if not normalized:
            raise ReviewFirstMemoryValidationError(
                "Memory candidate content is empty."
            )
        if len(normalized) > self.MAX_CONTENT_CHARS:
            raise ReviewFirstMemoryValidationError(
                "Memory candidate content exceeds the character limit."
            )
        if (
            len(normalized.encode("utf-8"))
            > self.MAX_CONTENT_BYTES
        ):
            raise ReviewFirstMemoryValidationError(
                "Memory candidate content exceeds the byte limit."
            )
        if any(
            ord(character) < 32
            and character not in {"\t", "\n", "\r"}
            for character in normalized
        ):
            raise ReviewFirstMemoryValidationError(
                "Memory candidate contains unsupported control characters."
            )
        return normalized

    @classmethod
    def _validate_candidate_id(cls, value: Any) -> str:
        candidate_id = str(value or "")
        if not cls._CANDIDATE_ID_RE.fullmatch(
            candidate_id
        ):
            raise ReviewFirstMemoryValidationError(
                "Memory candidate id is invalid."
            )
        return candidate_id

    @classmethod
    def _validate_session_id(cls, value: Any) -> str:
        session_id = str(value or "")
        if not cls._SESSION_ID_RE.fullmatch(session_id):
            raise ReviewFirstMemoryValidationError(
                "Source session id is invalid."
            )
        return session_id

    @classmethod
    def _validate_message_id(cls, value: Any) -> str:
        message_id = str(value or "")
        if not cls._MESSAGE_ID_RE.fullmatch(message_id):
            raise ReviewFirstMemoryValidationError(
                "Source message id is invalid."
            )
        return message_id

    @staticmethod
    def _validate_sequence(value: Any) -> int:
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value < 1
        ):
            raise ReviewFirstMemoryValidationError(
                "Source message sequence is invalid."
            )
        return value

    @staticmethod
    def _validate_revision(value: Any) -> int:
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value < 1
        ):
            raise ReviewFirstMemoryValidationError(
                "Candidate revision is invalid."
            )
        return value

    @classmethod
    def _validate_category(cls, value: Any) -> str:
        category = cls._normalize(value or "note").lower()
        if category not in cls.CATEGORIES:
            raise ReviewFirstMemoryValidationError(
                "Memory candidate category is unsupported."
            )
        return category

    @classmethod
    def _validate_importance(cls, value: Any) -> str:
        importance = cls._normalize(
            value or "normal"
        ).lower()
        if importance not in cls.IMPORTANCE_BANDS:
            raise ReviewFirstMemoryValidationError(
                "Memory candidate importance is unsupported."
            )
        return importance

    @staticmethod
    def _validate_pinned(value: Any) -> bool:
        if not isinstance(value, bool):
            raise ReviewFirstMemoryValidationError(
                "Memory candidate pinned must be boolean."
            )
        return value

    @staticmethod
    def _fingerprint(
        *,
        content: str,
        category: str,
        importance: str,
        pinned: bool,
        source_session_id: str,
        source_message_id: str,
        source_sequence: int,
    ) -> str:
        body = "|".join(
            (
                content,
                category,
                importance,
                "pinned" if pinned else "not_pinned",
                source_session_id,
                source_message_id,
                str(source_sequence),
            )
        ).encode("utf-8")
        return sha256(body).hexdigest()

    @classmethod
    def _redact(
        cls,
        content: str,
    ) -> tuple[str, list[str]]:
        redacted = content
        notes: list[str] = []
        for name, pattern, replacement in (
            cls._REDACTION_PATTERNS
        ):
            redacted, count = pattern.subn(
                replacement,
                redacted,
            )
            if count:
                notes.append(f"{name}:{count}")
        return redacted, notes

    @staticmethod
    def _call_first(
        manager: Any,
        names: tuple[str, ...],
        content: str,
    ) -> dict[str, Any]:
        for name in names:
            method = getattr(manager, name, None)
            if callable(method):
                result = method(content)
                if not isinstance(result, dict):
                    raise ReviewFirstMemoryIntegrationError(
                        f"Legacy contract {name} did not return an object."
                    )
                return result
        for name in sorted(dir(manager)):
            if not name.startswith("run_"):
                continue
            method = getattr(manager, name, None)
            if not callable(method):
                continue
            result = method(content)
            if isinstance(result, dict):
                return result
        raise ReviewFirstMemoryIntegrationError(
            "Compatible legacy memory preview method was not found."
        )

    def _legacy_snapshots(
        self,
        content: str,
    ) -> dict[str, dict[str, Any]]:
        return {
            "extraction": self.extraction_manager
            .run_extraction_dry_run(content),
            "privacy": self._call_first(
                self.privacy_manager,
                (
                    "run_privacy_preview",
                    "run_privacy_redaction_preview",
                    "run_redaction_preview",
                    "run_privacy_redaction_alpha",
                ),
                content,
            ),
            "importance": self.importance_manager
            .run_policy_preview(content),
            "review_queue": self.review_queue_manager
            .run_queue_preview(content),
        }

    def _public_candidate(
        self,
        candidate: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            key: deepcopy(value)
            for key, value in candidate.items()
            if not key.startswith("_")
        }

    def _candidate_unlocked(
        self,
        candidate_id: str,
    ) -> dict[str, Any]:
        validated = self._validate_candidate_id(
            candidate_id
        )
        candidate = self._candidates.get(validated)
        if candidate is None:
            raise ReviewFirstMemoryNotFoundError(
                f"Memory candidate not found: {validated}"
            )
        return candidate

    def _evaluate(
        self,
        *,
        content: str,
        category: str,
        importance: str,
        pinned: bool,
        source_session_id: str,
        source_message_id: str,
        source_sequence: int,
    ) -> dict[str, Any]:
        redacted, redaction_notes = self._redact(content)
        snapshots = self._legacy_snapshots(content)
        privacy_hold = bool(redaction_notes)

        return {
            "content": redacted,
            "content_redacted": privacy_hold,
            "category": category,
            "importance": importance,
            "pinned": pinned,
            "redaction_applied": privacy_hold,
            "redaction_notes": redaction_notes,
            "privacy_state": (
                "privacy_hold"
                if privacy_hold
                else "clear_for_manual_review"
            ),
            "review_state": (
                "privacy_hold"
                if privacy_hold
                else "pending_review"
            ),
            "candidate_fingerprint": self._fingerprint(
                content=content,
                category=category,
                importance=importance,
                pinned=pinned,
                source_session_id=source_session_id,
                source_message_id=source_message_id,
                source_sequence=source_sequence,
            ),
            "_legacy_preview_snapshots": snapshots,
            "legacy_preview_summary": {
                "extraction_contract_applied": True,
                "privacy_contract_applied": True,
                "importance_contract_applied": True,
                "review_queue_contract_applied": True,
                "snapshot_persisted": False,
            },
        }

    def status(self) -> dict[str, Any]:
        with self._lock:
            candidates = [
                self._public_candidate(candidate)
                for candidate in self._candidates.values()
            ]

        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "status": "ok",
            "candidate_count": len(candidates),
            "pending_review_count": sum(
                1
                for item in candidates
                if item["review_state"]
                == "pending_review"
            ),
            "privacy_hold_count": sum(
                1
                for item in candidates
                if item["review_state"]
                == "privacy_hold"
            ),
            "approved_write_preview_count": sum(
                1
                for item in candidates
                if item["review_state"]
                == "approved_write_preview"
            ),
            "candidates": candidates,
            "queue_kind": (
                "dedicated_browser_chat_in_process_queue"
            ),
            "candidate_persistence": False,
            "review_queue_persistence": False,
            "durable_memory_write": False,
            "memory_store_constructed": False,
            "memory_store_mutated": False,
            "permission_grant_applied": False,
            "automatic_memory_write": False,
            "automatic_memory_merge": False,
            "automatic_memory_delete": False,
            "cross_session_memory_import": False,
            "model_invocation": False,
            "network_connection_opened": False,
            "runtime_mutated": False,
            "safe_idle": True,
        }

    def list_candidates(self) -> dict[str, Any]:
        status = self.status()
        return {
            **status,
            "read_only_listing": True,
        }

    def create_candidate(
        self,
        *,
        content: Any,
        source_session_id: Any,
        source_message_id: Any,
        source_sequence: Any,
        category: Any = "note",
        importance: Any = "normal",
        pinned: Any = False,
    ) -> dict[str, Any]:
        normalized = self._validate_content(content)
        session_id = self._validate_session_id(
            source_session_id
        )
        message_id = self._validate_message_id(
            source_message_id
        )
        sequence = self._validate_sequence(
            source_sequence
        )
        validated_category = self._validate_category(
            category
        )
        validated_importance = self._validate_importance(
            importance
        )
        validated_pinned = self._validate_pinned(
            pinned
        )

        with self._lock:
            if len(self._candidates) >= self.MAX_CANDIDATES:
                raise ReviewFirstMemoryConflictError(
                    "Transient memory candidate queue is full."
                )

            candidate_id = (
                "memory_candidate_"
                + str(self._id_factory())
            )
            self._validate_candidate_id(candidate_id)
            if candidate_id in self._candidates:
                raise ReviewFirstMemoryConflictError(
                    "Generated memory candidate id already exists."
                )

            timestamp = self._now()
            evaluation = self._evaluate(
                content=normalized,
                category=validated_category,
                importance=validated_importance,
                pinned=validated_pinned,
                source_session_id=session_id,
                source_message_id=message_id,
                source_sequence=sequence,
            )
            candidate = {
                "schema_version": self.schema_version,
                "candidate_id": candidate_id,
                "source_session_id": session_id,
                "source_message_id": message_id,
                "source_sequence": sequence,
                "revision": 1,
                "created_at_utc": timestamp,
                "updated_at_utc": timestamp,
                "permission_scope": (
                    "memory.write.single_candidate"
                ),
                "manual_review_required": True,
                "privacy_review_required": True,
                "write_preview": None,
                "candidate_persisted": False,
                "review_queue_item_persisted": False,
                "durable_memory_written": False,
                "memory_store_mutated": False,
                "model_invoked": False,
                "network_connection_opened": False,
                "_content": normalized,
                **evaluation,
            }
            self._candidates[candidate_id] = candidate
            public = self._public_candidate(candidate)

        return {
            "status": "candidate_created",
            "candidate": public,
            "candidate_persisted": False,
            "review_queue_item_persisted": False,
            "durable_memory_written": False,
            "memory_store_mutated": False,
            "safe_idle": True,
        }

    def edit_candidate(
        self,
        candidate_id: Any,
        *,
        content: Any,
        category: Any,
        importance: Any,
        pinned: Any,
        expected_revision: Any,
    ) -> dict[str, Any]:
        validated_id = self._validate_candidate_id(
            candidate_id
        )
        normalized = self._validate_content(content)
        validated_category = self._validate_category(
            category
        )
        validated_importance = self._validate_importance(
            importance
        )
        validated_pinned = self._validate_pinned(
            pinned
        )
        revision = self._validate_revision(
            expected_revision
        )

        with self._lock:
            candidate = self._candidate_unlocked(
                validated_id
            )
            if candidate["revision"] != revision:
                raise ReviewFirstMemoryConflictError(
                    "Memory candidate revision changed before edit."
                )

            evaluation = self._evaluate(
                content=normalized,
                category=validated_category,
                importance=validated_importance,
                pinned=validated_pinned,
                source_session_id=candidate[
                    "source_session_id"
                ],
                source_message_id=candidate[
                    "source_message_id"
                ],
                source_sequence=candidate[
                    "source_sequence"
                ],
            )
            candidate.update(evaluation)
            candidate["_content"] = normalized
            candidate["write_preview"] = None
            candidate["revision"] += 1
            candidate["updated_at_utc"] = self._now()
            public = self._public_candidate(candidate)

        return {
            "status": "candidate_edited",
            "candidate": public,
            "approval_preview_invalidated": True,
            "candidate_persisted": False,
            "durable_memory_written": False,
            "memory_store_mutated": False,
            "safe_idle": True,
        }

    def approve_write_preview(
        self,
        candidate_id: Any,
        *,
        expected_revision: Any,
    ) -> dict[str, Any]:
        validated_id = self._validate_candidate_id(
            candidate_id
        )
        revision = self._validate_revision(
            expected_revision
        )

        with self._lock:
            candidate = self._candidate_unlocked(
                validated_id
            )
            if candidate["revision"] != revision:
                raise ReviewFirstMemoryConflictError(
                    "Memory candidate revision changed before approval preview."
                )
            if candidate["review_state"] == "privacy_hold":
                raise ReviewFirstMemoryConflictError(
                    "Memory candidate is on privacy hold; edit and re-review it first."
                )

            permission = self.permission_manager \
                .run_permission_gate_alpha(
                    candidate["_content"]
                )
            candidate["review_state"] = (
                "approved_write_preview"
            )
            candidate["write_preview"] = {
                "decision": (
                    "approved_for_future_permission_flow"
                ),
                "permission_scope": (
                    "memory.write.single_candidate"
                ),
                "candidate_fingerprint": candidate[
                    "candidate_fingerprint"
                ],
                "permission_envelope_preview": permission,
                "write_authorized": False,
                "permission_grant_applied": False,
                "durable_memory_written": False,
                "memory_store_mutated": False,
            }
            candidate["revision"] += 1
            candidate["updated_at_utc"] = self._now()
            public = self._public_candidate(candidate)

        return {
            "status": "write_preview_approved",
            "candidate": public,
            "permission_envelope_preview": deepcopy(
                permission
            ),
            "write_authorized": False,
            "permission_grant_applied": False,
            "durable_memory_written": False,
            "memory_store_mutated": False,
            "candidate_persisted": False,
            "review_queue_item_persisted": False,
            "safe_idle": True,
        }

    def reject_candidate(
        self,
        candidate_id: Any,
        *,
        expected_revision: Any,
    ) -> dict[str, Any]:
        validated_id = self._validate_candidate_id(
            candidate_id
        )
        revision = self._validate_revision(
            expected_revision
        )

        with self._lock:
            candidate = self._candidate_unlocked(
                validated_id
            )
            if candidate["revision"] != revision:
                raise ReviewFirstMemoryConflictError(
                    "Memory candidate revision changed before rejection."
                )
            public = self._public_candidate(candidate)
            del self._candidates[validated_id]

        return {
            "status": "candidate_rejected",
            "candidate_id": validated_id,
            "source_session_id": public[
                "source_session_id"
            ],
            "source_message_id": public[
                "source_message_id"
            ],
            "transient_candidate_discarded": True,
            "durable_memory_deleted": False,
            "memory_store_mutated": False,
            "candidate_persisted": False,
            "safe_idle": True,
        }

    def safety_boundary(self) -> dict[str, Any]:
        return {
            "review_first_memory_integration": True,
            "explicit_candidate_creation": True,
            "single_user_message_source": True,
            "in_process_candidate_queue": True,
            "edit_before_approve": True,
            "reject_discards_transient_candidate": True,
            "permission_envelope_preview": True,
            "candidate_persistence": False,
            "review_queue_persistence": False,
            "review_decision_persistence": False,
            "permission_request_persistence": False,
            "permission_grant_apply": False,
            "durable_memory_write": False,
            "memory_store_constructed": False,
            "memory_store_mutation": False,
            "automatic_memory_write": False,
            "automatic_memory_merge": False,
            "automatic_memory_delete": False,
            "cross_session_memory_import": False,
            "model_invocation": False,
            "network_connection_opened": False,
            "audit_write_runtime": False,
            "tool_execution": False,
            "action_dispatch": False,
            "command_execution": False,
            "safe_idle": True,
        }

    def self_test(self) -> dict[str, Any]:
        assertions: dict[str, bool] = {}
        identifiers = iter(
            (
                "1" * 24,
                "2" * 24,
                "3" * 24,
            )
        )
        clock_tick = 0

        def clock() -> datetime:
            nonlocal clock_tick
            clock_tick += 1
            return datetime(
                2026,
                7,
                18,
                1,
                0,
                min(clock_tick, 59),
                tzinfo=timezone.utc,
            )

        manager = ReviewFirstMemoryIntegrationRuntimeManager(
            project_root=self.project_root,
            now_factory=clock,
            id_factory=lambda: next(identifiers),
        )

        initial = manager.status()
        assertions["initial_empty"] = (
            initial["candidate_count"] == 0
        )
        assertions["initial_no_store"] = (
            initial["memory_store_constructed"]
            is False
        )
        assertions["initial_no_write"] = (
            initial["durable_memory_write"]
            is False
        )

        created = manager.create_candidate(
            content="AURA should remember my project milestone.",
            source_session_id="chat_" + "a" * 32,
            source_message_id="message_" + "b" * 32,
            source_sequence=1,
            category="milestone",
            importance="important",
            pinned=False,
        )
        candidate = created["candidate"]
        candidate_id = candidate["candidate_id"]
        assertions["create_status"] = (
            created["status"]
            == "candidate_created"
        )
        assertions["create_revision_one"] = (
            candidate["revision"] == 1
        )
        assertions["create_pending"] = (
            candidate["review_state"]
            == "pending_review"
        )
        assertions["create_not_persisted"] = (
            created["candidate_persisted"]
            is False
        )
        assertions["create_no_store_mutation"] = (
            created["memory_store_mutated"]
            is False
        )

        edited = manager.edit_candidate(
            candidate_id,
            content=(
                "AURA should remember the project milestone "
                "for Sprint 265."
            ),
            category="project_fact",
            importance="important",
            pinned=True,
            expected_revision=1,
        )
        edited_candidate = edited["candidate"]
        assertions["edit_status"] = (
            edited["status"] == "candidate_edited"
        )
        assertions["edit_revision_two"] = (
            edited_candidate["revision"] == 2
        )
        assertions["edit_pinned_true"] = (
            edited_candidate["pinned"] is True
        )
        assertions["edit_preview_invalidated"] = (
            edited[
                "approval_preview_invalidated"
            ]
            is True
        )

        approved = manager.approve_write_preview(
            candidate_id,
            expected_revision=2,
        )
        approved_candidate = approved["candidate"]
        assertions["approve_status"] = (
            approved["status"]
            == "write_preview_approved"
        )
        assertions["approve_revision_three"] = (
            approved_candidate["revision"] == 3
        )
        assertions["approve_state"] = (
            approved_candidate["review_state"]
            == "approved_write_preview"
        )
        assertions["approve_write_false"] = (
            approved["durable_memory_written"]
            is False
        )
        assertions["approve_grant_false"] = (
            approved["permission_grant_applied"]
            is False
        )
        assertions["approve_store_false"] = (
            approved["memory_store_mutated"]
            is False
        )

        stale_seen = False
        try:
            manager.edit_candidate(
                candidate_id,
                content="stale",
                category="note",
                importance="normal",
                pinned=False,
                expected_revision=2,
            )
        except ReviewFirstMemoryConflictError:
            stale_seen = True
        assertions["stale_revision_blocked"] = (
            stale_seen
        )

        sensitive = manager.create_candidate(
            content="api_key=super-secret-value",
            source_session_id="chat_" + "c" * 32,
            source_message_id="message_" + "d" * 32,
            source_sequence=2,
        )
        sensitive_candidate = sensitive["candidate"]
        assertions["privacy_hold"] = (
            sensitive_candidate["review_state"]
            == "privacy_hold"
        )
        assertions["privacy_redacted"] = (
            "super-secret-value"
            not in sensitive_candidate["content"]
        )

        privacy_approval_blocked = False
        try:
            manager.approve_write_preview(
                sensitive_candidate["candidate_id"],
                expected_revision=1,
            )
        except ReviewFirstMemoryConflictError:
            privacy_approval_blocked = True
        assertions["privacy_approval_blocked"] = (
            privacy_approval_blocked
        )

        rejected = manager.reject_candidate(
            sensitive_candidate["candidate_id"],
            expected_revision=1,
        )
        assertions["reject_status"] = (
            rejected["status"]
            == "candidate_rejected"
        )
        assertions["reject_transient_only"] = (
            rejected[
                "transient_candidate_discarded"
            ]
            is True
            and rejected["durable_memory_deleted"]
            is False
        )
        assertions["queue_one_after_reject"] = (
            manager.status()["candidate_count"] == 1
        )

        not_found_seen = False
        try:
            manager.reject_candidate(
                sensitive_candidate["candidate_id"],
                expected_revision=1,
            )
        except ReviewFirstMemoryNotFoundError:
            not_found_seen = True
        assertions["not_found_visible"] = (
            not_found_seen
        )

        boundary = manager.safety_boundary()
        disabled = (
            "candidate_persistence",
            "review_queue_persistence",
            "review_decision_persistence",
            "permission_request_persistence",
            "permission_grant_apply",
            "durable_memory_write",
            "memory_store_constructed",
            "memory_store_mutation",
            "automatic_memory_write",
            "automatic_memory_merge",
            "automatic_memory_delete",
            "cross_session_memory_import",
            "model_invocation",
            "network_connection_opened",
            "audit_write_runtime",
            "tool_execution",
            "action_dispatch",
            "command_execution",
        )
        for key in disabled:
            assertions[
                "boundary_disabled_" + key
            ] = boundary[key] is False
        assertions["boundary_safe_idle"] = (
            boundary["safe_idle"] is True
        )

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise ReviewFirstMemoryIntegrationError(
                "Review-first memory runtime self-test failed: "
                + ", ".join(failed)
            )

        return {
            "status": "ok",
            "component": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "assertion_count": len(assertions),
            "failed_assertion_count": 0,
            "candidate_create_verified": True,
            "candidate_edit_verified": True,
            "privacy_hold_verified": True,
            "approval_preview_verified": True,
            "reject_transient_only_verified": True,
            "revision_conflict_verified": True,
            "candidate_persistence": False,
            "review_queue_persistence": False,
            "durable_memory_write": False,
            "memory_store_mutation": False,
            "model_invocation": False,
            "network_connection_opened": False,
            "safe_idle": True,
        }
