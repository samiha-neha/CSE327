import os
import sys
sys.path.insert(0, os.path.abspath('../HutBazaar'))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HutBazaar.settings')

import django
django.setup()
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'HutBazaar'
copyright = '2025, Samiha Islam Neha, Md. Sakibul Alam Patwary, Fahmida Amy Prattasha, Maria Chowdhury Prianka, Rejmin Islam'
author = 'Samiha Islam Neha, Md. Sakibul Alam Patwary, Fahmida Amy Prattasha, Maria Chowdhury Prianka, Rejmin Islam'
release = '20 April 2025'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx.ext.viewcode',
    ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
