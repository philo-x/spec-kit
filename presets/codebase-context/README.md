# Codebase Context

This preset augments the core `plan`, `tasks`, and `implement` commands with
optional repository context from `.specify/memory/codebase-context.md`.

It replaces the three core commands with complete English command files based
on Spec Kit v1.0.1. The codebase-aware instructions are embedded at the same
workflow points as the original customized skills, while the original script
selection, frontmatter, hooks, and native agent command references remain
intact.

Because this preset uses `strategy: replace`, its command files do not inherit
future changes to the corresponding core commands automatically. Review and
resynchronize them when upgrading Spec Kit.

## Context Contract

The preset expects another process to create and maintain
`.specify/memory/codebase-context.md`. When present, the file may describe:

- the architecture baseline and module/package map;
- framework and dependency versions;
- entity, primary-key, persistence, DAO, and controller conventions;
- security standards; and
- test and build commands.

The file is optional. If it is absent, each command follows the unmodified core
workflow.

## Workflow Effects

| Command | Added behavior |
|---------|----------------|
| `speckit.plan` | Uses existing architecture and conventions to fill Technical Context, focus repository discovery, limit external research, and shape data models and contracts. |
| `speckit.tasks` | Uses module and persistence conventions to anchor Setup and Foundational tasks in the existing codebase. |
| `speckit.implement` | Loads coding conventions and repository-specific validation commands before executing tasks. |

## Installation

From a Spec Kit project, install this checkout as a development preset:

```bash
specify preset add --dev /path/to/spec-kit/presets/codebase-context
```

Verify the composed commands:

```bash
specify preset resolve speckit.plan
specify preset resolve speckit.tasks
specify preset resolve speckit.implement
```

Remove it with:

```bash
specify preset remove codebase-context
```
