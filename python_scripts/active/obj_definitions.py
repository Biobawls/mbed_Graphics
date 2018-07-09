#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon July 03 00:00:00 2018

@author: Biobawls
"""

import pandas as pd

class OBJ():
    def __init__(self):
        self.sprite = 0
        self.sprite_index = 0
        self.alpha_pixel = 0
        
        self.OBJ_id = ""
        self.OBJ_id_num = 0
        
        self.collision = 0
        
    def set_OBJ_details(self, id_string, id_num):
        self.OBJ_id = id_string
        self.OBJ_id_num = id_num
        
    def set_sprite(self, sprite, sprite_index, alpha_pixel):
        self.sprite = sprite
        self.sprite_index = sprite_index
        self.alpha_pixel = alpha_pixel
        
    def set_collision(self, collision):
        self.collision = collision
        
    def createCopy(self):
        new_obj = OBJ()
        new_obj.set_OBJ_details(self.OBJ_id, self.OBJ_id_num)
        new_obj.set_sprite(self.sprite, self.sprite_index, self.alpha_pixel)
        new_obj.set_collision(self.collision)
        return(new_obj)
    
def build_objs_h(h_file_text, obj_in):
    if obj_in.OBJ_id == "nothing":
        pass
    else:
        h_file_text = h_file_text + "const static uint16_t " + obj_in.OBJ_id + "_sprite_array[1] = {" + str(obj_in.sprite) + "};\n"
        h_file_text = h_file_text + "const static uint8_t " + obj_in.OBJ_id + "_sprite_indexing[1] = {" + str(obj_in.sprite_index) + "};\n"
    return h_file_text

def build_h(obj_list):
    h_file_text = ""
    h_file_text = h_file_text + "#ifndef OBJ_DEFINES_H\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "#include \"mbed.h\"\n"
    h_file_text = h_file_text + "#include \"obj_sprite.h\"\n"
    h_file_text = h_file_text + "\n"
    for this_obj in obj_list:
        h_file_text = build_objs_h(h_file_text, this_obj)
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "bool assign_obj(uint8_t obj_type, obj_sprite* obj, uint32_t obj_ID, uint8_t vis_grid_x, uint8_t vis_grid_y, uint32_t loc, uint32_t world_x, uint32_t world_y, bool colli_in, bool render_ontop_in);\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "#endif\n"
    
    ###############################################################################
    # Save the files
    ###############################################################################
    f_h = open("/home/pi/Documents/mbed_Graphics/output_objects/obj_defines.h", mode="w")
    f_h.write(h_file_text)
    f_h.close()

def build_objs_cpp(cpp_file_text, obj_in):
    if obj_in.OBJ_id == "nothing":
        return cpp_file_text
    
    cpp_file_text = cpp_file_text + "\t\tcase " + str(obj_in.OBJ_id_num) + ": {\n"
    cpp_file_text = cpp_file_text + "\t\t\tobj->init(obj_ID, 0, 0, vis_grid_x, vis_grid_y, loc%world_x, loc/world_x, world_x, world_y, " + obj_in.OBJ_id + "_sprite_array, " + obj_in.OBJ_id + "_sprite_indexing, " + str(obj_in.alpha_pixel) + ");\n"
    cpp_file_text = cpp_file_text + "\t\t\tbreak;\n"
    cpp_file_text = cpp_file_text + "\t\t}\n"
    
    return cpp_file_text

def build_cpp(obj_list):
    cpp_file_text = ""
    cpp_file_text = cpp_file_text + "#include \"mbed.h\"\n"
    cpp_file_text = cpp_file_text + "#include \"obj_defines.h\"\n"
    cpp_file_text = cpp_file_text + "#include \"obj_sprite.h\"\n"
    cpp_file_text = cpp_file_text + "\n"
    cpp_file_text = cpp_file_text + "bool assign_obj(uint8_t obj_type, obj_sprite* obj, uint32_t obj_ID, uint8_t vis_grid_x, uint8_t vis_grid_y, uint32_t loc, uint32_t world_x, uint32_t world_y, bool colli_in, bool render_ontop_in) {\n"
    cpp_file_text = cpp_file_text + "\tbool success = true;\n"
    cpp_file_text = cpp_file_text + "\tswitch (obj_type) {\n"
    for this_obj in obj_list:
        cpp_file_text = build_objs_cpp(cpp_file_text, this_obj)
    cpp_file_text = cpp_file_text + "\t\tdefault: {\n"
    cpp_file_text = cpp_file_text + "\t\t\tsuccess = false;\n"
    cpp_file_text = cpp_file_text + "\t\t\tbreak;\n"
    cpp_file_text = cpp_file_text + "\t\t}\n"
    cpp_file_text = cpp_file_text + "\t}\n"
    cpp_file_text = cpp_file_text + "\tif (colli_in == true) {\n"
    cpp_file_text = cpp_file_text + "\t\tobj->enable_collision();\n"
    cpp_file_text = cpp_file_text + "\t} else {\n"
    cpp_file_text = cpp_file_text + "\t\tobj->disable_collision();\n"
    cpp_file_text = cpp_file_text + "\t}\n"
    cpp_file_text = cpp_file_text + "\tif (render_ontop_in == true) {\n"
    cpp_file_text = cpp_file_text + "\t\tobj->render_top();\n"
    cpp_file_text = cpp_file_text + "\t} else {\n"
    cpp_file_text = cpp_file_text + "\t\tobj->render_bottom();\n"
    cpp_file_text = cpp_file_text + "\t}\n"
    cpp_file_text = cpp_file_text + "\t\n"
    cpp_file_text = cpp_file_text + "\treturn success;\n"
    cpp_file_text = cpp_file_text + "}\n"
    
    ###############################################################################
    # Save the files
    ###############################################################################
    f_h = open("/home/pi/Documents/mbed_Graphics/output_objects/obj_defines.cpp", mode="w")
    f_h.write(cpp_file_text)
    f_h.close()


obj_list = pd.Series()
obj = OBJ()
obj.set_OBJ_details("nothing", 0)
obj.set_sprite(7, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("emptyobj", 1)
obj.set_sprite(7, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("pot", 2)
obj.set_sprite(95, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("chairL", 3)
obj.set_sprite(99, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("chairR", 4)
obj.set_sprite(99, 1, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("tableS", 5)
obj.set_sprite(98, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("firewall", 6)
obj.set_sprite(237, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("iceprison", 7)
obj.set_sprite(236, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("lava", 8)
obj.set_sprite(12, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("chestclosed", 9)
obj.set_sprite(144, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("chestopen", 10)
obj.set_sprite(268, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("carpetTL", 11)
obj.set_sprite(287, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("carpetT", 12)
obj.set_sprite(286, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("carpetTR", 13)
obj.set_sprite(322, 4, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("carpetML", 14)
obj.set_sprite(286, 7, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("carpetM", 15)
obj.set_sprite(283, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("carpetMR", 16)
obj.set_sprite(286, 3, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("carpetBL", 17)
obj.set_sprite(322, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("carpetB", 18)
obj.set_sprite(286, 4, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("carpetBR", 19)
obj.set_sprite(287, 4, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("tableLL", 20)
obj.set_sprite(96, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("tableLR", 21)
obj.set_sprite(97, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("pottedplant", 22)
obj.set_sprite(100, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("bookshelfB", 23)
obj.set_sprite(170, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("bookshelfT", 24)
obj.set_sprite(171, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("sofaSR", 25)
obj.set_sprite(288, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("sofaSL", 26)
obj.set_sprite(288, 1, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("softchairR", 27)
obj.set_sprite(289, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("softchairG", 28)
obj.set_sprite(290, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("shield", 29)
obj.set_sprite(291, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("singlecandlelit", 30)
obj.set_sprite(292, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("singlecandleunlit", 31)
obj.set_sprite(295, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("threecandlelit", 32)
obj.set_sprite(293, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("threecandleunlit", 33)
obj.set_sprite(294, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("threebluecandlelit", 34)
obj.set_sprite(296, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("threesilvercandlelit", 35)
obj.set_sprite(297, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("threesilvercandleunlit", 36)
obj.set_sprite(298, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("wallsilvercandlelit", 37)
obj.set_sprite(300, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("wallsilvercandleunlit", 38)
obj.set_sprite(299, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("wallcandlelit", 39)
obj.set_sprite(301, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("wallcandleunlit", 40)
obj.set_sprite(302, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("wallshieldcandlelit", 41)
obj.set_sprite(304, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("wallshieldcandleunlit", 42)
obj.set_sprite(303, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("redbedT", 43)
obj.set_sprite(324, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("redbedB", 44)
obj.set_sprite(325, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("smallwindow", 45)
obj.set_sprite(14, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("boiler", 46)
obj.set_sprite(15, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("cabinet", 47)
obj.set_sprite(305, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("emptydesk", 48)
obj.set_sprite(306, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("inkwelldesk", 49)
obj.set_sprite(307, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("greenpotdesk", 50)
obj.set_sprite(308, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("redpotdesk", 51)
obj.set_sprite(309, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("alchdesk", 52)
obj.set_sprite(310, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("writedesk", 53)
obj.set_sprite(311, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("furnace", 54)
obj.set_sprite(318, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("bluebedtop", 55)
obj.set_sprite(326, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("bluebedbottom", 56)
obj.set_sprite(327, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

obj = OBJ()
obj.set_OBJ_details("firevortex", 57)
obj.set_sprite(415, 0, 28)
this_obj = pd.Series(obj, index=[obj.OBJ_id])
obj_list = obj_list.append(this_obj)

build_h(obj_list)
build_cpp(obj_list)