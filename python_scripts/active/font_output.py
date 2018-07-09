#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed June 27 01:30:55 2018

@author: Biobawls
This code assumes the font glyph is 8x16.
The loaded bitmap is expected to be black and white.
0 will = 0 and anything not 0 will = 1
"""

import numpy as np
from scipy import misc
import glob
import ntpath
import os

file_list = sorted(glob.glob("/home/pi/Documents/mbed_Graphics/bitmaps_font/*.bmp"))

for this_file in file_list:
    this_glyph = misc.imread(this_file, mode='L')
    this_glyph_bin = np.equal(this_glyph, 0)
    this_glyph_bytes = [np.packbits(np.uint8(this_glyph_bin))]
    
    file_name = os.path.splitext(ntpath.basename(this_file))[0]
    np.savetxt('/home/pi/Documents/mbed_Graphics/output_font/' + file_name + '.out', this_glyph_bytes, delimiter=', ',fmt='0x%02x')
    
