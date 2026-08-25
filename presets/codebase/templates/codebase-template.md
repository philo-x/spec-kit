---
schema_version: "1.0"
generator: "speckit.codebase"
analysis_profiles:
  - generic
source_commit: "[SOURCE_COMMIT]"
working_tree: "[WORKING_TREE]"
evidence_tier: "verify"
---

# [PROJECT_NAME] Codebase Context

> Generated from current repository evidence. Inferred or unknown conclusions
> are marked explicitly. Repository paths are relative to the repository root.

## 1. System Purpose

[Describe the system's purpose, users, and primary responsibilities.]

## 2. Technology Inventory

| Layer | Technology | Version / Detail | Usage Status | Confidence | Evidence |
|---|---|---|---|---|---|
| [Layer] | [Technology] | [Version or detail] | [Status] | [Confidence] | [Path or symbol] |

## 3. Module and Package Map

### Module Tree

[List build modules in stable build-file order and group low-value modules when appropriate.]

### Dependency Direction

[Describe verified dependency direction and major boundaries.]

### Package Conventions

[Describe repository-specific package placement rules.]

### Entry Points

[List deployable, job, listener, CLI, or public library entry points.]

## 4. Request, Messaging, Job, and Data Flows

### Global Request and Exception Pipeline

[Describe only ordering supported by registration or source evidence.]

### Representative Traces

[Summarize one to five representative flows with their entry, major hops,
transaction boundary, side effects, external boundary, and failure path.]

## 5. Persistence Model and Transaction Boundaries

[Describe storage technologies, model conventions, identifiers, auditing,
tenant or logical-delete behavior, migrations, and transaction boundaries.]

## 6. Integration Points

| Integration | Mechanism | Consumer | Usage Status | Confidence | Evidence |
|---|---|---|---|---|---|
| [Integration] | [Mechanism] | [Consumer] | [Status] | [Confidence] | [Path or symbol] |

## 7. Security Model

[Describe authentication, authorization, data authority, tenant boundaries,
request protection, and repository-specific whitelist rules without secret values.]

## 8. Testing Strategy

[Describe test frameworks actually used, unit/integration boundaries, naming,
required infrastructure, Maven plugins, and representative test patterns.]

## 9. Coding and Repository Modification Conventions

[Record repository-specific rules for modules, APIs, services, models,
persistence adapters, exceptions, validation, tests, and configuration.]

## 10. Operational Constraints and Automation

[Describe required runtimes, profiles, ports, infrastructure, packaging,
container/deployment behavior, CI, quality gates, and documented constraints.]

## 11. Known Risks and Technical Debt

| Finding | Impact | Confidence | Evidence | Recommendation |
|---|---|---|---|---|
| [High-value finding] | [Impact] | [Confidence] | [Path or symbol] | [Actionable recommendation] |

## 12. Build, Test, Quality, and Run Commands

| Purpose | Command | Preconditions | Evidence |
|---|---|---|---|
| [Purpose] | `[Repository-declared command]` | [Required profile or infrastructure] | [Wrapper, POM, CI, or documentation path] |

## 13. Evidence and Coverage Limitations

[Record the codebase-memory project and index status, bounded scopes checked,
excluded or stale paths read directly, unresolved external behavior, and any
conclusion that remains inferred or unknown.]

<!-- PROJECT OVERRIDES START -->
## 14. Project Overrides

> Human-maintained and preserved verbatim. The generator does not validate this
> section or use it to raise the confidence of generated findings.

<!-- PROJECT OVERRIDES END -->
