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

        # Parse the date string safely
        creation_date = parse_git_date(creation_date_str)

        # Get the last commit date (modification date)
        modified_cmd = ["git", "log", "-1", "--format=%ad", "--date=iso", filepath]
        modified_date_str = subprocess.check_output(modified_cmd, text=True).strip()

        # Parse the date string safely
        modified_date = parse_git_date(modified_date_str)

        return {
            "created": creation_date.strftime("%Y-%m-%d"),
            "modified": modified_date.strftime("%Y-%m-%d"),
        }
    except (subprocess.SubprocessError, IndexError, ValueError) as e:
        print(f"Warning: Could not get git dates for {filepath}: {e}")
        # Fallback to file system dates if git command fails
        modified_time = os.path.getmtime(filepath)
        modified_date = datetime.datetime.fromtimestamp(modified_time).strftime(
            "%Y-%m-%d"
        )
        # Since we can't get creation from file system easily, use the same date
        return {"created": modified_date, "modified": modified_date}


def parse_git_date(date_str):
    """Parse git date string into datetime object."""
    # Git date format is usually: "2023-04-07 19:21:02 -0700"
    try:
        # Try to directly parse with datetime
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S %z")
    except ValueError:
        try:
            # If that fails, try to manually format the string to ISO format
            # First split the string into components
            date_parts = date_str.split(" ")
            if len(date_parts) >= 3:
                date = date_parts[0]
                time = date_parts[1]
                timezone = date_parts[2]

                # Format into proper ISO format
                iso_format = f"{date}T{time}{timezone}"
                return datetime.datetime.fromisoformat(iso_format)
            else:
                raise ValueError(f"Could not parse date string: {date_str}")
        except Exception as e:
            print(f"Error parsing date: {date_str}, error: {e}")
            # Last resort: just use current time
            return datetime.datetime.now()


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
