#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon July 03 00:00:00 2018

@author: Biobawls
"""

import pandas as pd

class NPC():
    def __init__(self):
        self.left1 = 0
        self.left2 = 0
        self.right1 = 0
        self.right2 = 0
        self.up1 = 0
        self.up2 = 0
        self.down1 = 0
        self.down2 = 0
        
        self.left1_index = 0
        self.left2_index = 0
        self.right1_index = 0
        self.right2_index = 0
        self.up1_index = 0
        self.up2_index = 0
        self.down1_index = 0
        self.down2_index = 0
        
        self.alpha_pixel = 0
        
        self.NPC_id = ""
        self.NPC_id_num = 0
        
        self.text = ""
        self.ai = 0
        
    def set_NPC_details(self, id_string, id_num):
        self.NPC_id = id_string
        self.NPC_id_num = id_num
        
    def set_left(self, left1, left2, left1_index, left2_index):
        self.left1 = left1
        self.left2 = left2
        self.left1_index = left1_index
        self.left2_index = left2_index
        
    def set_right(self, right1, right2, right1_index, right2_index):
        self.right1 = right1
        self.right2 = right2
        self.right1_index = right1_index
        self.right2_index = right2_index
        
    def set_up(self, up1, up2, up1_index, up2_index):
        self.up1 = up1
        self.up2 = up2
        self.up1_index = up1_index
        self.up2_index = up2_index
        
    def set_down(self, down1, down2, down1_index, down2_index):
        self.down1 = down1
        self.down2 = down2
        self.down1_index = down1_index
        self.down2_index = down2_index
        
    def set_text(self, text_in):
        self.text = text_in
        
    def set_ai(self, ai_in):
        # 0, 1, 2, 3, 4, 5
        self.ai = ai_in
        
    def set_alpha_pixel(self, alpha_pixel):
        self.alpha_pixel = alpha_pixel
        
    def createCopy(self):
        new_npc = NPC()
        new_npc.set_NPC_details(self.NPC_id, self.NPC_id_num)
        new_npc.set_left(self.left1, self.left2, self.left1_index, self.left2_index)
        new_npc.set_right(self.right1, self.right2, self.right1_index, self.right2_index)
        new_npc.set_up(self.up1, self.up2, self.up1_index, self.up2_index)
        new_npc.set_down(self.down1, self.down2, self.down1_index, self.down2_index)
        new_npc.set_alpha_pixel(self.alpha_pixel)
        new_npc.set_text(self.text)
        new_npc.set_ai(self.ai)
        return(new_npc)

def build_npcs_h(h_file_text, npc_in):
    h_file_text = h_file_text + "const static uint16_t " + npc_in.NPC_id + "_sprite_array[8] = {" + str(npc_in.left1) + ", " + str(npc_in.left2) + ", " + str(npc_in.right1) + ", " + str(npc_in.right2) + ", " + str(npc_in.up1) + ", " + str(npc_in.up2) + ", " + str(npc_in.down1) + ", " + str(npc_in.down2) + "};\n"
    h_file_text = h_file_text + "const static uint8_t " + npc_in.NPC_id + "_sprite_indexing[8] = {" + str(npc_in.left1_index) + ", " + str(npc_in.left2_index) + ", " + str(npc_in.right1_index) + ", " + str(npc_in.right2_index) + ", " + str(npc_in.up1_index) + ", " + str(npc_in.up2_index) + ", " + str(npc_in.down1_index) + ", " + str(npc_in.down2_index) + "};\n"
    return h_file_text

def build_h(npc_list):
    h_file_text = ""
    h_file_text = h_file_text + "#ifndef NPC_DEFINES_H\n"
    h_file_text = h_file_text + "#define NPC_DEFINES_H\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "#include \"mbed.h\"\n"
    h_file_text = h_file_text + "#include \"npc_sprite.h\"\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "////////////////////////////////////////////////////////////////////////////////\n"
    h_file_text = h_file_text + "// sprite index in ROM\n"
    h_file_text = h_file_text + "////////////////////////////////////////////////////////////////////////////////\n"
    h_file_text = h_file_text + "// 0 = left1, 1 = left2, 2 = right1, 3 = right2, 4 = up1, 5 = up2, 6 = down1, 7 = down2\n"
    h_file_text = h_file_text + "const static uint16_t cursor_sprite_array[8] = {2, 2, 2, 2, 2, 2, 2, 2};\n"
    h_file_text = h_file_text + "const static uint8_t cursor_sprite_indexing[8] = {0, 0, 0, 0, 0, 0, 0, 0};\n"
    h_file_text = h_file_text + "const static uint16_t cursor_fill_sprite_array[8] = {4, 4, 4, 4, 4, 4, 4, 4};\n"
    h_file_text = h_file_text + "const static uint8_t cursor_fill_sprite_indexing[8] = {0, 0, 0, 0, 0, 0, 0, 0};\n"
    for this_npc in npc_list:
        h_file_text = build_npcs_h(h_file_text, this_npc)
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "bool assign_npc(uint8_t npc_type, npc_sprite* npc, uint32_t npc_ID, uint8_t vis_grid_x, uint8_t vis_grid_y, uint32_t loc, uint32_t world_x, uint32_t world_y, uint8_t ai, uint32_t update_rate);\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "#endif\n"
    ###############################################################################
    # Save the files
    ###############################################################################
    f_h = open("/home/pi/Documents/mbed_Graphics/output_npcs/npc_defines.h", mode="w")
    f_h.write(h_file_text)
    f_h.close()
    
def build_npcs_cpp(cpp_file_text, npc_in):
    cpp_file_text = cpp_file_text + "\t\tcase " + str(npc_in.NPC_id_num) + ": {\n"
    cpp_file_text = cpp_file_text + "\t\t\tnpc->init(npc_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, ai, update_rate, " + npc_in.NPC_id + "_sprite_array, " + npc_in.NPC_id + "_sprite_indexing, " + str(npc_in.alpha_pixel) + ");\n"
    cpp_file_text = cpp_file_text + "\t\t\tbreak;\n"
    cpp_file_text = cpp_file_text + "\t\t}\n"
    
    return cpp_file_text
    
def build_cpp(npc_list):
    cpp_file_text = ""
    cpp_file_text = cpp_file_text + "#include \"mbed.h\"\n"
    cpp_file_text = cpp_file_text + "#include \"npc_defines.h\"\n"
    cpp_file_text = cpp_file_text + "#include \"npc_sprite.h\"\n"
    cpp_file_text = cpp_file_text + "\n"
    cpp_file_text = cpp_file_text + "bool assign_npc(uint8_t npc_type, npc_sprite* npc, uint32_t npc_ID, uint8_t vis_grid_x, uint8_t vis_grid_y, uint32_t loc, uint32_t world_x, uint32_t world_y, uint8_t ai, uint32_t update_rate) {\n"
    cpp_file_text = cpp_file_text + "\tbool success = true;\n"
    cpp_file_text = cpp_file_text + "\tswitch (npc_type) {\n"
    for this_npc in npc_list:
        cpp_file_text = build_npcs_cpp(cpp_file_text, this_npc)
    cpp_file_text = cpp_file_text + "\t\tdefault: {\n"
    cpp_file_text = cpp_file_text + "\t\t\tsuccess = false;\n"
    cpp_file_text = cpp_file_text + "\t\t\tbreak;\n"
    cpp_file_text = cpp_file_text + "\t\t}\n"
    cpp_file_text = cpp_file_text + "\t}\n"
    cpp_file_text = cpp_file_text + "\t\n"
    cpp_file_text = cpp_file_text + "\treturn success;\n"
    cpp_file_text = cpp_file_text + "}\n"
    
    ###############################################################################
    # Save the files
    ###############################################################################
    f_h = open("/home/pi/Documents/mbed_Graphics/output_npcs/npc_defines.cpp", mode="w")
    f_h.write(cpp_file_text)
    f_h.close()
    
    

npc_list = pd.Series()
npc = NPC()
npc.set_NPC_details("empty", 0)
npc.set_left(7, 7, 0, 0)
npc.set_right(7, 7, 0, 0)
npc.set_up(7, 7, 0, 0)
npc.set_down(7, 7, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("player", 1)
npc.set_left(20, 21, 1, 1)
npc.set_right(20, 21, 0, 0)
npc.set_up(16, 17, 0, 0)
npc.set_down(18, 19, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("skeleman", 2)
npc.set_left(30, 31, 1, 1)
npc.set_right(30, 31, 0, 0)
npc.set_up(28, 29, 0, 0)
npc.set_down(24, 25, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("skelemage", 3)
npc.set_left(34, 35, 1, 1)
npc.set_right(34, 35, 0, 0)
npc.set_up(32, 33, 0, 0)
npc.set_down(26, 27, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("slimedood", 4)
npc.set_left(40, 41, 1, 1)
npc.set_right(40, 41, 0, 0)
npc.set_up(38, 39, 0, 0)
npc.set_down(36, 37, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("femalenpc2", 5)
npc.set_left(49, 50, 1, 1)
npc.set_right(49, 50, 0, 0)
npc.set_up(47, 48, 0, 0)
npc.set_down(45, 46, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("angryslime", 6)
npc.set_left(74, 75, 1, 1)
npc.set_right(74, 75, 0, 0)
npc.set_up(72, 73, 0, 0)
npc.set_down(70, 71, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("ratto", 7)
npc.set_left(89, 90, 1, 1)
npc.set_right(89, 90, 0, 0)
npc.set_up(87, 88, 0, 0)
npc.set_down(85, 86, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("magidude", 8)
npc.set_left(105, 106, 1, 1)
npc.set_right(105, 106, 0, 0)
npc.set_up(103, 104, 0, 0)
npc.set_down(101, 102, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("mage", 9)
npc.set_left(111, 112, 1, 1)
npc.set_right(111, 112, 0, 0)
npc.set_up(109, 110, 0, 0)
npc.set_down(107, 108, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("frogman", 10)
npc.set_left(117, 118, 1, 1)
npc.set_right(117, 118, 0, 0)
npc.set_up(115, 116, 0, 0)
npc.set_down(113, 114, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("slimecat", 11)
npc.set_left(136, 137, 1, 1)
npc.set_right(136, 137, 0, 0)
npc.set_up(134, 135, 0, 0)
npc.set_down(132, 133, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("bandit", 12)
npc.set_left(155, 156, 1, 1)
npc.set_right(155, 156, 0, 0)
npc.set_up(153, 154, 0, 0)
npc.set_down(151, 152, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("domo", 13)
npc.set_left(173, 174, 1, 1)
npc.set_right(173, 174, 0, 0)
npc.set_up(130, 131, 0, 0)
npc.set_down(128, 129, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("player2", 14)
npc.set_left(187, 188, 1, 1)
npc.set_right(187, 188, 0, 0)
npc.set_up(183, 184, 0, 0)
npc.set_down(185, 186, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("player3", 15)
npc.set_left(193, 194, 1, 1)
npc.set_right(193, 194, 0, 0)
npc.set_up(191, 192, 0, 0)
npc.set_down(189, 190, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("penguin", 16)
npc.set_left(219, 220, 0, 0)
npc.set_right(219, 220, 1, 1)
npc.set_up(217, 218, 0, 0)
npc.set_down(215, 216, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("goblinvillagerM", 17)
npc.set_left(355, 356, 1, 1)
npc.set_right(355, 356, 0, 0)
npc.set_up(353, 354, 0, 0)
npc.set_down(351, 352, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("hobgoblinvillagerM", 18)
npc.set_left(361, 362, 1, 1)
npc.set_right(361, 362, 0, 0)
npc.set_up(359, 360, 0, 0)
npc.set_down(357, 358, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("goblinguard", 19)
npc.set_left(367, 368, 1, 1)
npc.set_right(367, 368, 0, 0)
npc.set_up(365, 366, 0, 0)
npc.set_down(363, 364, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("goblinflameguard", 20)
npc.set_left(373, 374, 1, 1)
npc.set_right(373, 374, 0, 0)
npc.set_up(371, 372, 0, 0)
npc.set_down(369, 370, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

npc = NPC()
npc.set_NPC_details("malehumannpc", 21)
npc.set_left(410, 411, 1, 1)
npc.set_right(410, 411, 0, 0)
npc.set_up(42, 43, 0, 0)
npc.set_down(22, 23, 0, 0)
npc.set_alpha_pixel(28)
this_npc = pd.Series(npc, index=[npc.NPC_id])
npc_list = npc_list.append(this_npc)

build_h(npc_list)
build_cpp(npc_list)