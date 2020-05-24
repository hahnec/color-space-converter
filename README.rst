=====================
color-space-converter
=====================

Description
-----------

*color-space-converter* enables fast image color space conversion via vectorization from numpy arrays.

|release| |build| |coverage| |pypi|

Installation
------------

* via pip:
    1. install with ``pip3 install color-space-converter``
    2. type ``color-space-converter -h`` to the command line once installation finished

* from source:
    1. install Python from https://www.python.org/
    2. download the source_ using ``git clone https://github.com/hahnec/color-space-converter.git``
    3. go to the root directory ``cd color_space_converter``
    4. load dependencies ``$ pip3 install -r requirements.txt``
    5. install with ``python3 setup.py install``
    6. if installation ran smoothly, enter ``color-space-converter -h`` to the command line

Quick API Guide
---------------

Procedural usage::

    from color_space_converter import rgb2yuv, yuv2rgb

    def treat_lum(img):

        yuv = rgb2yuv(img)
        yuv[..., 0] /= 2
        rgb = yuv2rgb(yuv)

        return rgb

OOP style::

    from color_space_converter import ColorSpaceConverter

    def treat_sat(img):

        obj = ColorSpaceConverter(img)
        hsv = obj.hsv_conv()
        hsv[..., 1] *= .5
        rgb = obj.hsv_conv(hsv, inverse=True)

        return rgb

Command Line Usage
------------------

From the root directory of your downloaded repo, you can run the tool by

``color-space-converter -s '../your_path/yourimage.png' -m 'gry'``

on a UNIX system where the result is found at ``../your_path/``. A windows equivalent of the above command is

``color-space-converter --src=".\\your_path\\your_image.png" --method="gry"``

Alternatively, you can specify the method or select your images manually with

``color-space-converter --win --method='yuv'``

More information on optional arguments, can be found using the help parameter

``color-space-converter -h``

Author
------

`Christopher Hahne <http://www.christopherhahne.de/>`__

.. Hyperlink aliases

.. _source: https://github.com/hahnec/color-space-converter/archive/master.zip

.. |vspace| raw:: latex

   \vspace{1mm}

.. Image substitutions

.. |release| image:: https://img.shields.io/github/v/release/hahnec/color-space-converter?style=flat-square
    :target: https://github.com/hahnec/color-space-converter/releases/
    :alt: release

.. |build| image:: https://img.shields.io/travis/com/hahnec/color-space-converter?style=flat-square
    :target: https://travis-ci.com/github/hahnec/color-space-converter

.. |coverage| image:: https://img.shields.io/coveralls/github/hahnec/color-space-converter?style=flat-square
    :target: https://coveralls.io/github/hahnec/color-space-converter

.. |pypi| image:: https://img.shields.io/pypi/dm/color-space-converter?label=PyPI%20downloads&style=flat-square
    :target: https://pypi.org/project/color-space-converter/
    :alt: PyPI Downloads