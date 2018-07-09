#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon July 03 00:00:00 2018

@author: Biobawls
"""

import pandas as pd

class ITEM():
    def __init__(self):
        self.ITEM_id = ""
        self.ITEM_id_num = 0
        
        self.sprite = 7
        
        self.item_display_text = ""
        self.attack = 0
        # 0 = physical, 1 = fire, 2 = ice, 3 = arcane, 4 = nature, 5 = light, 6 = dark
        self.attribute = 0
        self.skill_assignment = 0
        self.alpha_pixel = 28
        self.use = 0
        self.equip = 0
        
        self.in_list_index = 0
        
    def set_ITEM_details(self, id_string, id_num):
        self.ITEM_id = id_string
        self.ITEM_id_num = id_num
        
    def set_sprite(self, sprite, alpha_pixel):
        self.sprite = sprite
        self.alpha_pixel = alpha_pixel
        
    def set_item_display_text(self, text_in):
        if len(text_in) > 10:
            pass
        else:
            self.item_display_text = text_in
        
    def set_stats(self, attack, attribute):
        self.attack = attack
        self.attribute = attribute
        
    def set_skill(self, skill_number):
        self.skill_assignment = skill_number
        
    def set_interaction(self, use, equip):
        self.use = use
        self.equip = equip
        
    def set_global_index(self, ind_in):
        self.in_list_index = ind_in
        
    def createCopy(self):
        new_item = ITEM()
        new_item.set_ITEM_details(self.ITEM_id, self.ITEM_id_num)
        new_item.set_sprite(self.sprite, self.alpha_pixel)
        new_item.set_item_display_text(self.item_display_text)
        new_item.set_stats(self.attack, self.attribute)
        new_item.set_skill(self.skill_assignment)
        new_item.set_interaction(self.use, self.equip)
        new_item.set_global_index(self.in_list_index)
        return new_item

def build_items_h(h_file_text, item_in):
    if item_in.sprite == 7:
        return h_file_text
    else:
        return h_file_text + "const static uint16_t " + item_in.ITEM_id + "_sprite_array[1] = {" + str(item_in.sprite) + "};\n"

def build_h(item_list):
    h_file_text = ""
    h_file_text = h_file_text + "#ifndef ITEMS_H\n"
    h_file_text = h_file_text + "#define ITEMS_H\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "#include \"mbed.h\"\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "////////////////////////////////////////////////////////////////////////////////\n"
    h_file_text = h_file_text + "// sprite index in ROM\n"
    h_file_text = h_file_text + "////////////////////////////////////////////////////////////////////////////////\n"
    for this_item in item_list:
        h_file_text = build_items_h(h_file_text, this_item)
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "class items {\n"
    h_file_text = h_file_text + "\tpublic:\n"
    h_file_text = h_file_text + "\t\titems(void){\n"
    h_file_text = h_file_text + "\t\t\tuint8_t i_8 = 0;\n"
    h_file_text = h_file_text + "\t\t\t\n"
    h_file_text = h_file_text + "\t\t\tsprite_array = NULL;\n"
    h_file_text = h_file_text + "\t\t\t\n"
    h_file_text = h_file_text + "\t\t\tattribute = 0;\n"
    h_file_text = h_file_text + "\t\t\tstats.attack = 1;\n"
    h_file_text = h_file_text + "\t\t\tskill_assign = 255;\n"
    h_file_text = h_file_text + "\t\t\t\n"
    h_file_text = h_file_text + "\t\t\tcan_use = false;\n"
    h_file_text = h_file_text + "\t\t\tcan_equip = false;\n"
    h_file_text = h_file_text + "\t\t\t\n"
    h_file_text = h_file_text + "\t\t\tfor (i_8 = 0; i_8 < item_name_char_limit; i_8++) {\n"
    h_file_text = h_file_text + "\t\t\t\titem_name[i_8] = 0;\n"
    h_file_text = h_file_text + "\t\t\t}\n"
    h_file_text = h_file_text + "\t\t\t\n"
    h_file_text = h_file_text + "\t\t\treturn;\n"
    h_file_text = h_file_text + "\t\t};\n"
    h_file_text = h_file_text + "\t\t\n"
    h_file_text = h_file_text + "\t\tvoid init(char* item_name_in, const uint16_t *sa_in, uint8_t attack_in, uint8_t attrib_in, uint8_t skill_assign_in, uint8_t a_pix, bool use_in, bool equip_in);\n"
    h_file_text = h_file_text + "\t\t\n"
    h_file_text = h_file_text + "\t\tconst uint16_t *sprite_array;\n"
    h_file_text = h_file_text + "\t\tuint8_t alpha_channel;\n"
    h_file_text = h_file_text + "\t\t\n"
    h_file_text = h_file_text + "\t\t// attribute numbers: 0 = physical, 1 = fire, 2 = ice, 3 = arcane, 4 = nature, 5 = light, 6 = dark\n"
    h_file_text = h_file_text + "\t\tuint8_t attribute;\n"
    h_file_text = h_file_text + "\t\t\n"
    h_file_text = h_file_text + "\t\tuint8_t skill_assign;\n"
    h_file_text = h_file_text + "\t\t\n"
    h_file_text = h_file_text + "\t\tstatic const uint8_t item_name_char_limit = 11;\n"
    h_file_text = h_file_text + "\t\tchar item_name[item_name_char_limit];\n"
    h_file_text = h_file_text + "\t\t\n"
    h_file_text = h_file_text + "\t\tstruct stats_struct {\n"
    h_file_text = h_file_text + "\t\t\t// Combat\n"
    h_file_text = h_file_text + "\t\t\tint16_t attack;\n"
    h_file_text = h_file_text + "\t\t} stats;\n"
    h_file_text = h_file_text + "\t\t\n"
    h_file_text = h_file_text + "\t\tbool can_use;\n"
    h_file_text = h_file_text + "\t\tbool can_equip;\n"
    h_file_text = h_file_text + "};\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "bool assign_item(uint8_t choice, items* container);\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "#endif\n"

    ###############################################################################
    # Save the files
    ###############################################################################
    f_h = open("/home/pi/Documents/mbed_Graphics/output_items/items.h", mode="w")
    f_h.write(h_file_text)
    f_h.close()
    
def build_items_cpp(cpp_file_text, item_in):
    if item_in.use == 0:
        use_bool = "false"
    elif item_in.use == 1:
        use_bool = "true"
    else:
        use_bool = "ERROR"

    if item_in.equip == 0:
        equip_bool = "false"
    elif item_in.equip == 1:
        equip_bool = "true"
    else:
        equip_bool = "ERROR"
        
    if item_in.ITEM_id == "nothing":
        return cpp_file_text
    
    if item_in.sprite == 7:
        sprite_ptr = "NULL"
    else:
        sprite_ptr = str(item_in.ITEM_id) + "_sprite_array"
    
    cpp_file_text = cpp_file_text + "\t\tcase " + str(item_in.ITEM_id_num) + ": {\n"
    cpp_file_text = cpp_file_text + "\t\t\tcontainer->init(\"" + item_in.item_display_text +  "\", " + sprite_ptr + ", " + str(item_in.attack) + ", " + str(item_in.attribute) + ", " + str(item_in.skill_assignment) + ", " + str(item_in.alpha_pixel) + ", " + use_bool + ", " + equip_bool + ");\n"
    cpp_file_text = cpp_file_text + "\t\t\tbreak;\n"
    cpp_file_text = cpp_file_text + "\t\t}\n"
    
    return cpp_file_text
    
def build_cpp(item_list):
    cpp_file_text = ""
    cpp_file_text = cpp_file_text + "#include \"mbed.h\"\n"
    cpp_file_text = cpp_file_text + "#include \"items.h\"\n"
    cpp_file_text = cpp_file_text + "#include \"effects.h\"\n"
    cpp_file_text = cpp_file_text + "\n"
    cpp_file_text = cpp_file_text + "////////////////////////////////////////////////////////////////////////////////\n"
    cpp_file_text = cpp_file_text + "void items::init(char* item_name_in, const uint16_t *sa_in, uint8_t attack_in, uint8_t attrib_in, uint8_t skill_assign_in, uint8_t a_pix, bool use_in, bool equip_in) {\n"
    cpp_file_text = cpp_file_text + "\tuint8_t i_8;\n"
    cpp_file_text = cpp_file_text + "\t\n"
    cpp_file_text = cpp_file_text + "\tsprite_array = sa_in;\n"
    cpp_file_text = cpp_file_text + "\talpha_channel = a_pix;\n"
    cpp_file_text = cpp_file_text + "\tattribute = attrib_in;\n"
    cpp_file_text = cpp_file_text + "\tskill_assign = skill_assign_in;\n"
    cpp_file_text = cpp_file_text + "\tstats.attack = attack_in;\n"
    cpp_file_text = cpp_file_text + "\tcan_use = use_in;\n"
    cpp_file_text = cpp_file_text + "\tcan_equip = equip_in;\n"
    cpp_file_text = cpp_file_text + "\t\n"
    cpp_file_text = cpp_file_text + "\tfor (i_8 = 0; i_8 < item_name_char_limit-1; i_8++) {\n"
    cpp_file_text = cpp_file_text + "\t\titem_name[i_8] = item_name_in[i_8];\n"
    cpp_file_text = cpp_file_text + "\t}\n"
    cpp_file_text = cpp_file_text + "\titem_name[item_name_char_limit-1] = 0;\n"
    cpp_file_text = cpp_file_text + "\t\n"
    cpp_file_text = cpp_file_text + "\treturn;\n"
    cpp_file_text = cpp_file_text + "}\n"
    cpp_file_text = cpp_file_text + "////////////////////////////////////////////////////////////////////////////////\n"
    cpp_file_text = cpp_file_text + "bool assign_item(uint8_t choice, items* container) {\n"
    cpp_file_text = cpp_file_text + "\tbool success = true;\n"
    cpp_file_text = cpp_file_text + "\t\n"
    cpp_file_text = cpp_file_text + "\tswitch (choice) {\n"
    for this_item in item_list:
        cpp_file_text = build_items_cpp(cpp_file_text, this_item)
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
    f_h = open("/home/pi/Documents/mbed_Graphics/output_items/items.cpp", mode="w")
    f_h.write(cpp_file_text)
    f_h.close()



item_list = pd.Series()
item = ITEM()
item.set_ITEM_details("nothing", 0)
this_item = pd.Series(item, index=[item.ITEM_id])
item_list = item_list.append(this_item)

item = ITEM()
item.set_ITEM_details("rusty_dagger", 1)
item.set_sprite(252, 28)
item.set_item_display_text("RUSTY DGR ")
item.set_stats(1, 0)
item.set_skill(0)
item.set_interaction(0, 1)
this_item = pd.Series(item, index=[item.ITEM_id])
item_list = item_list.append(this_item)

item = ITEM()
item.set_ITEM_details("copper_dagger", 2)
item.set_sprite(253, 28)
item.set_item_display_text("COPPER DGR")
item.set_stats(2, 0)
item.set_skill(0)
item.set_interaction(0, 1)
this_item = pd.Series(item, index=[item.ITEM_id])
item_list = item_list.append(this_item)

item = ITEM()
item.set_ITEM_details("iron_dagger", 3)
item.set_sprite(254, 28)
item.set_item_display_text("IRON DGR  ")
item.set_stats(3, 0)
item.set_skill(0)
item.set_interaction(0, 1)
this_item = pd.Series(item, index=[item.ITEM_id])
item_list = item_list.append(this_item)

item = ITEM()
item.set_ITEM_details("silver_dagger", 4)
item.set_sprite(255, 28)
item.set_item_display_text("SILVER DGR")
item.set_stats(4, 0)
item.set_skill(0)
item.set_interaction(0, 1)
this_item = pd.Series(item, index=[item.ITEM_id])
item_list = item_list.append(this_item)

item = ITEM()
item.set_ITEM_details("gold_dagger", 5)
item.set_sprite(256, 28)
item.set_item_display_text("GOLD DGR  ")
item.set_stats(5, 0)
item.set_skill(0)
item.set_interaction(0, 1)
this_item = pd.Series(item, index=[item.ITEM_id])
item_list = item_list.append(this_item)

item = ITEM()
item.set_ITEM_details("self_heal", 6)
item.set_item_display_text("SELFHEAL  ")
item.set_stats(1, 2)
item.set_skill(4)
item.set_interaction(1, 0)
this_item = pd.Series(item, index=[item.ITEM_id])
item_list = item_list.append(this_item)

item = ITEM()
item.set_ITEM_details("rusty_spear", 7)
item.set_sprite(275, 28)
item.set_item_display_text("RUSTY SPR ")
item.set_stats(1, 0)
item.set_skill(1)
item.set_interaction(1, 0)
this_item = pd.Series(item, index=[item.ITEM_id])
item_list = item_list.append(this_item)

build_h(item_list)
build_cpp(item_list)

