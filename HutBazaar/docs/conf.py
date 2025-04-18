# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# --- Django Setup (MUST be at the top!) ---
import os
import sys
import django

# Clear and set absolute paths
sys.path = [
    # Project root (manage.py location)
    '/Users/prottasha/Documents/CSE327/HutBazaar',
    
    # Django project (settings.py location)
    '/Users/prottasha/Documents/CSE327/HutBazaar/HutBazaar',
    
    # Keep Python packages
    *[p for p in sys.path if 'site-packages' in p]
]

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HutBazaar.settings')
django.setup()

# Verify configuration
from django.conf import settings
assert settings.BASE_DIR == '/Users/prottasha/Documents/CSE327/HutBazaar', "Path mismatch!"

# -- Project information -----------------------------------------------------
project = 'HutBazaar'
copyright = '2025, Fahmida'
author = 'Fahmida'
release = '0.1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.autosummary'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']