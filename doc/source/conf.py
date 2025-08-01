#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# KIWI NG documentation build configuration file
#
import sys
from os.path import abspath, dirname, join, normpath
import shlex
import sphinx_rtd_theme

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
_path = normpath(join(dirname(__file__), "../.."))
sys.path.insert(0, _path)


# -- General configuration ------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.extlinks',
    'sphinx.ext.todo',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.autodoc',
    'sphinx_rtd_theme'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['.templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

default_role="py:obj"

# General information about the project.
project = 'KIWI - Boxed Build Plugin'
copyright = '2020, Marcus Schäfer'
author = 'Marcus Schäfer'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '0.2.55'
# The full version, including alpha/beta/rc tags.
release = version

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

autosummary_generate = True

# -- Options for HTML output ----------------------------------------------

html_sidebars = {
   '**': [
          'localtoc.html', 'relations.html',
          'about.html', 'searchbox.html',
         ]
}

html_theme = "sphinx_rtd_theme"

# html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_theme_options = {
    'collapse_navigation': False,
    'display_version': False
}

# -- Options for manual page output ---------------------------------------

# The man page toctree documents.
system_boxbuild_doc = 'commands/system_boxbuild'

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (
        system_boxbuild_doc,
        'kiwi::system::boxbuild',
        'Self Contained Image Build',
        [author],
        8
    )
]

intersphinx_mapping = {'python': ('https://docs.python.org/3', None)}
