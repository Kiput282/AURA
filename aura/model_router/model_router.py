from pathlib import Path
from typing import Any

import yaml

from aura.model_router.model_route import ModelRoute


class ModelRouter:
    """
    AURA Model Router Foundation.

    Current phase:
    - stores model route metadata
    - selects recommended provider/model for a target role or task
    - does not download, start, stop, or switch real model runtimes
    """

    name = "model_router"
    version = "0.1.0"

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.settings_path = project_root / "aura" / "config" / "settings.yaml"
        self.settings = self.load_settings()
        self.routes = self.build_routes()

    def load_settings(self) -> dict[str, Any]:
        if not self.settings_path.exists():
            return {}

        data = yaml.safe_load(self.settings_path.read_text(encoding="utf-8")) or {}
        return data if isinstance(data, dict) else {}

    def reasoning_settings(self) -> dict[str, Any]:
        reasoning = self.settings.get("reasoning", {})
        return reasoning if isinstance(reasoning, dict) else {}

    def current_provider(self) -> str:
        return self.reasoning_settings().get("provider", "unknown")

    def current_model(self) -> str:
        return self.reasoning_settings().get("model", "unknown")

    def current_host(self) -> str:
        return self.reasoning_settings().get("host", "unknown")

    def build_routes(self) -> list[ModelRoute]:
        current_provider = self.current_provider()
        current_model = self.current_model()

        return [
            ModelRoute(
                name="companion",
                role="companion",
                provider=current_provider,
                model=current_model,
                status="online",
                description="Main conversational route for AURA companion personality.",
                use_cases=["chat", "identity", "casual conversation", "project discussion"],
                candidate_models=["llama3.2", "mistral", "qwen2.5"],
                safety_notes=["Text-only reasoning route."],
            ),
            ModelRoute(
                name="coding",
                role="coder",
                provider=current_provider,
                model=current_model,
                status="foundation",
                description="Coding and software architecture route. Dedicated coding model is planned later.",
                use_cases=["coding", "debugging", "architecture", "code review", "project inspection"],
                candidate_models=["deepseek-coder", "qwen2.5-coder", "codellama", current_model],
                safety_notes=["Code writing and command execution still require tool sandbox and confirmation."],
            ),
            ModelRoute(
                name="project",
                role="project_manager",
                provider="internal",
                model="project_journal",
                status="foundation",
                description="Project progress, journal, roadmap, and planning route.",
                use_cases=["roadmap", "journal", "project summary", "planning"],
                candidate_models=["internal_project_journal", current_model],
                safety_notes=["Journal writing remains explicit through journal commands."],
            ),
            ModelRoute(
                name="memory",
                role="memory",
                provider="internal",
                model="keyword_memory",
                status="online",
                description="Memory recall, pinned memory, important memory, and relevance route.",
                use_cases=["memory recall", "memory search", "context building"],
                candidate_models=["internal_keyword_memory"],
                safety_notes=["Memory modification uses permission checks."],
            ),
            ModelRoute(
                name="creative",
                role="creative",
                provider="planned",
                model="creative_model",
                status="planned",
                description="Creative writing, visual concepts, character ideas, image/asset concepts.",
                use_cases=["concept art", "story ideas", "texture concepts", "moodboards"],
                candidate_models=["sdxl", "flux", "llama3.2", "qwen2.5"],
                safety_notes=["Image generation and asset creation are future controlled runtimes."],
            ),
            ModelRoute(
                name="vision",
                role="vision",
                provider="planned",
                model="vision_model",
                status="foundation",
                description="Screen, camera, image, and environment understanding route.",
                use_cases=["screen analysis", "camera analysis", "image understanding", "OCR"],
                candidate_models=["llava", "moondream", "clip"],
                safety_notes=["Screen/camera access requires explicit permission."],
            ),
            ModelRoute(
                name="voice",
                role="voice",
                provider="planned",
                model="voice_runtime",
                status="foundation",
                description="Speech-to-text and text-to-speech routing.",
                use_cases=["voice commands", "speech recognition", "speech output"],
                candidate_models=["faster-whisper", "whisper.cpp", "vosk", "piper", "coqui-tts"],
                safety_notes=["Microphone and speaker access require explicit permission."],
            ),
            ModelRoute(
                name="avatar",
                role="avatar",
                provider="internal",
                model="avatar_manager",
                status="foundation",
                description="Avatar state, expression, gesture, and VRM/VRoid planning route.",
                use_cases=["avatar status", "expression proposal", "gesture proposal", "VRM planning"],
                candidate_models=["avatar_manager", "VRM runtime", "VSeeFace", "Unity", "Godot"],
                safety_notes=["Real avatar runtime is not connected yet."],
            ),
            ModelRoute(
                name="blender",
                role="creative",
                provider="planned",
                model="blender_bridge_model",
                status="planned",
                description="Future Blender bridge route for 3D modeling, retopology, UV, material, and texture workflows.",
                use_cases=["Blender automation", "3D modeling", "retopology", "UV texture", "material nodes"],
                candidate_models=["qwen2.5-coder", "deepseek-coder", "llama3.2", "vision_model"],
                safety_notes=["Blender scene modification must require confirmation and sandbox rules."],
            ),
            ModelRoute(
                name="media",
                role="vision",
                provider="planned",
                model="media_understanding_model",
                status="planned",
                description="Future media understanding route for video, subtitles, OCR, translation, and summaries.",
                use_cases=["video analysis", "translation", "subtitle extraction", "title suggestions"],
                candidate_models=["whisper", "llava", "moondream", "translation_model"],
                safety_notes=["Media file access and transcription should respect local-first privacy rules."],
            ),
            ModelRoute(
                name="gaming",
                role="gaming",
                provider="planned",
                model="gaming_model",
                status="planned",
                description="Future game companion route for game awareness and sandboxed game assistance.",
                use_cases=["Minecraft companion", "inventory awareness", "resource gathering", "navigation"],
                candidate_models=["vision_model", "planning_model", current_model],
                safety_notes=["Game control requires sandboxing and explicit confirmation."],
            ),
            ModelRoute(
                name="streaming",
                role="streaming",
                provider="planned",
                model="streaming_model",
                status="planned",
                description="Future streaming route for viewer interaction, moderation, OBS, and AURA's 3D environment.",
                use_cases=["livestream chat", "viewer interaction", "OBS", "donation-gated commands"],
                candidate_models=["streaming_model", current_model, "moderation_model"],
                safety_notes=["Streaming requires profanity filters, forbidden phrase rules, and interaction history."],
            ),
        ]

    def alias_map(self) -> dict[str, str]:
        return {
            "chat": "companion",
            "companion": "companion",
            "conversation": "companion",
            "coding": "coding",
            "coder": "coding",
            "code": "coding",
            "programming": "coding",
            "project": "project",
            "roadmap": "project",
            "journal": "project",
            "memory": "memory",
            "creative": "creative",
            "idea": "creative",
            "image": "creative",
            "asset": "creative",
            "vision": "vision",
            "screen": "vision",
            "camera": "vision",
            "ocr": "vision",
            "voice": "voice",
            "speech": "voice",
            "audio": "voice",
            "avatar": "avatar",
            "vrm": "avatar",
            "expression": "avatar",
            "gesture": "avatar",
            "blender": "blender",
            "3d": "blender",
            "uv": "blender",
            "texture": "blender",
            "retopology": "blender",
            "media": "media",
            "video": "media",
            "translate": "media",
            "subtitle": "media",
            "game": "gaming",
            "gaming": "gaming",
            "minecraft": "gaming",
            "stream": "streaming",
            "streaming": "streaming",
            "obs": "streaming",
            "viewer": "streaming",
        }

    def normalize_target(self, target: str) -> str:
        normalized = target.strip().lower().replace("_", "-")
        normalized = normalized.replace("-", " ")
        first_token = normalized.split()[0] if normalized.split() else ""
        aliases = self.alias_map()

        if normalized in aliases:
            return aliases[normalized]

        if first_token in aliases:
            return aliases[first_token]

        return target.strip().lower()

    def list_routes(self) -> list[ModelRoute]:
        return self.routes

    def get_route(self, target: str) -> ModelRoute | None:
        normalized = self.normalize_target(target)

        for route in self.routes:
            if route.name == normalized:
                return route

        return None

    def status(self) -> dict[str, Any]:
        statuses = {}

        for route in self.routes:
            statuses[route.status] = statuses.get(route.status, 0) + 1

        return {
            "name": self.name,
            "version": self.version,
            "status": "foundation",
            "router_ready": True,
            "route_selection_ready": True,
            "runtime_switching_ready": False,
            "model_download_ready": False,
            "active_provider": self.current_provider(),
            "active_model": self.current_model(),
            "active_host": self.current_host(),
            "routes": len(self.routes),
            "route_status_counts": statuses,
            "note": "Model router foundation is online. It selects route metadata only and does not switch real model runtimes yet.",
        }

    def select(self, target: str) -> dict[str, Any]:
        normalized = self.normalize_target(target)
        route = self.get_route(target)

        if route is None:
            fallback = self.get_route("companion")
            return {
                "target": target,
                "normalized_target": normalized,
                "found": False,
                "fallback_used": True,
                "route": fallback.to_dict() if fallback else None,
                "runtime_switching_performed": False,
                "note": "No exact model route found. Falling back to companion route metadata.",
            }

        return {
            "target": target,
            "normalized_target": normalized,
            "found": True,
            "fallback_used": False,
            "route": route.to_dict(),
            "runtime_switching_performed": False,
            "note": "Model route selected as metadata only. No real runtime model switching was performed.",
        }
