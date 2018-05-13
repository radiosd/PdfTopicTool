#!usr/bin/env python
"""
    Deployment of commands for the PdfLibrary
                                                    rgr14may18
"""

from distutils.core import setup

setup(name='rgrPdfLibrary',
      version='1.2.1',
      description='command line interface to the topic FindAdex database',
      author='Radio System Design Ltd',
      scripts=['plib-topic.py'],
      packages=['rgrPdfLibrary']
      )
