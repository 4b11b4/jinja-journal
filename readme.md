# Jinja Journal

A starting point for a site gen
at least using Jinja...

A simple static site generator using Jinja2 templates to convert markdown or HTML entries into a static website.

## Run It

### Quick Start

To set up an environment and run it:

  ```
  ./start.sh
  ```

## Background

### Structure
   - `entries/`: written entries in HTML (.html) or Markdown (.md) 
   - `templates/`: template for entry page & main page
   - `output/`: generated website files


## How It Works

The application:
1. Scans all files in the `entries/` directory
2. Generates a title from each filename (converting hyphenated names to title case)
3. Uses the file's last modified date as the entry date
4. Generates an index page listing all entries
5. Generates individual HTML pages for each entry
6. Outputs all files to the `output/` directory

## File Naming Convention

File names should use hyphenated format, which will be converted to title case in the output:
- `my-first-post.md` → "My First Post"
- `another-example-entry.html` → "Another Example Entry"

## Templates

The application uses two templates:
- `index.html`: For the main index page listing all entries
- `entry.html`: For individual entry pages

## Deployment

### GitHub Pages Deployment

This project is configured to automatically build and deploy to GitHub Pages using GitHub Actions. Here's how it works:

1. Push your changes to the main branch
2. GitHub Actions automatically:
   - Sets up a Python environment
   - Installs the required dependencies
   - Builds the site by running app.py
   - Deploys the generated files to the gh-pages branch

3. Your site will be available at:
   ```
   https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/
   ```

#### First-time setup:

After pushing your code with the workflow file:
1. Go to your repository on GitHub
2. Navigate to Settings > Pages
3. Under "Source", select the "gh-pages" branch and the "/" (root) folder
4. Click "Save"

The GitHub Action will handle rebuilding and deploying your site whenever you push new changes or add new entries.