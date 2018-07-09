import numpy as np
import glob
import sprites
import matplotlib.pyplot as plt
from map_output_C import read_map_CPP
from map_output_C import read_map_H

file_list = sorted(glob.glob("%s%s" % ("/home/pi/Documents/mbed_Graphics/bitmap_sprites", "/*.bmp")))

total_spritesheet = np.zeros((sprites.sprite_y, sprites.sprite_x*np.size(file_list)), dtype='uint8')
for ii in range(0, np.size(file_list)):
    this_sprite = sprites.bitmap_fix(file_list[ii])
    export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
    total_spritesheet[0:sprites.sprite_y, ii*sprites.sprite_x:(ii*sprites.sprite_x)+sprites.sprite_x] = export_sprite
    
sprite_sheet = np.reshape(total_spritesheet, (np.size(total_spritesheet)))

dicta_cpp = read_map_CPP("/home/pi/Documents/mbed_Graphics/output_maps/map005.cpp")
dicta_h = read_map_H("/home/pi/Documents/mbed_Graphics/output_maps/map005.h")
this_map = dicta_cpp["map_array"]

sprite_x = 16
sprite_y = 16
sprite_n = sprite_x * sprite_y
pre_pos_x = 0
pre_sprite_pos_x = 6
post_pos_x = 0
post_pos_y = 0
post_sprite_pos_y = 6
buffer_size = sprite_n * 2 
n_x = sprite_x
n_sprites = 183
alpha_pixel = 28

retain_buffer = np.zeros(buffer_size, dtype='uint8');
effect_buffer = np.zeros(buffer_size, dtype='uint8');
for i_16 in range(0, buffer_size):
    map_index = this_map[(((i_16//sprite_x)%2)+pre_pos_x+pre_sprite_pos_x) + ((post_pos_y+post_sprite_pos_y)*dicta_h["map_x"][0])];
    sprite_pixel = ((i_16%sprite_x)+(sprite_x*map_index))+(((i_16%((sprite_x*2)*sprite_x))//(sprite_x*2))*(sprite_x*n_sprites));
    #sprite_pixel = sprite_indexing(i_16, 0, map_index, sprite_x*2, buffer_size);
    retain_buffer[i_16] = sprite_sheet[sprite_pixel];
    
i_8 = 3
mm = np.zeros(buffer_size, dtype='uint32')
for i_16 in range(0, buffer_size):
#    effect_buffer[i_16] = retain_buffer[i_16];
    if ((i_16 >= ((i_8*4)*sprite_x)) & (i_16 < (((i_8*4)*sprite_x)+sprite_n))):
        map_index = 18;
        sprite_pixel = 1;
        mm[i_16] = sprite_pixel
        sprite_pixel = (((i_16-((i_8*4)*sprite_x))%sprite_x)+(sprite_x*map_index))+((((i_16-((i_8*4)*sprite_x))%(n_x*sprite_x))//n_x)*(sprite_x*n_sprites));
        #sprite_pixel = sprite_indexing(i_16-(i_8*4), 0, map_index, sprite_x*2, buffer_size);
        if (sprite_sheet[sprite_pixel] == alpha_pixel):
            effect_buffer[i_16] = retain_buffer[i_16];
        else:
            effect_buffer[i_16] = sprite_sheet[sprite_pixel];
    else:
        effect_buffer[i_16] = retain_buffer[i_16];

    
effect_buffer_2 = np.reshape(effect_buffer, (sprite_y*2, sprite_x))
mm_2 = np.reshape(mm, (sprite_y*2, sprite_x))

disp_map = np.zeros((np.size(effect_buffer_2, 0), np.size(effect_buffer_2, 1), 3), dtype='uint8')
disp_map[:, :, 0] = ((np.right_shift(effect_buffer_2, 5) & 7) / 7) * 255
disp_map[:, :, 1] = ((np.right_shift(effect_buffer_2, 2) & 7) / 7) * 255
disp_map[:, :, 2] = ((effect_buffer_2 & 3) / 3) * 255

fig, ax = plt.subplots()
cax = ax.imshow(disp_map)

fig2, ax2 = plt.subplots()
cax2 = ax2.imshow(mm_2)

plt.show()