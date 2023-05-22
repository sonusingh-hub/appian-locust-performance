# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import re
import itertools
from pathlib import Path
from textwrap import dedent
sys.path.insert(0, os.path.abspath('../../..'))


# -- Project information -----------------------------------------------------

project = 'Appian-Locust (Appian-Locust)'
copyright = '2020, Appian Corporation'
author = 'Appian Corporation'

# The full version, including alpha/beta/rc tags
release = 'latest'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.napoleon', 'sphinx.ext.autosectionlabel']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

html_favicon = 'favicon-32x32.png'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

autodoc_default_flags = ['members', 'private-members', 'undoc-members', 'inherited-members', 'show-inheritance']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Iterate through appian-locust classes to generate a list of exposed and internal APIs
appian_locust_dir = '../..'
exposed_dir = Path('./_api/exposed')
internal_dir = Path('./_api/internal')
exposed_dir.mkdir(parents=True, exist_ok=True)
internal_dir.mkdir(parents=True, exist_ok=True)


def write_automodule(name: str, folder: Path, show_private: bool = False) -> None:
    with open(f'{folder}/{name}.rst', 'w') as stream:
        stream.write(dedent(f"""\
            {name}
            {''.join(itertools.repeat('=', len(name)))}

            .. automodule:: appian_locust.{name}
                :members:
                :undoc-members:
                :show-inheritance:
                {':private-members:' if show_private else ''}
        """))


for f in os.listdir(appian_locust_dir):
    match = re.match('^([^_].+)\.py$', f)
    if match:
        write_automodule(
            name=match.group(1),
            folder=exposed_dir,
        )
        continue
    match = re.match('^(_[^_].+)\.py$', f)
    if match:
        write_automodule(
            name=match.group(1),
            folder=internal_dir,
            show_private=True,
        )
