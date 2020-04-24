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
from color_space_converter.xyz_converter import XyzConverter, rgb2xyz, xyz2rgb

MAT_LMS = np.array([[0.38971, 0.68898, -0.07868], [-0.22981, 1.18340, 0.04641], [0, 0, 1]])

# normalized to D65
MAT_LMS_NORM = np.array([[0.4002, -0.2263, 0], [0.7076, 1.1653, 0], [-0.0808, 0, 0.9182]])


class LmsConverter(XyzConverter, ConverterBaseclass):

    def __init__(self, *args, **kwargs):
        super(LmsConverter, self).__init__(*args, **kwargs)

    def lms_conv(self, img: np.ndarray = None, inverse: bool = False) -> np.ndarray:
        """ Convert RGB color space to LMS color space or vice versa given the inverse option.

        :param img: input array in either RGB or HSV color space
        :type img: :class:`~numpy:numpy.ndarray`
        :param inverse: option that determines whether conversion is from rgb2hsv (False) or hsv2rgb (True)
        :type inverse: :class:`boolean`
        :return: color space converted array
        :rtype: ~numpy:np.ndarray

        """

        # override if inputs present
        self._arr = img if img is not None else self._arr
        self._inv = inverse if inverse else self._inv

        if not self._inv:
            self._arr = rgb2lms(self._arr)
        else:
            self._arr = lms2rgb(self._arr)

        return self._arr


def rgb2lms(rgb: np.ndarray = None) -> np.ndarray:
    """ Convert RGB color space to LMS color space

    :param rgb: input array in red, green and blue (RGB) space
    :type rgb: :class:`~numpy:numpy.ndarray`
    :return: array in long, medium and short (LMS) space
    :rtype: ~numpy:np.ndarray

    """

    # store shape
    shape = rgb.shape

    # convert to xyz space
    xyz = rgb2xyz(rgb)

    # reshape image to channel vectors
    xyz = xyz.reshape(-1, 3).T

    # convert to lms space
    lms = np.dot(MAT_LMS, xyz)

    # reshape to 2-D image
    lms = lms.T.reshape(shape)

    return lms


def lms2rgb(lms: np.ndarray = None) -> np.ndarray:
    """ Convert HSV color space to RGB color space

    :param lms: input array in long, medium and short (LMS) space
    :type lms: :class:`~numpy:numpy.ndarray`
    :return: array in red, green and blue (RGB) space
    :rtype: ~numpy:np.ndarray

    """

    # store shape
    shape = lms.shape

    # reshape image to channel vectors
    lms = lms.reshape(-1, 3).T

    # convert to xyz space
    xyz = np.dot(np.linalg.inv(MAT_LMS), lms)

    # reshape to 2-D image
    xyz = xyz.T.reshape(shape)

    # convert to rgb space
    rgb = xyz2rgb(xyz)

    return rgb


def lms_conv(img: np.ndarray = None, inverse: bool = False) -> np.ndarray:
    """ Convert RGB color space to LMS color space or vice versa given the inverse option.

    :param img: input array in either RGB or HSV color space
    :type img: :class:`~numpy:numpy.ndarray`
    :param inverse: option that determines whether conversion is from rgb2hsv (False) or hsv2rgb (True)
    :type inverse: :class:`boolean`
    :return: color space converted array
    :rtype: ~numpy:np.ndarray

    """

    if not inverse:
        arr = rgb2lms(img)
    else:
        arr = lms2rgb(img)

    return arr
