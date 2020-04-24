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


class ConverterBaseclass(object):

    def __init__(self, *args, **kwargs):
        """

        The converter baseclass provides a scheme of variables and functions that all child converter classes
        have in common. The child classes are thought to handle the conversion specific to a certain color space.

        :param args: passed arguments are assigned to variables in the following order:
                        1) src image 2) conversion method 3) inverse option 4) standard option
        :param kwargs: supported keyword arguments are as follows: 'src', 'method', 'inverse' and 'standard'
        """

        # assign variables from arguments
        self._arr = args[0] if len(args) > 0 else None
        self._met = args[1] if len(args) > 1 else 'default'
        self._inv = args[2] if len(args) > 2 else False
        self._stn = args[3] if len(args) > 3 else 'HDTV'

        # assign variables from keyword arguments
        self._arr = kwargs['src'] if 'src' in kwargs else self._arr
        self._met = kwargs['method'] if 'method' in kwargs else self._met
        self._inv = kwargs['inverse'] if 'inverse' in kwargs else self._inv
        self._stn = kwargs['standard'] if 'standard' in kwargs else self._stn

        # validate variables
        self.validate_types()
        self.validate_img_dims() if not (self._arr is None) else None

        # store original image shape
        self.orig_shape = self._arr.shape if not (self._arr is None) else None

    def validate_types(self) -> bool:
        """
        This function analyzes the variable type from supported keywords 'src', 'method', 'inverse' and 'standard'.
        An exception is thrown if the data types are not as expected.
        """

        if not isinstance(self._arr, np.ndarray) and not (self._arr is None):
            raise BaseException('Provided "src" is not a numpy array.')
        elif not isinstance(self._met, str):
            raise BaseException('Provided "method" argument is not of type str.')
        elif not isinstance(self._inv, bool):
            raise BaseException('Provided "inverse" argument is not of type bool.')
        elif not isinstance(self._stn, str):
            raise BaseException('Provided "standard" argument is not of type str.')
        else:
            return True

    def validate_img_dims(self) -> bool:
        """
        This function validates the image dimensions. It throws an exception if the dimension are unequal to 2 or 3.
        """

        # add third image dimension for monochromatic images
        self._arr = self._arr[..., np.newaxis] if len(self._arr.shape) == 2 else self._arr

        if len(self._arr.shape) != 3:
            raise BaseException('Wrong image dimensions')
        else:
            return True

    def validate_color_chs(self) -> bool:
        """
        This function checks whether provided images consist of 3 color channels. An exception is thrown otherwise.
        """

        if self._arr.shape[2] != 3:
            raise BaseException('Each image must have 3 color channels')
        else:
            return True

    @property
    def arr(self):
        """ getter for array that is color converted """
        return self._arr
