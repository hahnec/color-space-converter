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

from color_space_converter.top_level import ColorSpaceConverter, METHODS, normalize_img
from color_space_converter import gry_conv, hsv_conv, lab_conv, lms_conv, xyz_conv, yuv_conv

import unittest
import os, sys
import numpy as np
import imageio
from ddt import ddt, idata, unpack, data


@ddt
class ColorSpaceConverterTester(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ColorSpaceConverterTester, self).__init__(*args, **kwargs)

    def setUp(self):
        """ set up test environment """

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dat_path = os.path.join(self.dir_path, 'data')

        # get test data from imageio lib
        self.fn_img = 'chelsea.png'
        self.ref_img = imageio.imread('imageio:'+self.fn_img)

        # create output folder
        os.mkdir(self.dat_path) if not os.path.exists(self.dat_path) else None

        # save original image (for comparison and reload)
        fp = os.path.join(self.dat_path, self.fn_img)
        if not os.path.exists(fp):
            imageio.imwrite(uri=fp, im=normalize_img(self.ref_img))

    @staticmethod
    def avg_hist_dist(img1, img2, bins=2**8-1):
        """ compute average histogram distance """

        hist_a = np.histogram(img1, bins)[0]
        hist_b = np.histogram(img2, bins)[0]

        return np.sqrt(np.sum(np.square(hist_a - hist_b)))

    @idata(([kw] for kw in [['-s ', '-m "yuv"', '-i', '-s SDTV'],
                            ['--src=', '--method="hsv"', '--inverse', '--standard=HDTV']]))
    @unpack
    def test_cli(self, kw=None):
        """ scrutinize  CLI command usage """

        from color_space_converter.bin.cli import main

        # compose cli arguments
        sys.argv.append(kw[0] + os.path.join(self.dat_path, self.fn_img)) if len(kw) > 0 else None
        sys.argv.append(kw[1]) if len(kw) > 1 else None

        # run cli command
        ret = main()

        # assertion
        self.assertEqual(True, ret)

        return True

    @idata(([m, ref] for m, ref in zip(METHODS+['wrong_arg'], (16971, 255, 515, 2000, 583, 474, 0))))
    @unpack
    def test_match_method_imageio(self, method=None, ref_val=0):
        """ compare original images with forward and backward processed images while providing output files """

        try:
            # convert to corresponding color space
            img_conv = ColorSpaceConverter(self.ref_img.copy(), method=method).main()

            # convert back to RGB space
            img_inv = ColorSpaceConverter(img_conv, method=method, inverse=True).main()

        # catch unsupported methods
        except BaseException as e:

            print(e)
            self.assertEqual(True, True if method not in METHODS else False)

            return True

        # assess quality
        dist_val = self.avg_hist_dist(self.ref_img, img_inv)
        print('Avg. histogram distance for %s is %s' % (method, round(dist_val, 3)))

        # assertion
        self.assertEqual(True, ref_val >= dist_val)

        # save color space result
        fp = os.path.join(self.dat_path, self.fn_img.split('.')[0] + '_' + method + '.png')
        imageio.imwrite(uri=fp, im=normalize_img(img_conv))

        # save re-converted result
        fp = os.path.join(self.dat_path, self.fn_img.split('.')[0] + '_' + method + '_re-converted.png')
        imageio.imwrite(uri=fp, im=normalize_img(img_inv))

        return True

    @data(
        (ColorSpaceConverter().gry_conv, gry_conv),
        (ColorSpaceConverter().hsv_conv, hsv_conv),
        (ColorSpaceConverter().lab_conv, lab_conv),
        (ColorSpaceConverter().lms_conv, lms_conv),
        (ColorSpaceConverter().xyz_conv, xyz_conv),
        (ColorSpaceConverter().yuv_conv, yuv_conv),
        (ColorSpaceConverter().gry_conv, gry_conv, True),
        (ColorSpaceConverter().hsv_conv, hsv_conv, True),
        (ColorSpaceConverter().lab_conv, lab_conv, True),
        (ColorSpaceConverter().lms_conv, lms_conv, True),
        (ColorSpaceConverter().xyz_conv, xyz_conv, True),
        (ColorSpaceConverter().yuv_conv, yuv_conv, True)
    )
    @unpack
    def test_compare_functions(self, obj_method, prd_method, inverse=False):
        """ validate that instance methods yield same result as their procedural counterparts """

        # compute results from instance and procedural methods
        res_obj = obj_method(self.ref_img.copy(), inverse=inverse)
        res_prd = prd_method(self.ref_img.copy(), inverse=inverse)

        # assess quality
        dist_val = self.avg_hist_dist(res_obj, res_prd)
        print('Avg. histogram distance for %s is %s' % (prd_method, round(dist_val, 3)))

        # assertion
        self.assertEqual(True, 1 > dist_val)                                # validate histogram is equal
        self.assertEqual(True, len(res_obj.shape) == len(res_prd.shape))    # validate shapes are equal

        return True


if __name__ == '__main__':
    unittest.main()
