import numpy as np
import matplotlib.pyplot as plt

ef_b = np.uint8(225)
ef_n = np.uint16(50625)

vis_grid_x = np.uint8(15)
vis_grid_y = np.uint8(15)
vis_grid_n = np.uint8(225)

effect_n = np.uint8(0)
effect_buf_n = np.zeros(ef_b, dtype='uint8')
effect_buf_delay = np.zeros(ef_b, dtype='uint32')
effect_buf_dmg = np.zeros(ef_b, dtype='uint16')
effect_sprite_array = np.zeros(ef_n, dtype='uint8')
effect_sprite_index = np.zeros(ef_n, dtype='uint8')
effect_sprite_pos = np.zeros(ef_n, dtype='uint8')

update_rate = np.uint32(600)
e_x = np.uint8(0)
e_y = np.uint8(0)
ex_i8 = np.int16(1)
ey_i8 = np.int16(0)
map_index = np.uint8(27)
sprite_indexing = np.uint8(0)

for i_16 in range(0, vis_grid_n):
    e_x = e_x + ex_i8;
    e_y = e_y + ey_i8;
        
    if ((e_x >= vis_grid_x) or (e_y >= vis_grid_y)) == True:
        break;
        
    effect_buf_n[i_16] = 2;
    effect_buf_delay[i_16] = update_rate;
    effect_buf_dmg[i_16] = 1;
        
    for j_16 in range(0, effect_buf_n[i_16]):
        if j_16 == 0:
            effect_sprite_array[(j_16 + (i_16*ef_b))] = 7;
        else:
            effect_sprite_array[(j_16 + (i_16*ef_b))] = map_index;
        effect_sprite_index[(j_16 + (i_16*ef_b))] = sprite_indexing;
        effect_sprite_pos[(j_16 + (i_16*ef_b))] = (e_x-(j_16*ex_i8)) + ((e_y-(j_16*ey_i8))*vis_grid_x);

effect_n = i_16;

#fig, ax = plt.subplots()
#cax = ax.plot(effect_sprite_array)
#
#plt.show()
