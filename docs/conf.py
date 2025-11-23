# Sphinx configuration for SmartKDB

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'SmartKDB'
copyright = '2024, Alhdrawi'
author = 'Alhdrawi'
release = '5.0.3'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'myst_parser',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Options for HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# MyST parser configuration
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
