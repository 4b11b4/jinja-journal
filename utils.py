import os
import re
import datetime
import markdown
import subprocess
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


def get_git_dates(filepath):
    """Get creation and modification dates from git history."""
    try:
        # Get the first commit date (creation date)
        creation_cmd = [
            "git",
            "log",
            "--follow",
            "--format=%ad",
            "--date=iso",
            "--reverse",
            filepath,
        ]
        creation_date_str = (
            subprocess.check_output(creation_cmd, text=True).strip().split("\n")[0]
        )
        creation_date = datetime.datetime.fromisoformat(
            creation_date_str.replace(" ", "T").replace(" -", "-")
        )

        # Get the last commit date (modification date)
        modified_cmd = ["git", "log", "-1", "--format=%ad", "--date=iso", filepath]
        modified_date_str = subprocess.check_output(modified_cmd, text=True).strip()
        modified_date = datetime.datetime.fromisoformat(
            modified_date_str.replace(" ", "T").replace(" -", "-")
        )

        return {
            "created": creation_date.strftime("%Y-%m-%d"),
            "modified": modified_date.strftime("%Y-%m-%d"),
        }
    except (subprocess.SubprocessError, IndexError):
        # Fallback to file system dates if git command fails
        modified_time = os.path.getmtime(filepath)
        modified_date = datetime.datetime.fromtimestamp(modified_time).strftime(
            "%Y-%m-%d"
        )
        # Since we can't get creation from file system easily, use the same date
        return {"created": modified_date, "modified": modified_date}


def get_entry_metadata(filepath):
    """Extract metadata from an entry file."""
    filename = os.path.basename(filepath)
    title = title_from_filename(filename)

    # Get dates from git history
    dates = get_git_dates(filepath)

    return {
        "title": title,
        "created_date": dates["created"],
        "modified_date": dates["modified"],
        "slug": slugify(title),
        "filepath": filepath,
    }


def get_all_entries(entries_dir):
    """Get metadata for all entries in the directory."""
    entries = []
    for filename in os.listdir(entries_dir):
        filepath = os.path.join(entries_dir, filename)
        if os.path.isfile(filepath) and (
            filename.endswith(".md") or filename.endswith(".html")
        ):
            entries.append(get_entry_metadata(filepath))

    # Sort by modified date, newest first
    return sorted(entries, key=lambda x: x["modified_date"], reverse=True)


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
