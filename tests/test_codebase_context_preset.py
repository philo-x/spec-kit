"""Tests for the local codebase-context preset."""

from pathlib import Path

from specify_cli.presets import PresetManager, PresetManifest, PresetResolver


PRESET_DIR = Path(__file__).parent.parent / "presets" / "codebase-context"
COMMAND_NAMES = (
    "speckit.plan",
    "speckit.tasks",
    "speckit.analyze",
    "speckit.implement",
)
CORE_MARKERS = {
    "speckit.plan": "## Mandatory Post-Execution Hooks",
    "speckit.tasks": "## Task Generation Rules",
    "speckit.analyze": "## Operating Principles",
    "speckit.implement": "## Mandatory Post-Execution Hooks",
}
COMPLETION_MARKERS = {
    "speckit.plan": "## Done When",
    "speckit.tasks": "## Done When",
    "speckit.analyze": "### 8. Offer Remediation",
    "speckit.implement": "## Done When",
}


def test_manifest_declares_replace_layers():
    manifest = PresetManifest(PRESET_DIR / "preset.yml")

    assert manifest.id == "codebase-context"
    assert manifest.version == "1.1.0"
    assert manifest.requires_speckit_version == ">=1.0.1"
    assert {entry["name"] for entry in manifest.templates} == set(COMMAND_NAMES)
    assert all(entry["type"] == "command" for entry in manifest.templates)
    assert all(entry["strategy"] == "replace" for entry in manifest.templates)


def test_replacement_commands_are_complete_english_commands():
    for command_name in COMMAND_NAMES:
        command_file = PRESET_DIR / "commands" / f"{command_name}.md"
        content = command_file.read_text(encoding="utf-8")

        assert ".specify/memory/codebase-context.md" in content
        assert content.startswith("---\n")
        assert "scripts:" in content
        assert "## User Input" in content
        assert COMPLETION_MARKERS[command_name] in content
        assert "{CORE_TEMPLATE}" not in content
        assert "## Codebase Context Augmentation" not in content
        assert not any("\u4e00" <= char <= "\u9fff" for char in content)


def test_install_resolves_replacement_without_composition(tmp_path):
    project_root = tmp_path / "project"
    (project_root / ".specify").mkdir(parents=True)

    manager = PresetManager(project_root)
    manager.install_from_directory(PRESET_DIR, "1.0.1")
    resolver = PresetResolver(project_root)

    for command_name in COMMAND_NAMES:
        layers = resolver.collect_all_layers(command_name, "command")
        assert layers[0]["strategy"] == "replace"
        assert layers[-1]["source"] == "core (bundled)"

        content = resolver.resolve_content(command_name, "command")
        assert content is not None
        command_file = PRESET_DIR / "commands" / f"{command_name}.md"
        assert content == command_file.read_text(encoding="utf-8")
        assert CORE_MARKERS[command_name] in content
        assert ".specify/memory/codebase-context.md" in content
        assert "scripts:" in content


def test_codebase_rules_are_embedded_in_the_original_workflow_positions():
    plan = (PRESET_DIR / "commands" / "speckit.plan.md").read_text(encoding="utf-8")
    tasks = (PRESET_DIR / "commands" / "speckit.tasks.md").read_text(encoding="utf-8")
    implement = (PRESET_DIR / "commands" / "speckit.implement.md").read_text(
        encoding="utf-8"
    )
    analyze = (PRESET_DIR / "commands" / "speckit.analyze.md").read_text(
        encoding="utf-8"
    )

    assert plan.index(".specify/memory/codebase-context.md") < plan.index(
        "## Mandatory Post-Execution Hooks"
    )
    assert plan.index("Prefer an available code graph") > plan.index(
        "### Phase 0: Outline & Research"
    )
    assert plan.index("shared model types, identifier strategies") > plan.index(
        "### Phase 1: Design & Contracts"
    )
    assert "feature-specific APIs, version compatibility" in plan
    assert "DAO or persistence registration point" not in plan
    assert "entity base classes and primary-key strategies" not in plan
    assert "controller and response-wrapper conventions" not in plan
    assert tasks.index(".specify/memory/codebase-context.md") < tasks.index(
        "## Mandatory Post-Execution Hooks"
    )
    assert "repository, mapper, ORM, schema-registration" in tasks
    assert "migration, compatibility, and validation tasks" in tasks
    assert implement.index(".specify/memory/codebase-context.md") < implement.index(
        "4. **Project Setup Verification**"
    )
    assert "confirm it is still supported" in implement
    assert "report the substitution in the implementation summary" in implement
    assert analyze.index(".specify/memory/codebase-context.md") < analyze.index(
        "### 3. Build Semantic Models"
    )
    assert analyze.index("#### G. Repository Alignment (Optional)") > analyze.index(
        "### 4. Detection Passes"
    )
    assert analyze.index("#### G. Repository Alignment (Optional)") < analyze.index(
        "### 5. Severity Assignment"
    )
    assert "STRICTLY READ-ONLY" in analyze
    assert "MUST NOT exceed MEDIUM" in analyze
    assert "corroborated by current source" in analyze
    assert "Constitution conflicts remain CRITICAL" in analyze


def test_readme_documents_the_external_context_contract():
    readme = (PRESET_DIR / "README.md").read_text(encoding="utf-8")

    assert "`plan`, `tasks`, `analyze`, and `implement`" in readme
    assert "does not generate the file or check" in readme
    assert "another process to create, refresh, and maintain" in readme
    assert "do not inherit" in readme
    assert "future changes" in readme
