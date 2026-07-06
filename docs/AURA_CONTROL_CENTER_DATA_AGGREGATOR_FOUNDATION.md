# AURA Control Center Data Aggregator Foundation

Status: COMPLETED
Version: v0.93.0-genesis
Sprint: 93.0
Phase: Genesis
Owner: Kiput
Motto: Grow Together

## Purpose

AURA Control Center Data Aggregator Foundation prepares the planner-only data aggregation layer for the future AURA Control Center.

This sprint does not fetch runtime data, connect to ORION, create client pairings, send or receive heartbeats, fetch or forward audit events, render dashboard views, start API/web/client runtime, or execute actions.

The purpose is to define dashboard packet blueprints that can later represent both ATLAS core status and ORION Client Agent status.

## Relationship to ATLAS and ORION

This sprint follows the canonical ATLAS-ORION deployment plan.

ATLAS represents:

- AURA core
- reasoning
- memory
- personality
- permission authority
- planner
- audit center
- future backend
- plugin registry
- client coordination

ORION represents:

- AURA Client Agent
- local body and senses
- screen bridge
- short recording and frame sampling bridge
- voice bridge
- avatar and 3D environment runtime bridge
- local action bridge
- OBS/streaming bridge
- game companion bridge
- Blender bridge
- VS Code/project bridge
- emergency stop
- GPU-heavy workload host

Sprint 93 only prepares metadata and packet blueprints for those future states.

## Added Module

Package:

- aura/control_center_data_aggregator/

Manager:

- AuraControlCenterDataAggregatorFoundationManager

The manager prepares:

- aggregator status
- aggregator packet catalog plan
- ATLAS core packet plan
- ORION client packet plan
- client bridge packet plan
- dashboard view packet plan
- permission scope packet plan
- health snapshot packet plan
- audit event visibility packet plan
- data aggregator safety policy plan
- full context packet

## Plan Types

Sprint 93 defines 11 plan types:

1. control_center_data_aggregator_status
2. aggregator_packet_catalog_plan
3. atlas_core_packet_plan
4. orion_client_packet_plan
5. client_bridge_packet_plan
6. dashboard_view_packet_plan
7. permission_scope_packet_plan
8. health_snapshot_packet_plan
9. audit_event_visibility_packet_plan
10. data_aggregator_safety_policy_plan
11. control_center_data_aggregator_context

## Packet Groups

Sprint 93 defines 7 packet groups:

1. ATLAS Core Packet Group
2. ORION Client Packet Group
3. Client Bridge Packet Group
4. Dashboard View Packet Group
5. Permission Scope Packet Group
6. Health Snapshot Packet Group
7. Audit Event Visibility Field Group

## Packet Counts

Final blueprint counts:

- aggregation packet groups: 7
- ATLAS core packets: 6
- ORION client packets: 8
- client bridge packets: 8
- dashboard view packets: 9
- permission scope packets: 7
- health snapshot packets: 10
- audit event visibility fields: 8
- total blueprint packets/fields: 56

## ATLAS Core Packets

The ATLAS packet group reserves future dashboard metadata for:

- ATLAS identity status
- ATLAS capability registry
- ATLAS permission workflow
- ATLAS runtime service foundation
- ATLAS launcher health foundation
- ATLAS roadmap status

No runtime ATLAS data is fetched.

## ORION Client Packets

The ORION packet group reserves future dashboard metadata for:

- ORION client identity
- ORION voice bridge
- ORION screen bridge
- ORION avatar and 3D environment
- ORION local action bridge
- ORION Blender bridge
- ORION VS Code project bridge
- ORION streaming and game bridge

No ORION client connection is opened.

## Client Bridge Packets

The client bridge packet group reserves future metadata for:

- pairing status
- client heartbeat
- client latency
- client permission scope
- client emergency stop
- client audit forwarding
- client plugin health
- client runtime boundary

No pairing, heartbeat, client connection, or audit forwarding runtime is activated.

## Dashboard View Packets

The dashboard view packet group reserves future metadata for:

- Genesis dashboard view
- chat console view
- permission center view
- capability viewer view
- plugin dashboard view
- service and launcher view
- ORION client view
- work mode view
- roadmap view

No dashboard view is rendered.

## Permission Scope Packets

The permission scope packet group reserves future metadata for:

- one-time permission scope
- session permission scope
- workspace permission scope
- app permission scope
- mode permission scope
- plugin permission scope
- emergency stop scope

No permission is granted, denied, resolved, or activated.

## Health Snapshot Packets

The health snapshot packet group reserves future metadata for:

- ATLAS core health
- ATLAS memory health
- ATLAS permission health
- ATLAS API schema health
- ORION client health
- ORION voice health
- ORION screen health
- ORION avatar health
- ORION app bridge health
- ORION emergency stop health

No runtime health data is fetched.

## Audit Event Visibility Fields

The audit event visibility group reserves future fields for:

- event_id
- source_device
- action_type
- target
- permission_scope
- risk_level
- result
- timestamp

No audit event is fetched or forwarded.

## Integration

Sprint 93 integrates with:

- skills registry
- plugin action registry
- system status manager
- CLI
- shell
- documentation
- capability registry
- project identity/version metadata

## CLI and Shell Commands

Sprint 93 adds commands for:

- control-center-data-aggregator-status
- aggregator-packet-catalog-plan
- atlas-core-packet-plan
- orion-client-packet-plan
- client-bridge-packet-plan
- dashboard-view-packet-plan
- permission-scope-packet-plan
- health-snapshot-packet-plan
- audit-event-visibility-packet-plan
- data-aggregator-safety-policy-plan
- control-center-data-aggregator-context

All commands are planner-only and metadata-only.

## Safety Boundary

Sprint 93 explicitly keeps disabled:

- data aggregator runtime
- runtime data fetch
- client connection
- client pairing runtime
- client heartbeat runtime
- client audit fetch runtime
- client audit forwarding runtime
- dashboard render runtime
- API server runtime
- API route runtime
- API request handling
- API response serving
- HTTP server start
- web server runtime
- local web server start
- frontend runtime
- backend runtime
- route creation runtime
- static file serving runtime
- port binding
- browser launch
- websocket runtime
- chat runtime
- session runtime
- plugin runtime
- permission grant runtime
- permission deny runtime
- runtime action activation
- runtime behavior change
- service runtime
- launcher runtime
- ORION client runtime
- voice bridge runtime
- screen capture runtime
- short recording runtime
- avatar runtime
- 3D environment runtime
- OBS bridge runtime
- game companion runtime
- Blender bridge runtime
- VS Code project bridge runtime
- local action bridge runtime
- emergency stop runtime
- file read/write/modify/delete
- command execution
- test execution
- code execution
- dependency install
- package download
- internet search
- network action
- tool execution
- real tool execution
- external action execution
- memory write
- desktop control
- git init/add/commit/push from AURA runtime

## Runtime Counters

Final expected runtime counters:

- runtime_packets_collected: 0
- runtime_data_fetches: 0
- client_connections_opened: 0
- client_pairings_created: 0
- client_heartbeats_sent: 0
- client_heartbeats_received: 0
- dashboard_views_rendered: 0
- api_requests_handled: 0
- api_responses_served: 0
- audit_events_fetched: 0
- audit_events_forwarded: 0
- runtime_execution_features: 0

## Result

Sprint 93 prepares AURA for future Control Center aggregation while keeping the system fully safe_idle-first, metadata-only, planner-only, and foundation-only.

The future Control Center can now reason about dashboard packet categories for both ATLAS and ORION without activating runtime fetching or client execution.
