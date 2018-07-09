#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon July 03 00:00:00 2018

@author: Biobawls
"""

import numpy as np
#import matplotlib as mpl
#mpl.use('TkAgg')
#import matplotlib.pyplot as plt
import glob
import sprites

file_list = sorted(glob.glob("/home/pi/Documents/mbed_Graphics/bitmap_sprites/*.bmp"))

total_spritesheet = np.zeros((sprites.sprite_y, sprites.sprite_x*np.size(file_list)), dtype='uint8')
for ii in range(0, np.size(file_list)):
    this_sprite = sprites.bitmap_fix(file_list[ii])
    export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
    total_spritesheet[0:sprites.sprite_y, ii*sprites.sprite_x:(ii*sprites.sprite_x)+sprites.sprite_x] = export_sprite

disp_sprite = np.zeros((sprites.sprite_y, sprites.sprite_x*np.size(file_list), 3), dtype='uint8')
disp_sprite[:, :, 0] = np.right_shift(total_spritesheet, 5) & 7
disp_sprite[:, :, 1] = np.right_shift(total_spritesheet, 2) & 7
disp_sprite[:, :, 2] = total_spritesheet & 3

disp_sprite_norm = np.zeros(np.shape(disp_sprite), dtype='double')
disp_sprite_norm[:, :, 0] = disp_sprite[:, :, 0]/np.max(sprites.rr)
disp_sprite_norm[:, :, 1] = disp_sprite[:, :, 1]/np.max(sprites.gg)
disp_sprite_norm[:, :, 2] = disp_sprite[:, :, 2]/np.max(sprites.bb)

np.savetxt('/home/pi/Documents/mbed_Graphics/output_spritesheet/spritesheet.out', total_spritesheet, delimiter=',',fmt='%i',newline=',\n')

#fig, ax = plt.subplots()
#cax = ax.imshow(disp_sprite_norm)
#
#plt.show()