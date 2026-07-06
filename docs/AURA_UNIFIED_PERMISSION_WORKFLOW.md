# AURA Unified Permission Workflow Manager

Target version: v0.83.0-genesis  
Status: UNIFIED PERMISSION WORKFLOW ONLINE

## Purpose

The Unified Permission Workflow Manager provides a planner-only foundation for unifying how AURA prepares permission requests, approval/deny state planning, risk reviews, confirmation prompts, audit trail planning, and future AURA Control Center Permission Center views.

This sprint does not grant permission and does not execute any action.

## Current Permission Workflow Summary

| Metric | Count |
|---|---:|
| Permission templates | 12 |
| Permission categories | 13 |
| Permission request states | 7 |
| Approval modes | 5 |
| Risk levels | 4 |
| Explicit confirmation required templates | 11 |
| Runtime-enabled templates | 0 |
| Always-approve templates | 0 |
| Runtime execution features | 0 |

## Permission Categories

The workflow tracks permission categories for:

- read_project
- user_confirmation
- microphone_permission
- camera_permission
- screen_permission
- file_write_permission
- command_execution_permission
- dependency_download_permission
- internet_search_permission
- desktop_control_permission
- git_operation_permission
- service_control_permission
- plugin_install_permission

## Approval Modes

Genesis phase supports only safe planning labels:

- none
- approve_once
- deny
- review_details
- request_clarification

Important rule:

There is no always-approve mode in Genesis phase.

## Permission Request States

The workflow can plan these states:

- draft
- pending_review
- approved_once_planned
- denied_planned
- expired_planned
- cancelled_planned
- audit_only

These are planning states only. They do not grant runtime permission.

## Permission Center Direction

The future AURA Control Center can use this workflow to display:

- pending permission requests
- risk level
- requested action
- target resource
- Approve Once button
- Deny button
- Review Details button
- Request Clarification button
- audit metadata

The Permission Center must not bypass the permission workflow.

## Safety Boundary

This sprint is permission-workflow-only, planner-only, proposal-only, and metadata-only.

It does not enable:

- permission grant runtime
- automatic approval
- always-approve mode
- background approval
- runtime action activation
- runtime behavior changes
- file operation runtime
- command execution runtime
- dependency install runtime
- download runtime
- microphone runtime
- camera runtime
- screen capture runtime
- internet runtime
- desktop control runtime
- git operation runtime
- plugin install runtime
- service control runtime
- UI runtime
- web server runtime
- chat runtime
- launcher runtime
- file operations
- command execution
- test execution
- code execution
- dependency install
- package download
- internet or network action
- tool execution
- memory write
- desktop control
- git execution
- external action execution
- real tool execution

## Design Principle

AURA may prepare permission requests, but AURA must not grant permission to herself.
