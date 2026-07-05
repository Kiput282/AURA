import importlib.util
import shutil
from pathlib import Path
from typing import Any

from aura.permissions.permission_manager import PermissionManager
from aura.plugins.builtin.project_plugin import ProjectPlugin
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.workspace.workspace_awareness_manager import WorkspaceAwarenessManager


class BlenderBridgeFoundationManager:
    """
    AURA Blender Bridge Foundation.

    Current phase:
    - detect Blender/bpy availability passively
    - read safe workspace/project asset candidates
    - prepare Blender scene plans
    - prepare Blender asset plans
    - prepare texture/material/shader plans
    - prepare rigging plans
    - prepare animation plans
    - prepare Blender context for future reasoning
    - never open Blender automatically
    - never execute Blender scripts automatically
    - never write .blend/.py/image files automatically
    - never execute shell commands
    """

    name = "blender_bridge_foundation"
    version = "0.1.0"
    status_name = "foundation"

    BLENDER_ASSET_SUFFIXES = {
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

    TEXTURE_SUFFIXES = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
        ".tga",
        ".tif",
        ".tiff",
        ".exr",
        ".hdr",
        ".bmp",
        ".svg",
        ".psd",
    }

    SCRIPT_SUFFIXES = {
        ".py",
    }

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.permission_manager = PermissionManager()
        self.sandbox = ToolSandboxManager(project_root=self.project_root)
        self.workspace = WorkspaceAwarenessManager(project_root=self.project_root)
        self.project_plugin = ProjectPlugin(project_root=self.project_root)

    def dependency_check(self) -> dict[str, Any]:
        bpy_found = importlib.util.find_spec("bpy") is not None
        blender_path = shutil.which("blender")
        ffmpeg_path = shutil.which("ffmpeg")

        return {
            "status": "checked",
            "bridge_ready": True,
            "runtime_ready": False,
            "bpy_found": bpy_found,
            "blender_executable_found": blender_path is not None,
            "blender_executable_path": blender_path or "",
            "ffmpeg_found": ffmpeg_path is not None,
            "ffmpeg_path": ffmpeg_path or "",
            "python_script_execution_ready": False,
            "blender_app_open_ready": False,
            "file_write_ready": False,
            "command_execution_ready": False,
            "note": "Passive Blender dependency check only. No Blender app, script, render, file write, or command execution was performed.",
        }

    def detect_backend(self) -> dict[str, Any]:
        if importlib.util.find_spec("bpy") is not None:
            return {
                "name": "bpy",
                "type": "python_blender_runtime",
                "found": True,
                "path": "",
                "priority": 1,
                "source": "python_package",
            }

        blender_path = shutil.which("blender")

        if blender_path:
            return {
                "name": "blender",
                "type": "external_blender_executable",
                "found": True,
                "path": blender_path,
                "priority": 2,
                "source": "executable",
            }

        return {
            "name": "",
            "type": "",
            "found": False,
            "path": "",
            "priority": 0,
            "source": "",
        }

    def safe_project_files(self, limit: int = 1000) -> list[str]:
        return self.project_plugin.list_files(limit=max(1, min(limit, 2000)))

    def asset_candidates(self, limit: int = 80) -> list[dict[str, Any]]:
        limit = max(1, min(limit, 200))
        files = self.safe_project_files(limit=2000)
        candidates: list[dict[str, Any]] = []

        known_suffixes = self.BLENDER_ASSET_SUFFIXES | self.TEXTURE_SUFFIXES | self.SCRIPT_SUFFIXES

        for relative_path in files:
            suffix = Path(relative_path).suffix.lower()

            if suffix not in known_suffixes:
                continue

            if suffix in self.BLENDER_ASSET_SUFFIXES:
                category = "3d_asset"
            elif suffix in self.TEXTURE_SUFFIXES:
                category = "texture_or_image"
            elif suffix in self.SCRIPT_SUFFIXES:
                category = "python_script_candidate"
            else:
                category = "unknown"

            candidates.append(
                {
                    "path": relative_path,
                    "suffix": suffix,
                    "category": category,
                }
            )

            if len(candidates) >= limit:
                break

        return candidates

    def asset_summary(self) -> dict[str, Any]:
        candidates = self.asset_candidates(limit=200)
        by_category: dict[str, int] = {}
        by_suffix: dict[str, int] = {}

        for item in candidates:
            by_category[item["category"]] = by_category.get(item["category"], 0) + 1
            by_suffix[item["suffix"]] = by_suffix.get(item["suffix"], 0) + 1

        return {
            "status": "ready",
            "asset_awareness_ready": True,
            "candidate_count": len(candidates),
            "by_category": by_category,
            "by_suffix": by_suffix,
            "candidates": candidates[:40],
            "read_only": True,
            "file_write_performed": False,
            "command_execution_performed": False,
            "note": "Asset summary is read-only and based on safe visible project files.",
        }

    def build_command_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        backend = self.detect_backend()
        cleaned_target = target.strip() or "<target>"

        if not backend["found"]:
            return {
                "available": False,
                "backend": backend,
                "command": "",
                "reason": "No Blender backend was found. Install or configure Blender/bpy before future real Blender runtime.",
            }

        if backend["name"] == "bpy":
            command = f"python3 <blender_{plan_type}_script.py>  # target: {cleaned_target}"
        else:
            command = (
                f"{backend['path']} --background <aura_workspace_scene.blend> "
                f"--python <blender_{plan_type}_script.py>"
            )

        return {
            "available": True,
            "backend": backend,
            "command": command,
            "reason": "Blender command proposal prepared for planning only. It is not executed by AURA.",
        }

    def sandbox_check_for_command(self, command: str) -> dict[str, Any] | None:
        if not command:
            return None

        if command.startswith("python3 <"):
            return {
                "command": command,
                "allowed": False,
                "state": "template_only",
                "executed": False,
                "reason": "Template command only; not sent to sandbox as a real command.",
                "note": "No command was executed.",
            }

        return self.sandbox.check_command(command)

    def base_plan(self, plan_type: str, target: str, recommended_steps: list[str]) -> dict[str, Any]:
        cleaned_target = target.strip()

        if not cleaned_target:
            cleaned_target = "<unspecified>"

        prepare_permission = self.permission_manager.check("prepare_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")
        open_app_permission = self.permission_manager.check("open_app")
        command_plan = self.build_command_plan(plan_type=plan_type, target=cleaned_target)
        sandbox_check = self.sandbox_check_for_command(command_plan["command"])

        return {
            "status": "planned",
            "plan_type": plan_type,
            "target": cleaned_target,
            "plan_state": "proposal_ready",
            "workspace_summary": self.workspace.context()["workspace_summary"],
            "asset_summary": self.asset_summary(),
            "dependency_check": self.dependency_check(),
            "recommended_steps": recommended_steps,
            "command_plan": command_plan,
            "sandbox_check": sandbox_check,
            "permissions": {
                "prepare_file": prepare_permission.to_dict(),
                "write_file": write_permission.to_dict(),
                "run_command": command_permission.to_dict(),
                "open_app": open_app_permission.to_dict(),
            },
            "execution_ready": False,
            "executed": False,
            "blender_app_opened": False,
            "blender_script_executed": False,
            "scene_modified": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "safety_notes": [
                "Blender plan is proposal-only.",
                "No Blender application was opened.",
                "No Blender Python script was executed.",
                "No .blend file was created or modified.",
                "No texture, material, rig, or animation file was written.",
                "No shell command was executed.",
                "Future real Blender actions must go through permission, confirmation, and sandbox rules.",
            ],
        }

    def scene_plan(self, scene_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="scene",
            target=scene_goal,
            recommended_steps=[
                "Clarify scene purpose, camera framing, and final output format.",
                "Identify required characters, props, environment assets, and lights.",
                "Prepare collection hierarchy: Character, Environment, Props, Cameras, Lights.",
                "Plan camera angle and safe render settings.",
                "Prepare a future Blender script only after user approval.",
            ],
        )

    def asset_plan(self, asset_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="asset",
            target=asset_goal,
            recommended_steps=[
                "Identify asset category: character, outfit, prop, environment, or UI object.",
                "List source references and required dimensions.",
                "Plan mesh organization, naming convention, and collection placement.",
                "Plan export/import format only if needed.",
                "Keep asset creation as a proposal until explicit confirmation.",
            ],
        )

    def texture_plan(self, texture_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="texture_material",
            target=texture_goal,
            recommended_steps=[
                "Identify material slots and target surfaces.",
                "Plan base color, roughness, metallic, normal, alpha, and emission maps.",
                "Check UV map readiness before texture painting.",
                "Prepare shader/material naming convention.",
                "Keep texture/material file writing disabled until user-approved workflow.",
            ],
        )

    def rigging_plan(self, rigging_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="rigging",
            target=rigging_goal,
            recommended_steps=[
                "Identify skeleton type: humanoid, prop rig, facial rig, or mechanical rig.",
                "Plan bone hierarchy and naming convention.",
                "Plan constraints, IK/FK controls, and deformation groups.",
                "Prepare weight painting checklist.",
                "Keep rig modification disabled until explicit user approval.",
            ],
        )

    def animation_plan(self, animation_goal: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="animation",
            target=animation_goal,
            recommended_steps=[
                "Clarify animation purpose, duration, FPS, and loop behavior.",
                "Plan key poses, timing, easing, and motion arcs.",
                "Identify required rig controls or shape keys.",
                "Plan preview/export workflow.",
                "Keep animation writing/rendering disabled until explicit user approval.",
            ],
        )

    def context(self) -> dict[str, Any]:
        status = self.status()

        return {
            "status": self.status_name,
            "context_ready": True,
            "bridge_status": status,
            "workspace_context": self.workspace.context(),
            "dependency_check": self.dependency_check(),
            "asset_summary": self.asset_summary(),
            "safe_current_capabilities": [
                "blender_bridge_status",
                "blender_scene_plan",
                "blender_asset_plan",
                "blender_texture_material_plan",
                "blender_rigging_plan",
                "blender_animation_plan",
                "blender_context",
            ],
            "disabled_capabilities": [
                "automatic_blender_open",
                "automatic_blender_script_execution",
                "automatic_blend_file_write",
                "automatic_texture_file_write",
                "automatic_rig_modification",
                "automatic_animation_write",
                "command_execution",
            ],
            "read_only": True,
            "write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "blender_app_opened": False,
            "blender_script_executed": False,
            "note": "Blender bridge context is read-only and preparation-only.",
        }

    def status(self) -> dict[str, Any]:
        dependency = self.dependency_check()
        backend = self.detect_backend()
        asset_summary = self.asset_summary()

        prepare_permission = self.permission_manager.check("prepare_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")
        open_app_permission = self.permission_manager.check("open_app")

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "bridge_ready": True,
            "scene_plan_ready": True,
            "asset_plan_ready": True,
            "texture_plan_ready": True,
            "material_plan_ready": True,
            "rigging_plan_ready": True,
            "animation_plan_ready": True,
            "context_ready": True,
            "dependency_check_ready": True,
            "asset_awareness_ready": True,
            "backend_found": backend["found"],
            "backend_name": backend["name"],
            "backend_path": backend["path"],
            "bpy_found": dependency["bpy_found"],
            "blender_executable_found": dependency["blender_executable_found"],
            "blender_executable_path": dependency["blender_executable_path"],
            "ffmpeg_found": dependency["ffmpeg_found"],
            "asset_candidate_count": asset_summary["candidate_count"],
            "requires_prepare_confirmation": prepare_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
            "requires_command_confirmation": command_permission.requires_confirmation,
            "requires_open_app_confirmation": open_app_permission.requires_confirmation,
            "runtime_ready": False,
            "blender_app_opened": False,
            "blender_script_executed": False,
            "scene_modified": False,
            "file_write": False,
            "blend_file_write": False,
            "texture_file_write": False,
            "script_file_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
            "sections": 7,
            "project_root": str(self.project_root),
            "note": "Blender Bridge Foundation is online for safe Blender planning. It does not open Blender, execute Blender scripts, write files, or execute shell commands automatically.",
        }
