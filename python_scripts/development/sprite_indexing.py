import numpy as np
import matplotlib.pyplot as plt
import glob
import sprites

# replace i_16//sprite_x with (i_16%(n_x*sprite_x))//n_x
# replace (sprite_n-1-i_16)//sprite_x with ((n_v-1-i_16)%(n_x*sprite_x))//n_x
# replace (n_x-1-i_16)%sprite_x with sprite_x-1-(i_16%sprite_x)

file_list = sorted(glob.glob("/home/pi/Documents/mbed_Graphics/bitmap_sprites/*.bmp"))

total_spritesheet = np.zeros((sprites.sprite_y, sprites.sprite_x*np.size(file_list)), dtype='uint8')
for ii in range(0, np.size(file_list)):
    this_sprite = sprites.bitmap_fix(file_list[ii])
    export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
    total_spritesheet[0:sprites.sprite_y, ii*sprites.sprite_x:(ii*sprites.sprite_x)+sprites.sprite_x] = export_sprite

#sprite_sheet = np.reshape(np.transpose(total_spritesheet), [np.size(total_spritesheet)])
sprite_sheet = np.reshape(total_spritesheet, [np.size(total_spritesheet)])

n_sprites = 346
sprite_x = 16
sprite_y = 16
sprite_n = 256
map_index = 16
x_grid = 4
y_grid = 1
n_grid = x_grid * y_grid
n_x = x_grid * sprite_x
n_y = y_grid * sprite_y
n_v = n_x * n_y

fig, ax = plt.subplots(4, 2)
out01 = []
ii01 = []
out02 = []
ii02 = []
out03 = []
ii03 = []
out04 = []
ii04 = []
out05 = []
ii05 = []
out06 = []
ii06 = []
out07 = []
ii07 = []
out08 = []
ii08 = []
for i_16 in range (0, sprite_n*n_grid):
    # mirror -90 roll
    #sprite_pixel = ((i_16//sprite_x)+(sprite_x*map_index))+((i_16%sprite_x)*(sprite_x*n_sprites));
    sprite_pixel = ((((i_16%(n_x*sprite_x))//n_x))+(sprite_x*map_index))+((i_16%sprite_x)*(sprite_x*n_sprites));
    out01.append(sprite_sheet[sprite_pixel]);
    ii01.append(sprite_pixel);
    
out01 = np.reshape(out01, [sprite_y*y_grid, sprite_x*x_grid])

im = ax[0, 0].imshow(out01)
#ax[0, 0].set_aspect('equal', 'box')
    
for i_16 in range (0, sprite_n*n_grid):
    # mirror 90 roll
    #sprite_pixel = (((sprite_n-1-i_16)//sprite_x)+(sprite_x*map_index))+(((sprite_n-1-i_16)%sprite_x)*(sprite_x*n_sprites));
    
    sprite_pixel = ((((n_v-1-i_16)%(n_x*sprite_x))//n_x)+(sprite_x*map_index))+((sprite_x-1-(i_16%sprite_x))*(sprite_x*n_sprites));
    out02.append(sprite_sheet[sprite_pixel]);
    ii02.append(sprite_pixel);
    
out02 = np.reshape(out02, [sprite_y*y_grid, sprite_x*x_grid])    

im = ax[0, 1].imshow(out02)
#ax[0, 1].set_aspect('equal', 'box')
    
for i_16 in range (0, sprite_n*n_grid):
    # normal indexing
    #sprite_pixel = ((i_16%sprite_x)+(sprite_x*map_index))+((i_16//sprite_x)*(sprite_x*n_sprites));
    sprite_pixel = ((i_16%sprite_x)+(sprite_x*map_index))+(((i_16%(n_x*sprite_x))//n_x)*(sprite_x*n_sprites));
    out03.append(sprite_sheet[sprite_pixel]);
    ii03.append(sprite_pixel);
    
out03 = np.reshape(out03, [sprite_y*y_grid, sprite_x*x_grid])

im = ax[1, 0].imshow(out03)
#ax[1, 0].set_aspect('equal', 'box')
    
for i_16 in range (0, sprite_n*n_grid):
    # 180 roll
    sprite_pixel = ((sprite_x-1-(i_16%sprite_x))+(sprite_x*map_index))+((((n_v-1-i_16)%(n_x*sprite_x))//n_x)*(sprite_x*n_sprites));
    out04.append(sprite_sheet[sprite_pixel]);
    ii04.append(sprite_pixel);
    
out04 = np.reshape(out04, [sprite_y*y_grid, sprite_x*x_grid])

im = ax[1, 1].imshow(out04)
#ax[1, 1].set_aspect('equal', 'box')    

for i_16 in range (0, sprite_n*n_grid):
    # mirror 180 roll
    sprite_pixel = ((i_16%sprite_x)+(sprite_x*map_index))+((((n_v-1-i_16)%(n_x*sprite_x))//n_x)*(sprite_x*n_sprites));
    out05.append(sprite_sheet[sprite_pixel]);
    ii05.append(sprite_pixel);
    
out05 = np.reshape(out05, [sprite_y*y_grid, sprite_x*x_grid])

im = ax[2, 0].imshow(out05)
#ax[2, 0].set_aspect('equal', 'box')
    
for i_16 in range (0, sprite_n*n_grid):
    # normal mirror
    #sprite_pixel = (((n_x-1-i_16)%sprite_x)+(sprite_x*map_index))+((((i_16%(n_x*sprite_x))//n_x))*(sprite_x*n_sprites));
    sprite_pixel = ((sprite_x-1-(i_16%sprite_x))+(sprite_x*map_index))+(((i_16%(n_x*sprite_x))//n_x)*(sprite_x*n_sprites));
    out06.append(sprite_sheet[sprite_pixel]);
    ii06.append(sprite_pixel);
    
out06 = np.reshape(out06, [sprite_y*y_grid, sprite_x*x_grid])

im = ax[2, 1].imshow(out06)
#ax[2, 1].set_aspect('equal', 'box')
    
for i_16 in range (0, sprite_n*n_grid):
    # roll 90
    sprite_pixel = ((((i_16%(n_x*sprite_x))//n_x))+(sprite_x*map_index))+((sprite_x-1-(i_16%sprite_x))*(sprite_x*n_sprites));
    out07.append(sprite_sheet[sprite_pixel]);
    ii07.append(sprite_pixel);
    
out07 = np.reshape(out07, [sprite_y*y_grid, sprite_x*x_grid])

im = ax[3, 0].imshow(out07)
#ax[3, 0].set_aspect('equal', 'box')
    
for i_16 in range (0, sprite_n*n_grid):
    # roll -90
    sprite_pixel = ((((n_v-1-i_16)%(n_x*sprite_x))//n_x)+(sprite_x*map_index))+((i_16%sprite_x)*(sprite_x*n_sprites));
    out08.append(sprite_sheet[sprite_pixel]);
    ii08.append(sprite_pixel);

out08 = np.reshape(out08, [sprite_y*y_grid, sprite_x*x_grid])

im = ax[3, 1].imshow(out08)
#ax[3, 1].set_aspect('equal', 'box')

