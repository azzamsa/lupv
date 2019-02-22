import os
import sys

sys.path.insert(0, os.path.abspath('../lupv'))

extensions = [
    'sphinx.ext.autodoc',
]

project = 'Lupv'
copyright = '2019, Azzam S.A'
author = 'Azzam S.A'
version = ''
release = '1.1'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_static_path = ['_static']
