# -*- coding: utf-8 -*-

import sys
from cx_Freeze import setup, Executable

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable(
        script='import_pdf_into_styluslab.py',
        icon='icon.ico',
        base=base
    )
]
includefiles = ['icon.ico']

setup(name='Import PDF into StylusLab Write',
      version='1.0',
      description='Convert PDF documents to HTML/SVG',
      executables=executables,
      options = {'build_exe': {'include_files':includefiles}}
      )
