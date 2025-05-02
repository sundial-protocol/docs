html_theme = "sphinx_rtd_theme"

html_context = {
    "display_github": False,  # Turn off default "Edit on GitHub"
}

html_theme_options = {
    'logo_only': True,
    'display_version': False,
}

html_static_path = ['_static']
html_css_files = ['custom.css']
html_js_files = ['toggle-theme.js']
# templates_path = ['_templates']