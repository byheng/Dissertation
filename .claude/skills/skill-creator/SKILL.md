---
name: "skill-creator"
description: "Expert guidance for creating Claude Code skills and slash commands. Use when working with SKILL.md files, agents, and local development of skills."
---

# Skill Creator

Provides guidance for creating effective skills that extend Claude with specialized knowledge or workflows.

## Core Requirements

Every skill requires a `SKILL.md` file featuring:
- **YAML Frontmatter**: Includes `name` and `description` to help Claude understand when to invoke the skill.
- **Clear Instructions**: Use imperative form and objective language to define the skill's behavior.

## Directory Structure

- `SKILL.md`: Root configuration and main instructions (Mandatory).
- `scripts/`: Executable code for deterministic operations.
- `references/`: Supplemental documentation or large datasets to keep context lean.
- `assets/`: Templates, icons, or static files.

## Development Workflow

1. **Initialize**: Create the skill directory and frontmatter.
2. **Draft Instructions**: Define the primary workflow in `SKILL.md`.
3. **Externalize Knowledge**: Move specific details or long docs to the `references/` folder.
4. **Iterate**: Test the skill by interacting with Claude in the repo.

Follow the Progressive Disclosure Design Principle: Metadata and high-level instructions first, detailed resources only when needed.
