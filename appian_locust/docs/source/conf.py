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

html_favicon = '../assets/Appian_Locust_FINAL_NAVY_CIRCLE_Reversed.svg'
html_logo = '../assets/Appian_Locust_FINAL_NAVY_CIRCLE_Reversed.svg'
html_static_path = ['_static']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_api/core']

autodoc_default_flags = ['members', 'private-members', 'undoc-members', 'inherited-members', 'show-inheritance']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'


def setup(app):
    app.add_css_file("custom_style.css")

# Iterate through appian-locust classes to generate a list of exposed and internal APIs


def init_path(dir: str) -> Path:
    path = Path(dir)
    path.mkdir(parents=True, exist_ok=True)
    [os.remove(f'{dir}/{f}') for f in os.listdir(dir)]
    return path


def get_project_subdir_array(subdir: str) -> [str]:
    match = re.match('.*/(appian_locust.*)', subdir)
    if not match:
        raise Exception('Unable to locate appian_locust subfolder...')
    return match.group(1).split('/')


def insert_header(header: str, output_file: str):
    with open(output_file, 'w') as stream:
        stream.write(dedent(f"""\
            {''.join(itertools.repeat('=', len(header)))}
            {header}
            {''.join(itertools.repeat('=', len(header)))}
        """))


def write_automodule(
    subdir_array: [str],
    module_name: str,
    output_dir: Path,
    show_private: bool = False
) -> None:
    is_submodule = len(subdir_array) > 1
    file_name = f'{"_" if show_private else ""}{subdir_array[-1]}.rst'
    output_file = f'{output_dir}/{"modules" if is_submodule else "core"}/{file_name}'
    if not os.path.exists(output_file) and is_submodule:
        header = f"**{subdir_array[-1].capitalize()} module**"
        insert_header(header, output_file)
    with open(output_file, 'a') as stream:
        stream.write(dedent(f"""
            .. automodule:: {'.'.join(subdir_array)}.{module_name}
                :members:
                :undoc-members:
                :show-inheritance:
                {':private-members:' if show_private else ''}
        """))


appian_locust_dir = os.path.abspath(f'{os.path.dirname(__file__)}/../..')
init_path('./_api/modules')
init_path('./_api/core')
api_dir = Path('./_api')

for subdir, dirs, files in os.walk(appian_locust_dir):
    appian_locust_subdir = get_project_subdir_array(subdir)
    if 'docs' in appian_locust_subdir:
        continue
    files.sort()
    for f in files:
        match = re.match('^((_?)[^_].+)\.py$', f)
        if match:
            write_automodule(
                output_dir=api_dir,
                subdir_array=appian_locust_subdir,
                module_name=match.group(1),
                show_private=bool(match.group(2)),
            )
