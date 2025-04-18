import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath("../.."))

# Set Django settings module
os.environ["DJANGO_SETTINGS_MODULE"] = "HutBazaar.settings"

# Ensure Django can find the settings without needing a full server context
try:
    from django.conf import settings
    import django

    django.setup()
except Exception as e:
    print(f"Warning: Could not initialize Django: {e}")
    # Proceed without Django setup if it fails (views without models might still work)

# Project information
project = "HutBazaar"
copyright = "2025, Jim"
author = "Jim"
release = "1.0.0"

# Extensions
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_design",
    "sphinx_autodoc_typehints",  # Optional
]

# Theme
html_theme = "sphinx_rtd_theme"

# Paths
templates_path = ["_templates"]
exclude_patterns = []

# Autodoc settings
autoclass_content = "both"
autodoc_member_order = "bysource"
