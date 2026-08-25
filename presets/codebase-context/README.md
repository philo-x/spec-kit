# Codebase Context

This preset generates verified repository context at
`.specify/memory/codebase-context.md` and makes the core `plan`, `tasks`,
`analyze`, and `implement` workflows consume it.

It provides one standalone generator command, `speckit.codebase-context`, and
replaces four core commands with complete English command files based on Spec
Kit v1.0.1. The codebase-aware instructions are embedded at the same workflow
points as the original customized skills, while the original script selection,
frontmatter, hooks, and native agent command references remain intact.

Because the four consumer commands use `strategy: replace`, they do not inherit
future changes to the corresponding core commands automatically. Review and
resynchronize them when upgrading Spec Kit.

## Generator

Run `speckit.codebase-context` through the active coding agent after installing
the preset. The command:

- prefers the codebase-memory-mcp tool surface and falls back to its local CLI;
- creates a full local graph index with `persistence=false` when needed;
- performs a generic repository analysis for every project;
- enables a deeper Spring Boot Maven profile when matching POM evidence exists;
- verifies important graph findings against current source, build,
  configuration, CI, deployment, and representative test files;
- generates a compact English context document with explicit evidence and
  coverage limitations; and
- preserves the marked Project Overrides section on later refreshes.

The command does not install codebase-memory-mcp and does not silently replace
it with a grep-only analysis. Install and configure
[codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) as an MCP
server or make its local `codebase-memory-mcp` executable available on `PATH`.

The generator records repository-declared build, test, quality, run, and
deployment commands but does not execute them. It does not modify application
source, build files, configuration, tests, or deployment artifacts.

## Context Contract

Generated files carry this ownership marker in frontmatter:

```yaml
generator: "speckit.codebase-context"
```

The generator refreshes an owned file only when its schema and Project
Overrides markers are valid. It preserves content between:

```markdown
<!-- PROJECT OVERRIDES START -->
<!-- PROJECT OVERRIDES END -->
```

An existing unowned file is not overwritten by default. Move trusted manual
content into a Project Overrides section, then invoke the command with
`--replace-existing` only when a full replacement is intended. There is no
automatic adopt mode because old generated and human-authored statements cannot
be distinguished safely.

The file is optional for the four consumer workflows. If it is absent, each
consumer follows the unmodified core workflow.

## Workflow Effects

| Command | Added behavior |
|---------|----------------|
| `speckit.codebase-context` | Generates or refreshes verified repository context with a generic baseline and optional Spring Boot Maven profile. |
| `speckit.plan` | Uses existing architecture and conventions to fill Technical Context, focus repository discovery, limit external research, and shape data models and contracts. |
| `speckit.tasks` | Uses module and persistence conventions to anchor Setup and Foundational tasks in the existing codebase. |
| `speckit.analyze` | Optionally checks plan and task references against repository context and corroborating repository evidence before implementation. |
| `speckit.implement` | Loads coding conventions and repository-specific validation commands before executing tasks. |

## Installation

From a Spec Kit project, install this checkout as a development preset:

```bash
specify preset add --dev /path/to/spec-kit/presets/codebase-context
```

Verify the resolved generator, output template, and consumer commands:

```bash
specify preset resolve speckit.codebase-context
specify preset resolve codebase-context-template
specify preset resolve speckit.plan
specify preset resolve speckit.tasks
specify preset resolve speckit.analyze
specify preset resolve speckit.implement
```

Remove it with:

```bash
specify preset remove codebase-context
```
