import importlib.util
import shutil
from pathlib import Path
from typing import Any

from aura.blender.blender_bridge_foundation_manager import BlenderBridgeFoundationManager
from aura.permissions.permission_manager import PermissionManager
from aura.plugins.builtin.project_plugin import ProjectPlugin
from aura.vision.vision_runtime_alpha_manager import VisionRuntimeAlphaManager
from aura.workspace.workspace_awareness_manager import WorkspaceAwarenessManager


class MediaUnderstandingFoundationManager:
    """
    AURA Media Understanding Foundation.

    Current phase:
    - identify safe visible media files by metadata only
    - summarize image, texture, video, audio, and 3D media candidates
    - prepare image description plans
    - prepare texture reference plans
    - prepare thumbnail/banner review plans
    - prepare video/audio planning context
    - integrate workspace, vision, avatar, and Blender planning context
    - never read pixels automatically
    - never open media files automatically
    - never edit/write media files automatically
    - never execute ffmpeg, Blender, or shell commands automatically
    """

    name = "media_understanding_foundation"
    version = "0.1.0"
    status_name = "foundation"

    IMAGE_SUFFIXES = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".bmp",
        ".gif",
        ".tga",
        ".tif",
        ".tiff",
        ".exr",
        ".hdr",
        ".svg",
        ".psd",
    }

    VIDEO_SUFFIXES = {
        ".mp4",
        ".mov",
        ".mkv",
        ".webm",
        ".avi",
        ".m4v",
        ".flv",
    }

    AUDIO_SUFFIXES = {
        ".wav",
        ".mp3",
        ".ogg",
        ".flac",
        ".m4a",
        ".aac",
    }

    THREE_D_SUFFIXES = {
        ".blend",
        ".fbx",
        ".obj",
        ".glb",
        ".gltf",
        ".dae",
        ".stl",
        ".abc",
        ".usd",
        ".usdz",
    }

    DESIGN_SUFFIXES = {
        ".ai",
        ".ase",
        ".kra",
        ".clip",
    }

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.permission_manager = PermissionManager()
        self.project_plugin = ProjectPlugin(project_root=self.project_root)
        self.workspace = WorkspaceAwarenessManager(project_root=self.project_root)
        self.blender_bridge = BlenderBridgeFoundationManager(project_root=self.project_root)
        self.vision_runtime = VisionRuntimeAlphaManager(project_root=self.project_root)

    def dependency_check(self) -> dict[str, Any]:
        python_packages = [
            {
                "name": "PIL",
                "purpose": "future image metadata/pixel handling through Pillow",
                "installed": importlib.util.find_spec("PIL") is not None,
            },
            {
                "name": "cv2",
                "purpose": "future image/video frame processing through OpenCV",
                "installed": importlib.util.find_spec("cv2") is not None,
            },
            {
                "name": "numpy",
                "purpose": "future frame/image buffer processing",
                "installed": importlib.util.find_spec("numpy") is not None,
            },
        ]

        executables = [
            {
                "name": "ffmpeg",
                "purpose": "future video/audio metadata and conversion candidate",
                "found": shutil.which("ffmpeg") is not None,
            },
            {
                "name": "ffprobe",
                "purpose": "future video/audio metadata probing candidate",
                "found": shutil.which("ffprobe") is not None,
            },
            {
                "name": "magick",
                "purpose": "future image metadata/conversion candidate",
                "found": shutil.which("magick") is not None,
            },
            {
                "name": "convert",
                "purpose": "future ImageMagick fallback candidate",
                "found": shutil.which("convert") is not None,
            },
        ]

        return {
            "status": "checked",
            "dependency_check_ready": True,
            "runtime_ready": False,
            "python_packages": python_packages,
            "executables": executables,
            "python_packages_installed": sum(1 for item in python_packages if item["installed"]),
            "python_packages_total": len(python_packages),
            "executables_found": sum(1 for item in executables if item["found"]),
            "executables_total": len(executables),
            "pixel_read_ready": False,
            "media_file_open_ready": False,
            "media_file_write_ready": False,
            "command_execution_ready": False,
            "note": "Passive media dependency check only. No media file was opened, no pixels were read, no file was written, and no command was executed.",
        }

    def known_suffixes(self) -> set[str]:
        return (
            self.IMAGE_SUFFIXES
            | self.VIDEO_SUFFIXES
            | self.AUDIO_SUFFIXES
            | self.THREE_D_SUFFIXES
            | self.DESIGN_SUFFIXES
        )

    def classify_suffix(self, suffix: str) -> str:
        normalized = suffix.lower()

        if normalized in self.IMAGE_SUFFIXES:
            return "image_or_texture"

        if normalized in self.VIDEO_SUFFIXES:
            return "video"

        if normalized in self.AUDIO_SUFFIXES:
            return "audio"

        if normalized in self.THREE_D_SUFFIXES:
            return "3d_asset"

        if normalized in self.DESIGN_SUFFIXES:
            return "design_source"

        return "unknown"

    def safe_project_files(self, limit: int = 2000) -> list[str]:
        return self.project_plugin.list_files(limit=max(1, min(limit, 3000)))

    def media_assets(self, limit: int = 200) -> list[dict[str, Any]]:
        limit = max(1, min(limit, 500))
        assets: list[dict[str, Any]] = []

        for relative_path in self.safe_project_files(limit=3000):
            suffix = Path(relative_path).suffix.lower()

            if suffix not in self.known_suffixes():
                continue

            target = self.project_plugin.resolve_safe_path(relative_path)

            assets.append(
                {
                    "path": relative_path,
                    "suffix": suffix,
                    "category": self.classify_suffix(suffix),
                    "size_bytes": target.stat().st_size if target.is_file() else 0,
                    "metadata_only": True,
                    "pixel_read": False,
                    "file_opened": False,
                }
            )

            if len(assets) >= limit:
                break

        return assets

    def asset_summary(self) -> dict[str, Any]:
        assets = self.media_assets(limit=500)
        by_category: dict[str, int] = {}
        by_suffix: dict[str, int] = {}

        for item in assets:
            by_category[item["category"]] = by_category.get(item["category"], 0) + 1
            by_suffix[item["suffix"]] = by_suffix.get(item["suffix"], 0) + 1

        image_count = by_category.get("image_or_texture", 0)
        video_count = by_category.get("video", 0)
        audio_count = by_category.get("audio", 0)
        three_d_count = by_category.get("3d_asset", 0)
        design_count = by_category.get("design_source", 0)

        return {
            "status": "ready",
            "asset_summary_ready": True,
            "candidate_count": len(assets),
            "image_count": image_count,
            "texture_reference_count": image_count,
            "video_count": video_count,
            "audio_count": audio_count,
            "three_d_count": three_d_count,
            "design_source_count": design_count,
            "by_category": by_category,
            "by_suffix": by_suffix,
            "assets": assets[:80],
            "metadata_only": True,
            "file_opened": False,
            "pixel_read": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "note": "Media asset summary is metadata-only and based on safe visible project files.",
        }

    def base_plan(self, plan_type: str, target: str, recommended_steps: list[str]) -> dict[str, Any]:
        cleaned_target = target.strip() or "<unspecified>"

        read_permission = self.permission_manager.check("read_project")
        prepare_permission = self.permission_manager.check("prepare_file")
        open_file_permission = self.permission_manager.check("open_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "status": "planned",
            "plan_type": plan_type,
            "target": cleaned_target,
            "plan_state": "proposal_ready",
            "workspace_summary": self.workspace.context()["workspace_summary"],
            "asset_summary": self.asset_summary(),
            "dependency_check": self.dependency_check(),
            "vision_context_ready": self.vision_runtime.status()["vision_context_ready"],
            "blender_context_ready": self.blender_bridge.status()["context_ready"],
            "recommended_steps": recommended_steps,
            "permissions": {
                "read_project": read_permission.to_dict(),
                "prepare_file": prepare_permission.to_dict(),
                "open_file": open_file_permission.to_dict(),
                "write_file": write_permission.to_dict(),
                "run_command": command_permission.to_dict(),
            },
            "metadata_only": True,
            "execution_ready": False,
            "executed": False,
            "media_file_opened": False,
            "pixel_read": False,
            "image_pixel_read": False,
            "video_frame_read": False,
            "audio_stream_read": False,
            "thumbnail_generated": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "safety_notes": [
                "Media understanding plan is proposal-only.",
                "No media file was opened.",
                "No image pixels were read.",
                "No video frame was decoded.",
                "No audio stream was read.",
                "No thumbnail, texture, or edited media file was written.",
                "No ffmpeg, Blender, or shell command was executed.",
                "Future real media analysis must go through explicit permission and confirmation.",
            ],
        }

    def image_description_plan(self, image_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="image_description",
            target=image_goal,
            recommended_steps=[
                "Identify the intended image role: reference, texture, thumbnail, banner, or concept art.",
                "Collect metadata-only candidates by suffix and path.",
                "Prepare visual questions to answer once pixel reading is explicitly approved.",
                "Plan safe description fields: subject, style, colors, composition, and usage notes.",
                "Keep image opening and pixel reading disabled until user confirmation.",
            ],
        )

    def texture_reference_plan(self, texture_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="texture_reference",
            target=texture_goal,
            recommended_steps=[
                "Identify target material or surface.",
                "List possible texture/reference candidates by path and suffix.",
                "Plan color, roughness, normal, alpha, emission, and UV requirements.",
                "Connect texture planning with Blender Bridge material planning.",
                "Keep texture file reading/writing disabled until user-approved workflow.",
            ],
        )

    def thumbnail_review_plan(self, review_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="thumbnail_banner_review",
            target=review_goal,
            recommended_steps=[
                "Clarify platform: YouTube thumbnail, YouTube banner, stream overlay, or profile image.",
                "Plan review criteria: readability, contrast, brand consistency, focal point, and safe area.",
                "Prepare checklist for title/logo placement and mobile visibility.",
                "Identify candidate image files by metadata only.",
                "Keep image opening, pixel reading, and edits disabled until confirmation.",
            ],
        )

    def video_plan(self, video_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="video_audio_understanding",
            target=video_goal,
            recommended_steps=[
                "Clarify video/audio purpose, duration, platform, and target output.",
                "Identify video/audio file candidates by suffix and metadata only.",
                "Plan future metadata inspection with ffprobe only after approval.",
                "Plan key review points: intro, pacing, audio clarity, transitions, and export format.",
                "Keep video decoding, audio reading, file writing, and command execution disabled.",
            ],
        )

    def context(self) -> dict[str, Any]:
        status = self.status()

        return {
            "status": self.status_name,
            "context_ready": True,
            "media_status": status,
            "workspace_context": self.workspace.context(),
            "blender_context": self.blender_bridge.context(),
            "vision_context": self.vision_runtime.context(),
            "dependency_check": self.dependency_check(),
            "asset_summary": self.asset_summary(),
            "safe_current_capabilities": [
                "media_understanding_status",
                "media_asset_summary",
                "media_image_description_plan",
                "media_texture_reference_plan",
                "media_thumbnail_banner_review_plan",
                "media_video_audio_plan",
                "media_context",
            ],
            "disabled_capabilities": [
                "automatic_media_file_open",
                "automatic_pixel_read",
                "automatic_video_frame_decode",
                "automatic_audio_stream_read",
                "automatic_thumbnail_generation",
                "automatic_media_file_write",
                "ffmpeg_command_execution",
                "blender_command_execution",
                "shell_command_execution",
            ],
            "read_only": True,
            "metadata_only": True,
            "write_performed": False,
            "media_file_opened": False,
            "pixel_read": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "note": "Media Understanding Foundation context is metadata-only, read-only, and preparation-only.",
        }

    def status(self) -> dict[str, Any]:
        dependency = self.dependency_check()
        summary = self.asset_summary()

        open_file_permission = self.permission_manager.check("open_file")
        prepare_permission = self.permission_manager.check("prepare_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "understanding_ready": True,
            "asset_summary_ready": True,
            "image_plan_ready": True,
            "texture_reference_ready": True,
            "thumbnail_review_ready": True,
            "video_plan_ready": True,
            "context_ready": True,
            "dependency_check_ready": True,
            "metadata_inspection_ready": True,
            "candidate_count": summary["candidate_count"],
            "image_count": summary["image_count"],
            "texture_reference_count": summary["texture_reference_count"],
            "video_count": summary["video_count"],
            "audio_count": summary["audio_count"],
            "three_d_count": summary["three_d_count"],
            "design_source_count": summary["design_source_count"],
            "pil_found": any(item["name"] == "PIL" and item["installed"] for item in dependency["python_packages"]),
            "cv2_found": any(item["name"] == "cv2" and item["installed"] for item in dependency["python_packages"]),
            "numpy_found": any(item["name"] == "numpy" and item["installed"] for item in dependency["python_packages"]),
            "ffmpeg_found": any(item["name"] == "ffmpeg" and item["found"] for item in dependency["executables"]),
            "ffprobe_found": any(item["name"] == "ffprobe" and item["found"] for item in dependency["executables"]),
            "requires_open_file_confirmation": open_file_permission.requires_confirmation,
            "requires_prepare_confirmation": prepare_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
            "requires_command_confirmation": command_permission.requires_confirmation,
            "runtime_ready": False,
            "read_only": True,
            "metadata_only": True,
            "media_file_opened": False,
            "media_pixel_read": False,
            "image_pixel_read": False,
            "video_frame_read": False,
            "audio_stream_read": False,
            "thumbnail_generated": False,
            "file_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
            "sections": 7,
            "project_root": str(self.project_root),
            "note": "Media Understanding Foundation is online for metadata-only media planning. It does not open media files, read pixels, write files, or execute commands automatically.",
        }
