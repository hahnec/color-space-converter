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


class HsvConverter(ConverterBaseclass):

    def __init__(self, *args, **kwargs):
        super(HsvConverter, self).__init__(*args, **kwargs)

    def hsv_conv(self, img: np.ndarray = None, inverse: bool = False) -> np.ndarray:
        """ Convert RGB color space to HSV color space or vice versa given the inverse option.

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
            self._arr = rgb2hsv(self._arr)
        else:
            self._arr = hsv2rgb(self._arr)

        return self._arr


def rgb2hsv(rgb: np.ndarray = None) -> np.ndarray:
    """ Convert RGB color space to HSV color space

    :param rgb: input array in red, green and blue (RGB) space
    :type rgb: :class:`~numpy:numpy.ndarray`
    :return: array in hue, saturation and value (HSV) space
    :rtype: ~numpy:np.ndarray

    """

    rgb = rgb.astype('float')
    maxv = np.amax(rgb, axis=2)
    maxc = np.argmax(rgb, axis=2)
    minv = np.amin(rgb, axis=2)
    minc = np.argmin(rgb, axis=2)

    # slicing implementation of HSV channel definitions
    hsv = np.zeros(rgb.shape, dtype='float')
    hsv[maxc == minc, 0] = np.zeros(hsv[maxc == minc, 0].shape)
    hsv[maxc == 0, 0] = (((rgb[..., 1] - rgb[..., 2]) * 60.0 /
                          (maxv - minv + np.spacing(1))) % 360.0)[maxc == 0]
    hsv[maxc == 1, 0] = (((rgb[..., 2] - rgb[..., 0]) * 60.0 /
                          (maxv - minv + np.spacing(1))) + 120.0)[maxc == 1]
    hsv[maxc == 2, 0] = (((rgb[..., 0] - rgb[..., 1]) * 60.0 /
                          (maxv - minv + np.spacing(1))) + 240.0)[maxc == 2]
    hsv[maxv == 0, 1] = np.zeros(hsv[maxv == 0, 1].shape)
    hsv[maxv != 0, 1] = (1 - minv / (maxv + np.spacing(1)))[maxv != 0]
    hsv[..., 2] = maxv

    return hsv


def hsv2rgb(hsv: np.ndarray = None) -> np.ndarray:
    """ Convert HSV color space to RGB color space

    :param hsv: input array in hue, saturation and value (HSV) space
    :type hsv: :class:`~numpy:numpy.ndarray`
    :return: array in red, green and blue (RGB) space
    :rtype: ~numpy:np.ndarray

    """

    hi = np.floor(hsv[..., 0] / 60.0) % 6
    hi = hi.astype('uint8')
    v = hsv[..., 2].astype('float')
    f = (hsv[..., 0] / 60.0) - np.floor(hsv[..., 0] / 60.0)
    p = v * (1.0 - hsv[..., 1])
    q = v * (1.0 - (f * hsv[..., 1]))
    t = v * (1.0 - ((1.0 - f) * hsv[..., 1]))

    rgb = np.zeros(hsv.shape)
    rgb[hi == 0, :] = np.dstack((v, t, p))[hi == 0, :]
    rgb[hi == 1, :] = np.dstack((q, v, p))[hi == 1, :]
    rgb[hi == 2, :] = np.dstack((p, v, t))[hi == 2, :]
    rgb[hi == 3, :] = np.dstack((p, q, v))[hi == 3, :]
    rgb[hi == 4, :] = np.dstack((t, p, v))[hi == 4, :]
    rgb[hi == 5, :] = np.dstack((v, p, q))[hi == 5, :]

    return rgb


def hsv_conv(img: np.ndarray = None, inverse: bool = False) -> np.ndarray:
    """ Convert RGB color space to HSV color space or vice versa given the inverse option.

    :param img: input array in either RGB or HSV color space
    :type img: :class:`~numpy:numpy.ndarray`
    :param inverse: option that determines whether conversion is from rgb2hsv (False) or hsv2rgb (True)
    :type inverse: :class:`boolean`
    :return: color space converted array
    :rtype: ~numpy:np.ndarray

    """

    if not inverse:
        arr = rgb2hsv(img)
    else:
        arr = hsv2rgb(img)

    return arr
