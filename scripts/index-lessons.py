
"""Simple indexer to generate Docusaurus sidebar entries from lessons."""
import os, json, pathlib

BASE = pathlib.Path(__file__).resolve().parents[1]
lessons_dir = BASE / "docs" / "lessons"
sidebar_path = BASE / "ui" / "docs-ui" / "sidebars.json"

tree = {"docs": []}
for file in sorted(lessons_dir.glob("*.md")):
    tree["docs"].append(str(file.relative_to(BASE)))
sidebar_path.parent.mkdir(parents=True, exist_ok=True)
sidebar_path.write_text(json.dumps(tree, indent=2))
print("Sidebar updated with", len(tree["docs"]), "lessons.")
