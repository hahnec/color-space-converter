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

# https://web.archive.org/web/20120502065620/http://cookbooks.adobe.com/post_Useful_color_equations__RGB_to_LAB_converter-14227.html

# Observer = 2°, Illuminant = D65 (from Adobe)
MAT_ADB = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])

# Int. Telecom. Union standard XYZitu601-1 (D65) from Reinhard et al. paper (2001)
MAT_ITU = np.array([[0.4306, 0.3415, 0.1784], [0.2220, 0.7067, 0.0713], [0.0202, 0.1295, 0.9394]])


class XyzConverter(ConverterBaseclass):

    def __init__(self, *args, **kwargs):
        super(XyzConverter, self).__init__(*args, **kwargs)

    def xyz_conv(self, img: np.ndarray = None, inverse: bool = False, standard: str = 'Adobe', norm: bool = False) \
            -> np.ndarray:
        """ Convert RGB color space to xyz color space or vice versa given the inverse option.

        :param img: input array in either RGB or xyz color space
        :type img: :class:`~numpy:numpy.ndarray`
        :param inverse: option that determines whether conversion is from rgb2xyz (False) or xyz2rgb (True)
        :type inverse: :class:`boolean`
        :param standard: option that determines which standard (Adobe or ITU) is used
        :type standard: str, optional
        :param norm: option that determines whether matrix is normalized to allow for R=G=B=1 to X=Y=Z=1 mappings
        :type norm: bool, optional
        :return: color space converted array
        :rtype: ~numpy:np.ndarray

        """

        # override if inputs present
        self._arr = img if img is not None else self._arr
        self._inv = inverse if inverse else self._inv

        if not self._inv:
            self._arr = rgb2xyz(self._arr, standard=standard, norm=norm)
        else:
            self._arr = xyz2rgb(self._arr, standard=standard, norm=norm)

        return self._arr


def rgb2xyz(rgb: np.ndarray = None, standard: str = 'Adobe', norm: bool = False) -> np.ndarray:
    """ Convert RGB color space to xyz color space

    :param rgb: input array in red, green and blue (RGB) space
    :type rgb: :class:`~numpy:numpy.ndarray`
    :param standard: option that determines which standard (Adobe or ITU) is used
    :type standard: str, optional
    :param norm: option that determines whether matrix is normalized to allow for R=G=B=1 to X=Y=Z=1 mappings
    :type norm: bool, optional
    :return: array in xyz space
    :rtype: ~numpy:np.ndarray

    """

    # store shape
    shape = rgb.shape

    # choose method
    mat = MAT_ADB if standard == 'Adobe' else MAT_ITU

    # normalize Matrix such that R = G = B = 1 maps to X = Y = Z = 1
    mat = np.transpose(np.dot(np.ones(3), np.linalg.inv(MAT_ITU))*MAT_ITU.T) if norm else mat

    # normalize input
    rgb = rgb / np.max(rgb)

    for ch in range(rgb.shape[2]):
        mask = rgb[..., ch] > 0.04045
        rgb[..., ch][mask] = np.power((rgb[..., ch] + 0.055) / 1.055, 2.4)[mask]
        rgb[..., ch][~mask] /= 12.92

    rgb *= 100

    # reshape image to channel vectors
    rgb = rgb.reshape(-1, 3).T

    # convert to xyz space
    xyz = np.dot(mat, rgb)

    # reshape to 2-D image
    xyz = xyz.T.reshape(shape)

    return xyz


def xyz2rgb(xyz: np.ndarray = None, standard: str = 'Adobe', norm: bool = False) -> np.ndarray:
    """ Convert HSV color space to RGB color space

    :param xyz: input array in xyz space
    :type xyz: :class:`~numpy:numpy.ndarray`
    :param standard: option that determines which standard (Adobe or ITU) is used
    :type standard: str, optional
    :param norm: option that determines whether matrix is normalized to allow for R=G=B=1 to X=Y=Z=1 mappings
    :type norm: bool, optional
    :return: array in red, green and blue (RGB) space
    :rtype: ~numpy:np.ndarray

    """

    # store shape
    shape = xyz.shape

    # choose method
    mat = MAT_ADB if standard == 'Adobe' else MAT_ITU

    # normalize Matrix such that R = G = B = 1 maps to X = Y = Z = 1
    mat = np.transpose(np.dot(np.ones(3), np.linalg.inv(MAT_ITU))*MAT_ITU.T) if norm else mat

    # invert matrix
    mat_inv = np.linalg.inv(mat)

    # de-normalize input
    xyz = xyz.astype('float') / 100

    # reshape image to channel vectors
    xyz = xyz.reshape(-1, 3).T

    # convert to rgb space
    rgb = np.dot(mat_inv, xyz)

    # reshape to 2-D image
    rgb = rgb.T.reshape(shape)

    for ch in range(rgb.shape[2]):
        mask = rgb[..., ch] > 0.0031308
        rgb[..., ch][mask] = 1.055 * np.power(rgb[..., ch][mask], 1 / 2.4) - 0.055
        rgb[..., ch][~mask] *= 12.92

    return rgb


def xyz_conv(img: np.ndarray = None, inverse: bool = False, standard: str = 'Adobe', norm: bool = False) \
        -> np.ndarray:
    """ Convert RGB color space to xyz color space or vice versa given the inverse option.

    :param img: input array in either RGB or xyz color space
    :type img: :class:`~numpy:numpy.ndarray`
    :param inverse: option that determines whether conversion is from rgb2xyz (False) or xyz2rgb (True)
    :type inverse: :class:`boolean`
    :param standard: option that determines which standard (Adobe or ITU) is used
    :type standard: str, optional
    :param norm: option that determines whether matrix is normalized to allow for R=G=B=1 to X=Y=Z=1 mappings
    :type norm: bool, optional
    :return: color space converted array
    :rtype: ~numpy:np.ndarray

    """

    if not inverse:
        arr = rgb2xyz(img, standard=standard, norm=norm)
    else:
        arr = xyz2rgb(img, standard=standard, norm=norm)

    return arr
