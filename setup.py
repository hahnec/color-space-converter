#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
    Copyright (c) 2020 Christopher Hahne <inbox@christopherhahne.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from setuptools import setup, find_packages
from color_space_converter import __version__
from sys import platform
from docutils import core
import os

APP = ['color_space_converter/bin/cli.py']

FILES = [
        # ('subdir' , ['file_path'])
]

OPTIONS = {
    "argv_emulation": True,
    "compressed": True,
    "optimize": 2,
    "iconfile": '',
    "excludes": ['matplotlib'],
    "plist": dict(NSHumanReadableCopyright='2020 Christopher Hahne'),
    "packages": ['numpy', 'docutils'],
}

if platform == 'darwin':
    extra_options = dict(
        setup_requires=[],
        data_files=FILES,
    )
elif platform == 'win32':
    extra_options = dict(
        setup_requires=[],
        data_files=FILES,
    )
else:
    extra_options = dict(
        setup_requires=[],
        data_files=FILES,
 )

# parse description section text
readme_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'README.rst')
with open(readme_path, "r") as f:
    data = f.read()
    readme_nodes = list(core.publish_doctree(data))
    for node in readme_nodes:
        if node.astext().startswith('Description'):
                long_description = node.astext().rsplit('\n\n')[1]

setup(
      name='color-space-converter',
      version=__version__,
      description='Package enabling color space conversion',
      long_description=long_description,
      long_description_content_type='text/x-rst',
      url='http://github.com/hahnec/color-space-converter',
      author='Christopher Hahne',
      author_email='inbox@christopherhahne.de',
      license='GNU GPL V3.0',
      keywords='color space model converter conversion rgb hsv yuv xyz lab lms cnn pytorch tensorflow',
      scripts=['color_space_converter/bin/cli.py'],
      entry_points={'console_scripts': ['color-space-converter=color_space_converter.bin.cli:main'], },
      packages=find_packages(),
      install_requires=['numpy', 'imageio', 'docutils', 'ddt'],
      include_package_data=True,
      python_requires='>=3',
      zip_safe=False,
      **extra_options
      )
