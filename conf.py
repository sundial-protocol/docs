# Project name (can be left blank or used for internal reference)
project = ""

# Sets the full title of the documentation in the browser/tab header
html_title = "Sundial Protocol Documentation"

# Sets the shorter version of the title, used in the sidebar
html_short_title = "Sundial Docs"

# Selects the theme used for HTML output – in this case, Read the Docs theme
html_theme = "sphinx_rtd_theme"

# Optionally hide "View page source" links (currently commented out)
# html_show_sourcelink = False

# Context settings passed to the HTML templates
html_context = {
    "display_github": False,  # Disables the "Edit on GitHub" button in the top-right
}

# Options specific to the selected theme
html_theme_options = {
    'logo_only': True,         # Show only the logo, not the project name
    'display_version': False,  # Hide the version number in the header
}

# Path to static assets (e.g. images, CSS files)
html_static_path = ['_static']

# Custom CSS file to override theme styles (must be in _static/)
html_css_files = ['custom.css']
