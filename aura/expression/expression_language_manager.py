from pathlib import Path
from typing import Any

import yaml

from aura.avatar.avatar_manager import AvatarManager
from aura.avatar.avatar_runtime_alpha_manager import AvatarRuntimeAlphaManager
from aura.permissions.permission_manager import PermissionManager
from aura.voice.voice_runtime_alpha_manager import VoiceRuntimeAlphaManager


class ExpressionLanguageManager:
    """
    AURA Expression Language.

    Current phase:
    - define safe internal mood and emotion language
    - map text/intention into expression hints
    - prepare voice tone hints
    - prepare avatar expression hints
    - prepare gesture hints
    - prepare response style hints
    - never changes a real avatar automatically
    - never plays voice output automatically
    - never writes files automatically
    - never executes commands
    """

    name = "expression_language"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.permission_manager = PermissionManager()
        self.avatar_manager = AvatarManager(project_root=self.project_root)
        self.avatar_runtime_alpha = AvatarRuntimeAlphaManager(project_root=self.project_root)
        self.voice_runtime_alpha = VoiceRuntimeAlphaManager(project_root=self.project_root)

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}

        content = self.identity_path.read_text(encoding="utf-8", errors="replace")
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            return {}

        return data

    def mood_states(self) -> list[str]:
        return [
            "neutral",
            "warm",
            "focused",
            "curious",
            "playful",
            "encouraging",
            "calm",
            "serious",
            "celebrating",
            "concerned",
        ]

    def emotion_tags(self) -> list[str]:
        return [
            "friendly",
            "supportive",
            "focused",
            "curious",
            "playful",
            "confident",
            "calm",
            "careful",
            "excited",
            "empathetic",
            "honest",
            "professional",
        ]

    def voice_tones(self) -> list[str]:
        return [
            "neutral_clear",
            "warm_friendly",
            "focused_concise",
            "playful_light",
            "calm_supportive",
            "celebratory",
            "serious_professional",
        ]

    def avatar_expressions(self) -> list[str]:
        return self.avatar_manager.expression_options()

    def gesture_hints(self) -> list[str]:
        return self.avatar_manager.gesture_options()

    def response_styles(self) -> list[str]:
        return [
            "concise",
            "clear",
            "supportive",
            "technical",
            "creative",
            "streaming_friendly",
            "calm_step_by_step",
        ]

    def normalize_text(self, text: str) -> str:
        normalized = " ".join(text.strip().split())

        if len(normalized) > 500:
            return normalized[:500].rstrip() + "..."

        return normalized

    def infer_emotion_tags(self, text: str) -> list[str]:
        lowered = text.lower()
        tags: list[str] = []

        keyword_map = {
            "senang": "excited",
            "happy": "excited",
            "mantap": "excited",
            "selesai": "celebratory",
            "berhasil": "celebratory",
            "fokus": "focused",
            "coding": "focused",
            "serius": "professional",
            "tenang": "calm",
            "bingung": "empathetic",
            "error": "careful",
            "gagal": "careful",
            "stream": "streaming_friendly",
            "game": "playful",
            "avatar": "creative",
            "texture": "creative",
            "blender": "creative",
        }

        for keyword, tag in keyword_map.items():
            if keyword in lowered and tag not in tags:
                tags.append(tag)

        if not tags:
            tags.extend(["friendly", "supportive"])

        clean_tags: list[str] = []

        for tag in tags:
            if tag == "streaming_friendly":
                if "playful" not in clean_tags:
                    clean_tags.append("playful")
                continue

            if tag == "creative":
                if "curious" not in clean_tags:
                    clean_tags.append("curious")
                continue

            if tag not in clean_tags:
                clean_tags.append(tag)

        return clean_tags[:5]

    def infer_mood(self, tags: list[str]) -> str:
        if "celebratory" in tags or "excited" in tags:
            return "celebrating"

        if "focused" in tags or "professional" in tags:
            return "focused"

        if "careful" in tags or "empathetic" in tags:
            return "calm"

        if "playful" in tags:
            return "playful"

        if "curious" in tags:
            return "curious"

        return "warm"

    def choose_voice_tone(self, mood: str, tags: list[str]) -> str:
        if mood == "celebrating":
            return "celebratory"

        if mood == "focused":
            return "focused_concise"

        if mood == "playful":
            return "playful_light"

        if mood == "calm":
            return "calm_supportive"

        if "professional" in tags:
            return "serious_professional"

        return "warm_friendly"

    def choose_avatar_expression(self, mood: str, tags: list[str]) -> str:
        if mood == "celebrating":
            return "happy"

        if mood == "focused":
            return "focused"

        if mood == "playful":
            return "smile"

        if mood == "calm":
            return "neutral"

        if "curious" in tags:
            return "thinking"

        return "smile"

    def choose_gesture(self, mood: str, tags: list[str]) -> str:
        if mood == "celebrating":
            return "celebrate"

        if mood == "focused":
            return "thinking_pose"

        if mood == "playful":
            return "wave"

        if mood == "calm":
            return "idle"

        if "curious" in tags:
            return "present"

        return "nod"

    def choose_response_style(self, mood: str, tags: list[str]) -> str:
        if mood == "focused":
            return "technical"

        if mood == "celebrating":
            return "supportive"

        if mood == "playful":
            return "streaming_friendly"

        if mood == "calm":
            return "calm_step_by_step"

        if "curious" in tags:
            return "creative"

        return "clear"

    def expression_state(self) -> dict[str, Any]:
        identity = self.load_identity()
        avatar_state = self.avatar_manager.state()

        return {
            "status": self.status_name,
            "state_ready": True,
            "aura_name": identity.get("name", "AURA"),
            "aura_version": identity.get("version", "unknown"),
            "codename": identity.get("codename", "Genesis"),
            "creator": identity.get("creator", "Kiput"),
            "base_mood": "warm",
            "base_emotion_tags": ["friendly", "supportive", "curious", "honest"],
            "default_voice_tone": "warm_friendly",
            "default_avatar_expression": avatar_state["expression"],
            "default_gesture": avatar_state["gesture"],
            "supported_moods": self.mood_states(),
            "supported_emotion_tags": self.emotion_tags(),
            "supported_voice_tones": self.voice_tones(),
            "supported_avatar_expressions": self.avatar_expressions(),
            "supported_gestures": self.gesture_hints(),
            "supported_response_styles": self.response_styles(),
            "personality_traits": identity.get("personality", {}).get("traits", []),
            "modes": identity.get("modes", {}),
            "read_only": True,
            "write_performed": False,
            "avatar_changed": False,
            "voice_output_performed": False,
            "command_execution_performed": False,
            "note": "Expression state is an internal language map only. No avatar, voice, file, or command action was performed.",
        }

    def base_hint(self, hint_type: str, target: str, recommended_steps: list[str]) -> dict[str, Any]:
        cleaned_target = self.normalize_text(target) or "<unspecified>"
        prepare_permission = self.permission_manager.check("prepare_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        tags = self.infer_emotion_tags(cleaned_target)
        mood = self.infer_mood(tags)

        return {
            "status": "planned",
            "hint_type": hint_type,
            "target": cleaned_target,
            "hint_state": "proposal_ready",
            "emotion_tags": tags,
            "mood": mood,
            "voice_tone_hint": self.choose_voice_tone(mood=mood, tags=tags),
            "avatar_expression_hint": self.choose_avatar_expression(mood=mood, tags=tags),
            "gesture_hint": self.choose_gesture(mood=mood, tags=tags),
            "response_style_hint": self.choose_response_style(mood=mood, tags=tags),
            "recommended_steps": recommended_steps,
            "permissions": {
                "prepare_file": prepare_permission.to_dict(),
                "write_file": write_permission.to_dict(),
                "run_command": command_permission.to_dict(),
            },
            "execution_ready": False,
            "executed": False,
            "avatar_changed": False,
            "gesture_changed": False,
            "voice_output_performed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "safety_notes": [
                "Expression hint is proposal-only.",
                "No avatar expression was changed.",
                "No gesture was changed.",
                "No voice output was played.",
                "No file was written.",
                "No command was executed.",
                "Future real voice/avatar expression must go through explicit permission and confirmation.",
            ],
        }

    def voice_hint(self, target: str) -> dict[str, Any]:
        return self.base_hint(
            hint_type="voice_tone",
            target=target,
            recommended_steps=[
                "Choose a tone that matches AURA's current role and user context.",
                "Keep the voice concise, warm, and not excessive.",
                "Use a clearer tone for coding or technical steps.",
                "Use a more expressive tone for streaming and milestone moments.",
                "Do not play audio until explicit voice runtime approval exists.",
            ],
        )

    def avatar_hint(self, target: str) -> dict[str, Any]:
        return self.base_hint(
            hint_type="avatar_expression",
            target=target,
            recommended_steps=[
                "Choose a facial expression that matches the intended mood.",
                "Prefer subtle expression changes unless the moment is celebratory.",
                "Keep expression compatible with supported avatar expressions.",
                "Prepare avatar runtime alpha plan only; do not change the avatar.",
                "Do not render or write avatar media files automatically.",
            ],
        )

    def gesture_hint(self, target: str) -> dict[str, Any]:
        return self.base_hint(
            hint_type="gesture",
            target=target,
            recommended_steps=[
                "Choose a gesture that supports the response without distracting.",
                "Prefer small gestures for normal conversation.",
                "Use celebrate/wave only for milestones or streaming-friendly moments.",
                "Keep gesture compatible with supported avatar gestures.",
                "Do not execute or render gesture changes automatically.",
            ],
        )

    def expression_plan(self, text: str) -> dict[str, Any]:
        cleaned_text = self.normalize_text(text) or "<unspecified>"
        tags = self.infer_emotion_tags(cleaned_text)
        mood = self.infer_mood(tags)

        voice_tone = self.choose_voice_tone(mood=mood, tags=tags)
        avatar_expression = self.choose_avatar_expression(mood=mood, tags=tags)
        gesture = self.choose_gesture(mood=mood, tags=tags)
        response_style = self.choose_response_style(mood=mood, tags=tags)

        avatar_plan = self.avatar_runtime_alpha.expression_plan(avatar_expression)
        gesture_plan = self.avatar_runtime_alpha.gesture_plan(gesture)

        return {
            "status": "planned",
            "plan_type": "expression_language",
            "text": cleaned_text,
            "plan_state": "proposal_ready",
            "mood": mood,
            "emotion_tags": tags,
            "voice_tone_hint": voice_tone,
            "avatar_expression_hint": avatar_expression,
            "gesture_hint": gesture,
            "response_style_hint": response_style,
            "avatar_plan": avatar_plan,
            "gesture_plan": gesture_plan,
            "voice_runtime_alpha_ready": self.voice_runtime_alpha.status()["alpha_ready"],
            "avatar_runtime_alpha_ready": self.avatar_runtime_alpha.status()["alpha_ready"],
            "expression_state": self.expression_state(),
            "execution_ready": False,
            "executed": False,
            "avatar_changed": False,
            "gesture_changed": False,
            "voice_output_performed": False,
            "speaker_output": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "safety_notes": [
                "Expression plan is internal and proposal-only.",
                "No avatar expression was changed.",
                "No avatar gesture was changed.",
                "No voice output was played.",
                "No file was written.",
                "No command was executed.",
                "Voice and avatar runtime remain disabled until explicit confirmation.",
            ],
        }

    def context(self) -> dict[str, Any]:
        status = self.status()
        state = self.expression_state()

        return {
            "status": self.status_name,
            "context_ready": True,
            "expression_status": status,
            "expression_state": state,
            "avatar_runtime_context": self.avatar_runtime_alpha.context(),
            "voice_runtime_context": self.voice_runtime_alpha.context(),
            "safe_current_capabilities": [
                "expression_language_status",
                "expression_state",
                "expression_plan",
                "expression_voice_hint",
                "expression_avatar_hint",
                "expression_gesture_hint",
                "expression_context",
            ],
            "disabled_capabilities": [
                "automatic_avatar_expression_change",
                "automatic_avatar_gesture_change",
                "automatic_voice_output",
                "automatic_speaker_playback",
                "automatic_file_write",
                "command_execution",
            ],
            "read_only": True,
            "write_performed": False,
            "avatar_changed": False,
            "gesture_changed": False,
            "voice_output_performed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "note": "Expression context is read-only and preparation-only.",
        }

    def status(self) -> dict[str, Any]:
        state = self.expression_state()

        prepare_permission = self.permission_manager.check("prepare_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "language_ready": True,
            "state_ready": True,
            "plan_ready": True,
            "voice_hint_ready": True,
            "avatar_hint_ready": True,
            "gesture_hint_ready": True,
            "context_ready": True,
            "mood_states": len(state["supported_moods"]),
            "emotion_tags": len(state["supported_emotion_tags"]),
            "voice_tones": len(state["supported_voice_tones"]),
            "avatar_expressions": len(state["supported_avatar_expressions"]),
            "gestures": len(state["supported_gestures"]),
            "response_styles": len(state["supported_response_styles"]),
            "requires_prepare_confirmation": prepare_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
            "requires_command_confirmation": command_permission.requires_confirmation,
            "runtime_ready": False,
            "read_only": True,
            "avatar_changed": False,
            "gesture_changed": False,
            "voice_output": False,
            "speaker_output": False,
            "file_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
            "sections": 7,
            "project_root": str(self.project_root),
            "note": "AURA Expression Language is online as an internal planning layer. It does not change avatar state, play voice output, write files, or execute commands automatically.",
        }
