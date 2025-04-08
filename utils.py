import os
import re
import datetime
import markdown
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


def slugify(title):
    """Convert a filename to a URL slug."""
    return title.lower().replace(" ", "-")


def title_from_filename(filename):
    """Extract title from filename format like 'a-title-name'."""
    # Remove extension
    basename = os.path.splitext(os.path.basename(filename))[0]
    # Convert hyphens to spaces and capitalize each word
    return " ".join(word.capitalize() for word in basename.split("-"))


def get_entry_metadata(filepath):
    """Extract metadata from an entry file."""
    filename = os.path.basename(filepath)
    title = title_from_filename(filename)

    # Get last modified time
    modified_time = os.path.getmtime(filepath)
    date = datetime.datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d")

    return {"title": title, "date": date, "slug": slugify(title), "filepath": filepath}


def get_all_entries(entries_dir):
    """Get metadata for all entries in the directory."""
    entries = []
    for filename in os.listdir(entries_dir):
        filepath = os.path.join(entries_dir, filename)
        if os.path.isfile(filepath) and (
            filename.endswith(".md") or filename.endswith(".html")
        ):
            entries.append(get_entry_metadata(filepath))

    # Sort by date, newest first
    return sorted(entries, key=lambda x: x["date"], reverse=True)


def read_entry_content(filepath):
    """Read and process the content of an entry file."""
    with open(filepath, "r") as f:
        content = f.read()

    # Convert markdown to HTML if needed
    if filepath.endswith(".md"):
        content = markdown.markdown(content)

    return content


def render_template(template_name, context, output_path):
    """Render a template with given context and write to output file."""
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template(template_name)
    html = template.render(**context)

    with open(output_path, "w") as f:
        f.write(html)
