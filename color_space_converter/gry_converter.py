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

import numpy as np

from color_space_converter.converter_baseclass import ConverterBaseclass

MAT_GRY_HDTV = np.array([0.2126, 0.7152, 0.0722])
MAT_GRY_SDTV = np.array([0.299, 0.587, 0.114])


class GryConverter(ConverterBaseclass):

    def __init__(self, *args, **kwargs):
        super(GryConverter, self).__init__(*args, **kwargs)

    def gry_conv(self, img: np.ndarray = None, inverse: bool = False) -> np.ndarray:
        """ Convert RGB color space to monochromatic color space or to 3-channel array given the inverse option.

        :param img: input array in either RGB or monochromatic color space
        :type img: :class:`~numpy:numpy.ndarray`
        :param inverse: option that determines whether conversion is from rgb2gry (False) or gry2ch3 (True)
        :type inverse: :class:`boolean`
        :return: color space converted array
        :rtype: ~numpy:np.ndarray

        """

        # override if inputs present
        self._arr = img if img is not None else self._arr
        self._inv = inverse if inverse else self._inv

        if not self._inv:
            self._arr = rgb2gry(self._arr)
        else:
            self._arr = gry2ch3(self._arr)

        return self._arr


def rgb2gry(rgb: np.ndarray = None, standard: str = 'HDTV') -> np.ndarray:
    """ Convert RGB color space to monochromatic color space

    :param rgb: input array in red, green and blue (RGB) space
    :type rgb: :class:`~numpy:numpy.ndarray`
    :param standard: option that determines whether head- and footroom are excluded ('HDTV') or considered otherwise
    :type standard: :class:`string`
    :return: array in monochromatic space
    :rtype: ~numpy:np.ndarray

    """

    # store shape
    shape = rgb.shape

    # reshape image to channel vectors
    rgb = rgb.reshape(-1, 3).T

    # choose standard
    mat = MAT_GRY_HDTV if standard == 'HDTV' else MAT_GRY_SDTV

    # convert to gray
    arr = np.dot(mat, rgb)

    # reshape to 2-D image
    arr = arr.reshape(shape[:2] + (1,))

    return arr


def gry2ch3(gry: np.ndarray = None) -> np.ndarray:
    """ Convert monochromatic color space to 3-channel array

    :param gry: input array in monochromatic space
    :type gry: :class:`~numpy:numpy.ndarray`
    :return: array in red, green and blue (RGB) space
    :rtype: ~numpy:np.ndarray

    """

    return np.repeat(gry, repeats=3, axis=2)


def gry_conv(img: np.ndarray = None, inverse: bool = False) -> np.ndarray:
    """ Convert RGB color space to monochromatic color space or to 3-channel array given the inverse option.

    :param img: input array in either RGB or monochromatic color space
    :type img: :class:`~numpy:numpy.ndarray`
    :param inverse: option that determines whether conversion is from rgb2gry (False) or gry2ch3 (True)
    :type inverse: :class:`boolean`
    :return: color space converted array
    :rtype: ~numpy:np.ndarray

    """

    if not inverse:
        arr = rgb2gry(img)
    else:
        arr = gry2ch3(img)

    return arr
