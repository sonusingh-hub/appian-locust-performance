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
def init_path(dir: str) -> Path:
    path = Path(dir)
    path.mkdir(parents=True, exist_ok=True)
    [os.remove(f'{dir}/{f}') for f in os.listdir(dir)]
    return path

def write_automodule(
    subdir: str,
    module_name: str,
    output: Path,
    show_private: bool = False
) -> None:
    subdir_name = f'{subdir.split("/")[-1]}{"_private" if show_private else ""}'
    output_file = f'{output}/{subdir_name}.rst'
    if not os.path.exists(output_file):
        with open(output_file, 'w') as stream:
            stream.write(dedent(f"""\
                {''.join(itertools.repeat('=', len(subdir_name)))}
                {subdir_name}
                {''.join(itertools.repeat('=', len(subdir_name)))}
            """))
    with open(output_file, 'a') as stream:
        stream.write(dedent(f"""
            .. automodule:: {subdir.replace('/', '.')}.{module_name}
                :members:
                :undoc-members:
                :show-inheritance:
                {':private-members:' if show_private else ''}
        """))

appian_locust_dir = os.path.abspath(f'{os.path.dirname(__file__)}/../..')
exposed_dir = init_path('./_api/exposed')
internal_dir = init_path('./_api/internal')

for subdir, dirs, files in os.walk(appian_locust_dir):
    appian_locust_subdir = subdir.split('appian-locust/')[-1]
    parent_dir = appian_locust_subdir.split('/')[-1]
    if re.match('^__.+', parent_dir) or 'docs' in subdir:
        continue
    for f in files:
        match = re.match('^([^_].+)\.py$', f)
        if match:
            write_automodule(
                output=exposed_dir,
                module_name=match.group(1),
                subdir=appian_locust_subdir,
            )
            continue
        match = re.match('^(_[^_].+)\.py$', f)
        if match:
            write_automodule(
                output=internal_dir,
                module_name=match.group(1),
                subdir=appian_locust_subdir,
                show_private=True,
            )
