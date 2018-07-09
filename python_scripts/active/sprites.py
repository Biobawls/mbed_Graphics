#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon July 03 00:00:00 2018

@author: Biobawls
"""

import numpy as np
from scipy import misc

sprite_x = 16
sprite_y = 16

rr = np.arange(0, 2**3)
gg = np.arange(0, 2**3)
bb = np.arange(0, 2**2)

def bitmap_fix(path_in):
    this_sprite = misc.imread(path_in, mode='RGB')
    this_sprite[:, :, 0] = np.round((this_sprite[:, :, 0]/255)*np.max(rr))
    this_sprite[:, :, 1] = np.round((this_sprite[:, :, 1]/255)*np.max(gg))
    this_sprite[:, :, 2] = np.round((this_sprite[:, :, 2]/255)*np.max(bb))
    return this_sprite

def sprite_indexing(indexing_in, sprite_in):
    if indexing_in == 0:
        return sprite_in
    elif indexing_in == 1:
        return np.flip(sprite_in, 1)
    elif indexing_in == 2:
        return np.rot90(sprite_in, 3)
    elif indexing_in == 3:
        return np.rot90(np.flip(sprite_in, 1), 3)
    elif indexing_in == 4:
        return np.rot90(sprite_in, 2)
    elif indexing_in == 5:
        return np.rot90(np.flip(sprite_in, 1), 2)
    elif indexing_in == 6:
        return np.rot90(sprite_in, 1)
    elif indexing_in == 7:
        return np.rot90(np.flip(sprite_in, 1), 1)
    else:
        return sprite_in
