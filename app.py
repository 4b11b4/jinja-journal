import os
import shutil
from pathlib import Path
from utils import get_all_entries, read_entry_content, render_template


def ensure_dir(directory):
    """Ensure a directory exists, creating it if necessary."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def main():
    # Configuration
    entries_dir = "entries"
    templates_dir = "templates"
    output_dir = "output"

    # Ensure output directory exists
    ensure_dir(output_dir)

    # Get all entries
    entries = get_all_entries(entries_dir)

    # Generate index page
    render_template(
        "index.html",
        {"entries": entries, "title": "Jinja Journal"},
        os.path.join(output_dir, "index.html"),
    )

    # Generate individual entry pages
    for entry in entries:
        content = read_entry_content(entry["filepath"])
        render_template(
            "entry.html",
            {"entry": entry, "content": content, "title": entry["title"]},
            os.path.join(output_dir, f"{entry['slug']}.html"),
        )

    print(f"Generated site with {len(entries)} entries in {output_dir}/")


if __name__ == "__main__":
    main()
