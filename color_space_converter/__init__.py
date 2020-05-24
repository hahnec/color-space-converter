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

__version__ = '0.1.4'

from .top_level import ColorSpaceConverter
from .gry_converter import GryConverter, rgb2gry, gry2ch3, gry_conv
from .hsv_converter import HsvConverter, rgb2hsv, hsv2rgb, hsv_conv
from .lab_converter import LabConverter, rgb2lab, lab2rgb, lab_conv
from .lms_converter import LmsConverter, rgb2lms, lms2rgb, lms_conv
from .xyz_converter import XyzConverter, rgb2xyz, xyz2rgb, xyz_conv
from .yuv_converter import YuvConverter, rgb2yuv, yuv2rgb, yuv_conv
from .converter_baseclass import ConverterBaseclass
