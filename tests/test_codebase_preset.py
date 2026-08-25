"""Tests for the local codebase preset."""

from pathlib import Path

from specify_cli.presets import PresetManager, PresetManifest, PresetResolver


PRESET_DIR = Path(__file__).parent.parent / "presets" / "codebase"
CORE_OVERRIDE_COMMAND_NAMES = (
    "speckit.plan",
    "speckit.tasks",
    "speckit.analyze",
    "speckit.implement",
)
GENERATOR_COMMAND_NAME = "speckit.codebase"
OUTPUT_TEMPLATE_NAME = "codebase-template"
ALL_COMMAND_NAMES = (GENERATOR_COMMAND_NAME, *CORE_OVERRIDE_COMMAND_NAMES)
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
    expected_entries = {("command", name) for name in ALL_COMMAND_NAMES}
    expected_entries.add(("template", OUTPUT_TEMPLATE_NAME))

    assert manifest.id == "codebase"
    assert manifest.version == "1.2.0"
    assert manifest.requires_speckit_version == ">=1.0.1"
    assert {
        (entry["type"], entry["name"]) for entry in manifest.templates
    } == expected_entries
    assert all(entry["strategy"] == "replace" for entry in manifest.templates)


def test_replacement_commands_are_complete_english_commands():
    for command_name in CORE_OVERRIDE_COMMAND_NAMES:
        command_file = PRESET_DIR / "commands" / f"{command_name}.md"
        content = command_file.read_text(encoding="utf-8")

        assert ".specify/memory/codebase.md" in content
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

    for command_name in CORE_OVERRIDE_COMMAND_NAMES:
        layers = resolver.collect_all_layers(command_name, "command")
        assert layers[0]["strategy"] == "replace"
        assert layers[-1]["source"] == "core (bundled)"

        content = resolver.resolve_content(command_name, "command")
        assert content is not None
        command_file = PRESET_DIR / "commands" / f"{command_name}.md"
        assert content == command_file.read_text(encoding="utf-8")
        assert CORE_MARKERS[command_name] in content
        assert ".specify/memory/codebase.md" in content
        assert "scripts:" in content


def test_generator_command_is_complete_and_uses_current_backend_contract():
    command_file = PRESET_DIR / "commands" / f"{GENERATOR_COMMAND_NAME}.md"
    content = command_file.read_text(encoding="utf-8")

    assert content.startswith("---\n")
    assert "## User Input" in content
    assert "## Done When" in content
    assert ".specify/memory/codebase.md" in content
    assert "scripts/bash/resolve-template.sh codebase-template --json" in content
    assert (
        "scripts/powershell/resolve-template.ps1 codebase-template -Json"
        in content
    )
    assert "scripts/python/resolve_template.py codebase-template --json" in content
    assert "MCP tools" in content
    assert "codebase-memory-mcp cli --json <tool>" in content
    assert "--mode full" in content
    assert "--persistence false" in content
    assert "check_index_coverage" in content
    assert "include_evidence=true" in content
    assert "Not observed in verified scope" in content
    assert "spring-boot-maven" in content
    assert "one or two meaningful entry points" in content
    assert "stop after five representative traces" in content
    assert "PROJECT OVERRIDES START" in content
    assert "--replace-existing" in content
    assert "codegraph_explore" not in content
    assert "get_architecture(repo_path" not in content
    assert "--adopt-existing" not in content
    assert "`Executed`" not in content
    assert not any("\u4e00" <= char <= "\u9fff" for char in content)


def test_generator_and_output_template_resolve_without_core_layers(tmp_path):
    project_root = tmp_path / "project"
    (project_root / ".specify").mkdir(parents=True)

    manager = PresetManager(project_root)
    manager.install_from_directory(PRESET_DIR, "1.0.1")
    resolver = PresetResolver(project_root)

    command_layers = resolver.collect_all_layers(GENERATOR_COMMAND_NAME, "command")
    assert len(command_layers) == 1
    assert command_layers[0]["strategy"] == "replace"
    assert command_layers[0]["source"] == "codebase v1.2.0"
    assert resolver.resolve_core(GENERATOR_COMMAND_NAME, "command") is None
    assert resolver.resolve_content(GENERATOR_COMMAND_NAME, "command") == (
        PRESET_DIR / "commands" / f"{GENERATOR_COMMAND_NAME}.md"
    ).read_text(encoding="utf-8")

    template_layers = resolver.collect_all_layers(OUTPUT_TEMPLATE_NAME, "template")
    assert len(template_layers) == 1
    assert template_layers[0]["strategy"] == "replace"
    assert template_layers[0]["source"] == "codebase v1.2.0"
    assert resolver.resolve_core(OUTPUT_TEMPLATE_NAME, "template") is None
    assert resolver.resolve_content(OUTPUT_TEMPLATE_NAME, "template") == (
        PRESET_DIR / "templates" / f"{OUTPUT_TEMPLATE_NAME}.md"
    ).read_text(encoding="utf-8")


def test_output_template_has_stable_schema_and_override_markers():
    template = (
        PRESET_DIR / "templates" / f"{OUTPUT_TEMPLATE_NAME}.md"
    ).read_text(encoding="utf-8")

    assert template.startswith("---\n")
    assert 'schema_version: "1.0"' in template
    assert 'generator: "speckit.codebase"' in template
    assert 'evidence_tier: "verify"' in template
    for section_number in range(1, 15):
        assert f"## {section_number}." in template
    assert template.count("<!-- PROJECT OVERRIDES START -->") == 1
    assert template.count("<!-- PROJECT OVERRIDES END -->") == 1
    assert template.index("<!-- PROJECT OVERRIDES START -->") < template.index(
        "<!-- PROJECT OVERRIDES END -->"
    )
    assert not any("\u4e00" <= char <= "\u9fff" for char in template)


def test_codebase_rules_are_embedded_in_the_original_workflow_positions():
    plan = (PRESET_DIR / "commands" / "speckit.plan.md").read_text(encoding="utf-8")
    tasks = (PRESET_DIR / "commands" / "speckit.tasks.md").read_text(encoding="utf-8")
    implement = (PRESET_DIR / "commands" / "speckit.implement.md").read_text(
        encoding="utf-8"
    )
    analyze = (PRESET_DIR / "commands" / "speckit.analyze.md").read_text(
        encoding="utf-8"
    )

    assert plan.index(".specify/memory/codebase.md") < plan.index(
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
    assert tasks.index(".specify/memory/codebase.md") < tasks.index(
        "## Mandatory Post-Execution Hooks"
    )
    assert "repository, mapper, ORM, schema-registration" in tasks
    assert "migration, compatibility, and validation tasks" in tasks
    assert implement.index(".specify/memory/codebase.md") < implement.index(
        "4. **Project Setup Verification**"
    )
    assert "confirm it is still supported" in implement
    assert "report the substitution in the implementation summary" in implement
    assert analyze.index(".specify/memory/codebase.md") < analyze.index(
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


def test_readme_documents_generator_and_context_contract():
    readme = (PRESET_DIR / "README.md").read_text(encoding="utf-8")

    assert "one standalone generator command" in readme
    assert "`speckit.codebase`" in readme
    assert "Spring Boot Maven profile" in readme
    assert "Project Overrides" in readme
    assert "`--replace-existing`" in readme
    assert "There is no\nautomatic adopt mode" in readme
    assert "does not execute them" in readme
    assert "another process to create, refresh, and maintain" not in readme
    assert "do not inherit" in readme
    assert "future changes" in readme
