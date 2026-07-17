# AURA Operational Browser Chat Model Handoff

- Version: `v1.2.2`
- Sprint: `262`
- Boundary: `operational_browser_chat_model_handoff`
- Next boundary: `session_list_resume_rename_archive_restore`
- Primary interface: browser Control Center
- Primary model route: `companion`

The existing explicitly confirmed route
`POST /api/chat/sessions/{session_id}/model-messages` is the canonical
operational browser-to-model handoff. User/model pairs remain atomic and
idempotent. The save-only route remains available and does not invoke a model.

Native process-role classification now distinguishes `service_runtime`,
`control_plane`, and `unclassified_main`. Control-plane commands remain visible
but are not counted as strict service conflicts. The Sprint 260 count allowance
removed all post-observation subtraction and override logic.

Implementation validation uses a deterministic isolated response factory. It
opens no network connection and executes no real model request. Sprint 262
finalization must run one live model handoff rehearsal and restore AURA to
safe-idle.
