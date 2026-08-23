"""Tests for the local codebase-context preset."""

from pathlib import Path

from specify_cli.presets import PresetManager, PresetManifest, PresetResolver


PRESET_DIR = Path(__file__).parent.parent / "presets" / "codebase-context"
COMMAND_NAMES = ("speckit.plan", "speckit.tasks", "speckit.implement")
CORE_MARKERS = {
    "speckit.plan": "## Mandatory Post-Execution Hooks",
    "speckit.tasks": "## Task Generation Rules",
    "speckit.implement": "## Mandatory Post-Execution Hooks",
}


def test_manifest_declares_replace_layers():
    manifest = PresetManifest(PRESET_DIR / "preset.yml")

    assert manifest.id == "codebase-context"
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
        assert "## Done When" in content
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

    assert plan.index(".specify/memory/codebase-context.md") < plan.index(
        "## Mandatory Post-Execution Hooks"
    )
    assert plan.index("Prefer an available code graph") > plan.index(
        "### Phase 0: Outline & Research"
    )
    assert plan.index("entity base classes and primary-key strategies") > plan.index(
        "### Phase 1: Design & Contracts"
    )
    assert tasks.index(".specify/memory/codebase-context.md") < tasks.index(
        "## Mandatory Post-Execution Hooks"
    )
    assert implement.index(".specify/memory/codebase-context.md") < implement.index(
        "4. **Project Setup Verification**"
    )
