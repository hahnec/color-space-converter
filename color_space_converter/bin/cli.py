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

from color_space_converter import __version__
from color_space_converter.top_level import ColorSpaceConverter, METHODS, FILE_EXTS, normalize_img

import getopt
import sys, os
import imageio


def usage():

    print("Usage: color-space-converter <options>\n")
    print("Options:")
    print("-s <path>,     --src=<str>        Specify source image file or folder to process")
    print("-m <method>,   --method=<str>     Provide color transfer method. Available methods are:")
    print("                                  "+', '.join(['"'+m+'"' for m in METHODS]))
    print("-i <path>,     --inverse=<bool>   Specify conversion direction (forward=False or backwards=True)")
    print("-S <path>,     --standard=<str>   Specify standard with either 'HDTV' or 'SDTV' for headroom handling")
    print("-w ,           --win              Select files from window")
    print("-h,            --help             Print this help message")
    print("")


def parse_options(argv):

    try:
        opts, args = getopt.getopt(argv, "hs:m:iS:w", ["help", "src=", "method=", "inverse", "standard=", "win"])
    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)

    cfg = dict()

    # default settings
    cfg['src_path'] = ''
    cfg['method'] = None
    cfg['inverse'] = False
    cfg['standard'] = 'HDTV'
    cfg['win'] = None

    if opts:
        for (opt, arg) in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            if opt in ("-s", "--src"):
                cfg['src_path'] = arg.strip(" \"\'")
            if opt in ("-m", "--method"):
                cfg['method'] = arg.strip(" \"\'")
            if opt in ("-i", "--inverse"):
                cfg['inverse'] = True
            if opt in ("-S", "--standard"):
                cfg['standard'] = arg.strip(" \"\'")
            if opt in ("-w", "--win"):
                cfg['win'] = True

    # create dictionary containing all parameters for the light field
    return cfg


def select_file(init_dir=None, title=''):
    ''' get filepath from tkinter dialog '''

    # consider initial directory if provided
    init_dir = os.path.expanduser('~/') if not init_dir else init_dir

    # import tkinter while considering Python version
    try:
        if (sys.version_info > (3, 0)):
            from tkinter import Tk
            from tkinter.filedialog import askopenfilename
        elif (sys.version_info > (2, 0)):
            from Tkinter import Tk
            from tkFileDialog import askopenfilename
    except ImportError:
        raise ImportError('Please install tkinter package.')

    # open window using tkinter
    root = Tk()
    root.withdraw()
    root.update()
    file_path = askopenfilename(initialdir=[init_dir], title=title)
    root.update()

    return file_path if file_path else None


def main():

    # program info
    print("\ncolor-space-converter v%s \n" % __version__)

    # parse options
    cfg = parse_options(sys.argv[1:])

    # select files from window (if option set)
    if cfg['win']:
        cfg['src_path'] = select_file('.', 'Select source image')

    # cancel if file paths not provided
    if not cfg['src_path']:
        usage()
        print('Canceled due to missing image file path\n')
        sys.exit()

    # select light field image(s) considering provided folder or file
    if os.path.isdir(cfg['src_path']):
        filenames = [f for f in os.listdir(cfg['src_path']) if f.lower().endswith(FILE_EXTS)]
    elif not os.path.isfile(cfg['src_path']):
        print('File(s) not found \n')
        sys.exit()
    else:
        filenames = [cfg['src_path']]

    # method handling
    cfg['method'] = cfg['method'] if cfg['method'] in METHODS else 'default'

    # file handling
    output_path = os.path.dirname(cfg['src_path'])

    # user notifications
    print("Converting to %s color space ... \n" % cfg['method'])
    if cfg['method'] != METHODS[0]:
        print(
            'Output image is saved as uint8 which may yield undesirable results depending on the numerical range of '
            'the color space. \nFor lossless conversion, API usage is recommended. For more details on this, see '
            ' https://hahnec.github.io/color-space-converter/.'
            )

    # process the images
    for f in filenames:
        src = imageio.imread(uri=f)
        obj = ColorSpaceConverter(src=src, method=cfg['method'], inverse=cfg['inverse'], standard=cfg['standard'])
        res = obj.main()
        res = normalize_img(res)
        filename = os.path.splitext(os.path.basename(cfg['src_path']))[0]+'_'+cfg['method']
        file_ext = os.path.splitext(cfg['src_path'])[-1]
        imageio.imwrite(uri=os.path.join(output_path, filename+'.'+file_ext[1:]), im=res)

    return True


if __name__ == "__main__":

    sys.exit(main())
