from __future__ import annotations

from collections.abc import Collection


def _semantic_version_tuple(
    version: str,
) -> tuple[int, int, int] | None:
    """Parse an AURA semantic version with an optional Genesis suffix."""
    normalized = version.strip()

    if normalized.startswith("v"):
        normalized = normalized[1:]

    if normalized.endswith("-genesis"):
        normalized = normalized[
            :-len("-genesis")
        ]

    parts = normalized.split(".")

    if (
        len(parts) != 3
        or any(
            not part.isdigit()
            for part in parts
        )
    ):
        return None

    return tuple(
        int(part)
        for part in parts
    )


def is_checkpoint_identity_compatible(
    version: object,
    *,
    historical_versions: Collection[str] = (),
) -> bool:
    """Accept explicit historical versions or canonical versions from v1 onward."""
    if not isinstance(version, str):
        return False

    if version in historical_versions:
        return True

    parsed = _semantic_version_tuple(
        version
    )

    return (
        parsed is not None
        and parsed >= (1, 0, 0)
    )
