project = 'Sundial Protocol'
html_title = 'Sundial Documentation'
html_short_title = 'Sundial Docs'
html_theme = "sphinx_rtd_theme"
# html_show_sourcelink = False

html_context = {
    "display_github": False,  # Turn off default "Edit on GitHub"
}

html_theme_options = {
    "logo_only": False,
    "display_version": False,
    "collapse_navigation": False,
}

html_static_path = ['_static']
html_css_files = ['custom.css']
html_js_files = ['remove-version.js']