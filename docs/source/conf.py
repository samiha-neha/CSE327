# conf.py

import os
import sys
import django

# Calculate the path to the project root (where manage.py is)
# This assumes conf.py is in docs/source/
# Correct - points to the hutbazaar folder inside CSE327
project_root = os.path.abspath('../../Hutbazaar') # Add '/Hutbazaar'
sys.path.insert(0, project_root)

# Print the path to verify (optional, but helpful for debugging)
print(f"Adding to sys.path: {project_root}")
print(f"Current sys.path: {sys.path}")

# Set the Django settings module environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'HutBazaar.settings'

# Setup Django
django.setup()

# docs/source/conf.py

# ... other settings ...

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',  # <--- ADD THIS LINE (or make sure it's uncommented)
    # Add other useful extensions below if needed:
    'sphinx.ext.napoleon',  # If using Google/NumPy style docstrings
    'sphinx.ext.viewcode',  # Adds links to source code in docs
    'sphinx.ext.intersphinx', # For linking to Python/Django docs
]

# (Optional but recommended for intersphinx)
# intersphinx_mapping = {'python': ('https://docs.python.org/3', None),
#                       'django': ('https://docs.djangoproject.com/en/stable/', 'https://docs.djangoproject.com/en/stable/_objects/')}


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# ... rest of the file ...