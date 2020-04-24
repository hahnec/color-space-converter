#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "info@christopherhahne.de"
__license__ = """
    Copyright (c) 2020 Christopher Hahne <info@christopherhahne.de>

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

import numpy as np

from color_space_converter.hsv_converter import HsvConverter
from color_space_converter.yuv_converter import YuvConverter
from color_space_converter.xyz_converter import XyzConverter
from color_space_converter.lab_converter import LabConverter
from color_space_converter.lms_converter import LmsConverter
from color_space_converter.gry_converter import GryConverter

METHODS = sorted(['gry', 'hsv', 'lab', 'lms', 'xyz', 'yuv'])
FILE_EXTS = ['png', 'jpeg', 'jpg', 'bmp', 'tiff']


def normalize_img(img: np.ndarray = None) -> np.ndarray:
    return np.uint8((img-np.min(img))/(np.max(img)-np.min(img)) * (2**8-1))


class ColorSpaceConverter(LabConverter, LmsConverter, HsvConverter, YuvConverter, XyzConverter, GryConverter):

    def __init__(self, *args, **kwargs):
        super(ColorSpaceConverter, self).__init__(*args, **kwargs)

        self._met = kwargs['method'] if 'method' in kwargs else 'default'
        self._met = 'yuv' if self._met == 'default' else self._met

    def main(self, img: np.ndarray = None, method: str = None, inverse: str = False, standard: str = None) -> np.ndarray:
        """
        The main function and high-level entry point performing the color space conversion. Valid methods are

        :param img: input array in either RGB or xyz color space
        :type img: :class:`~numpy:numpy.ndarray`
        :param method: describing target color space
        :type method: :class:`str`
        :param inverse: option that determines whether conversion is from rgb2yuv (False) or yuv2rgb (True)
        :type inverse: :class:`boolean`
        :param standard: option that determines whether head- and footroom are excluded ('HDTV') or considered otherwise
        :type standard: :class:`string`
        :return: Resulting image after color mapping
        :rtype: np.ndarray
        """

        # override if inputs present
        self._arr = img if img is not None else self._arr
        self._inv = inverse if inverse else self._inv
        self._stn = standard if standard else 'HDTV'
        self._met = method if method is not None else self._met

        # color transfer methods (to be iterated through)
        if self._met == METHODS[0]:
            funs = [self.gry_conv]
        elif self._met == METHODS[1]:
            funs = [self.hsv_conv]
        elif self._met == METHODS[2]:
            funs = [self.lab_conv]
        elif self._met == METHODS[3]:
            funs = [self.lms_conv]
        elif self._met == METHODS[4]:
            funs = [self.xyz_conv]
        elif self._met == METHODS[5]:
            funs = [self.yuv_conv]
        else:
            raise BaseException('Conversion method \'%s\' not recognized' % self._met)

        # proceed with the color conversion
        for fun in funs:
            self._arr = fun(self._arr.astype('float'))

        return self._arr
