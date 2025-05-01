import os

project = 'Sundial'
html_title = "Sundial Documentation"
copyright = '2025'
author = 'Sundial Team'

extensions = [
    'sphinx.ext.mathjax',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'furo'

html_theme_options = {
    "light_logo": "sundial_logo.png",
    "dark_logo": "sundial_logo.png",
}

html_static_path = ['_static']
html_css_files = ['custom.css']
