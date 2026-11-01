from pathlib import Path

import yaml

SKILL_DIRS = [
    Path.cwd() / ".agents" / "skills",
    Path.home() / ".agents" / "skills",
]


def find_skills():
    """Map each skill name to its description and SKILL.md path"""
    skills = {}
    for dir in SKILL_DIRS:
        if not dir.exists():
            continue
        paths = sorted(set(dir.glob("*/SKILL.md")) | set(dir.glob("SKILL.md")))
        for path in paths:
            try:
                _, frontmatter, _ = path.read_text().split("---", 2)
                meta = yaml.safe_load(frontmatter)
                description = " ".join(meta["description"].split())
                skills[meta["name"]] = {"description": description, "path": path}
            except Exception as e:
                print(f"Warning: Failed to load skill from {path}: {e}")

    return skills


SKILLS = find_skills()


def skills_prompt():
    return "\n".join(f"- {name}: {s['description']}" for name, s in SKILLS.items())


def read_skill(name: str) -> str:
    """Open a skill and return its full instructions."""
    if name not in SKILLS:
        return f"No skill named '{name}'"
    return SKILLS[name]["path"].read_text()


if __name__ == "__main__":
    print(skills_prompt())