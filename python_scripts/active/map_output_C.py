#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon July 03 00:00:00 2018

@author: Biobawls
"""

import numpy as np
import re

def output_map_CPP(map_name_in, map_x_in, map_y_in, map_array_in, collision_array_in, npc_obj_array_in, spawns_array_in, obj_obj_array_in, item_obj_array_in):
    map_name = map_name_in
    map_x = np.uint32(map_x_in)
    map_y = np.uint32(map_y_in)
    map_n = map_x * map_y
    
    # values = sprite number
    map_array = map_array_in
    # 0 = collide, 1 = np collide, anything else = warp to number number
    collision_array = collision_array_in
    #npc_obj_array = np.empty(map_n, dtype=NPC)
    npc_obj_array = npc_obj_array_in
    # true = can spawn, false = can't spawn
    spawns_array = spawns_array_in
    #obj_obj_array = np.empty(map_n, dtype=OBJ)
    obj_obj_array = obj_obj_array_in
    #item_obj_array = np.empty(map_n, dtype=ITEM)
    item_obj_array = item_obj_array_in
    
    # number of npcs
    npc_n = np.uint8(0)
    # number of objs
    obj_n = np.uint8(0)
    # number of items
    item_n = np.uint8(0)
    for ii in range(0, map_n):
        if npc_obj_array[ii].NPC_id_num != 0:
            npc_n = npc_n + 1
        if obj_obj_array[ii].OBJ_id_num != 0:
            obj_n = obj_n + 1
        if item_obj_array[ii].ITEM_id_num != 0:
            item_n = item_n + 1

    # NPC type number
    npc_LUT = np.zeros(npc_n, dtype='uint8')
    # ai type - half the size of NPC_LUT
    npc_move = np.zeros(npc_n, dtype='uint8')
    # npc text
    npc_text = []
    # npc position
    npc_pos = np.zeros(npc_n, dtype='uint32')
    # OBJ type number
    obj_LUT = np.zeros(obj_n, dtype='uint8')
    # obj position
    obj_pos = np.zeros(obj_n, dtype='uint32')
    # obj has collision
    obj_colli = np.zeros(obj_n, dtype='bool')
    # ITEM type number
    item_LUT = np.zeros(item_n, dtype='uint8')
    # item position
    item_pos = np.zeros(item_n, dtype='uint32')
    # item number in the global item list
    item_in_list = np.zeros(item_n, dtype='uint8')
    jj = 0
    kk = 0
    ll = 0
    for ii in range(0, map_n):
        if npc_obj_array[ii].NPC_id_num != 0:
            npc_LUT[jj] = npc_obj_array[ii].NPC_id_num
            npc_move[jj] = npc_obj_array[ii].ai
            npc_text.append(npc_obj_array[ii].text)
            npc_pos[jj] = ii
            jj = jj + 1
        if obj_obj_array[ii].OBJ_id_num != 0:
            obj_LUT[kk] = obj_obj_array[ii].OBJ_id_num
            obj_colli[kk] = obj_obj_array[ii].collision
            obj_pos[kk] = ii
            kk = kk + 1
        if item_obj_array[ii].ITEM_id_num != 0:
            item_LUT[ll] = item_obj_array[ii].ITEM_id_num
            item_in_list[ll] = item_obj_array[ii].in_list_index
            item_pos[ll] = ii
            ll = ll + 1
    
    # number of types of npc
    #dicta = {}
    #for ii in range(0, npc_list.size):
    #    dicta[ii] = sum(npc_LUT[1::2] == ii)
    
    ###############################################################################
    # Build the .h file:
    ###############################################################################
    h_file_text = ""
    h_file_text = h_file_text + "struct " + map_name + "_struct {\n"
    h_file_text = h_file_text + "\tconst static uint32_t world_y = " + str(map_y) + ";\n"
    h_file_text = h_file_text + "\tconst static uint32_t world_x = " + str(map_x) + ";\n"
    h_file_text = h_file_text + "\tconst static uint32_t world_n = " + str(map_n) + ";\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "\tconst static uint16_t map[];\n"
    h_file_text = h_file_text + "\tconst static uint8_t collision[];\n"
    h_file_text = h_file_text + "\tconst static bool spawns[];\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "\tconst static uint8_t npc_n = " + str(npc_n) + ";\n"
    h_file_text = h_file_text + "\tconst static uint8_t npc_LUT[];\n"
    h_file_text = h_file_text + "\tconst static uint8_t npc_move[];\n"
    h_file_text = h_file_text + "\tstatic const std::string npc_text[];\n"
    h_file_text = h_file_text + "\tconst static uint32_t npc_pos[];\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "\tconst static uint8_t obj_n = " + str(obj_n) + ";\n"
    h_file_text = h_file_text + "\tconst static uint8_t obj_LUT[];\n"
    h_file_text = h_file_text + "\tconst static uint32_t obj_pos[];\n"
    h_file_text = h_file_text + "\tconst static bool obj_colli[];\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "\tconst static uint8_t item_n = " + str(item_n) + ";\n"
    h_file_text = h_file_text + "\tconst static uint8_t item_LUT[];\n"
    h_file_text = h_file_text + "\tconst static uint32_t item_pos[];\n"
    h_file_text = h_file_text + "\tconst static uint8_t item_in_list[];\n"
    h_file_text = h_file_text + "};\n"
        
    ###############################################################################
    # Build the .cpp file:
    ###############################################################################
    cpp_file_text = ""
    cpp_file_text = cpp_file_text + "const uint16_t " + map_name + "_struct::map[] = {"
    for ii in range(0, map_y):
        for jj in range(0, map_x):
            cpp_file_text = cpp_file_text + str(map_array[jj + (ii*map_x)]) + ","
        cpp_file_text = cpp_file_text + "\n"
    cpp_file_text = cpp_file_text[:-2]
    cpp_file_text = cpp_file_text + "};\n"
    cpp_file_text = cpp_file_text + "\n"
    
    cpp_file_text = cpp_file_text + "const uint8_t " + map_name + "_struct::collision[] = {"
    for ii in range(0, map_y):
        for jj in range(0, map_x):
            cpp_file_text = cpp_file_text + str(collision_array[jj + (ii*map_x)]) + ","
        cpp_file_text = cpp_file_text + "\n"
    cpp_file_text = cpp_file_text[:-2]
    cpp_file_text = cpp_file_text + "};\n"
    cpp_file_text = cpp_file_text + "\n"
    
    cpp_file_text = cpp_file_text + "const bool " + map_name + "_struct::spawns[] = {"
    for ii in range(0, map_y):
        for jj in range(0, map_x):
            cpp_file_text = cpp_file_text + str(spawns_array[jj + (ii*map_x)]) + ","
        cpp_file_text = cpp_file_text + "\n"
    cpp_file_text = cpp_file_text[:-2]
    cpp_file_text = cpp_file_text + "};\n"
    cpp_file_text = cpp_file_text + "\n"
    
    temp = ""
    for ii in range(0, len(npc_LUT)):
        if ii == len(npc_LUT)-1:
            temp = temp + str(npc_LUT[ii])
        else:
            temp = temp + str(npc_LUT[ii]) + ","
    cpp_file_text = cpp_file_text + "const uint8_t " + map_name + "_struct::npc_LUT[] = {" + temp + "};\n"
    
    temp = ""
    for ii in range(0, len(npc_move)):
        if ii == len(npc_move)-1:
            temp = temp + str(npc_move[ii])
        else:
            temp = temp + str(npc_move[ii]) + ","
    cpp_file_text = cpp_file_text + "const uint8_t " + map_name + "_struct::npc_move[] = {" + temp + "};\n"
    
    temp = ""
    for ii in range(0, len(npc_text)):
        if ii == len(npc_text)-1:
            temp = temp + "\"" + npc_text[ii] + "\""
        else:
            temp = temp + "\"" + npc_text[ii] + "\"" + ","
    cpp_file_text = cpp_file_text + "const std::string " + map_name + "_struct::npc_text[] = {" + temp + "};\n"
    
    temp = ""
    for ii in range(0, len(npc_pos)):
        if ii == len(npc_pos)-1:
            temp = temp + str(npc_pos[ii])
        else:
            temp = temp + str(npc_pos[ii]) + ","
    cpp_file_text = cpp_file_text + "const uint32_t " + map_name + "_struct::npc_pos[] = {" + temp + "};\n"
    
    temp = ""
    for ii in range(0, len(obj_LUT)):
        if ii == len(obj_LUT)-1:
            temp = temp + str(obj_LUT[ii])
        else:
            temp = temp + str(obj_LUT[ii]) + ","
    cpp_file_text = cpp_file_text + "const uint8_t " + map_name + "_struct::obj_LUT[] = {" + temp + "};\n"
    
    temp = ""
    for ii in range(0, len(obj_pos)):
        if ii == len(obj_pos)-1:
            temp = temp + str(obj_pos[ii])
        else:
            temp = temp + str(obj_pos[ii]) + ","
    cpp_file_text = cpp_file_text + "const uint32_t " + map_name + "_struct::obj_pos[] = {" + temp + "};\n"
    
    temp = ""
    for ii in range(0, len(obj_colli)):
        if ii == len(obj_colli)-1:
            temp = temp + str(obj_colli[ii])
        else:
            temp = temp + str(obj_colli[ii]) + ","
    cpp_file_text = cpp_file_text + "const bool " + map_name + "_struct::obj_colli[] = {" + temp + "};\n"
    
    temp = ""
    for ii in range(0, len(item_LUT)):
        if ii == len(item_LUT)-1:
            temp = temp + str(item_LUT[ii])
        else:
            temp = temp + str(item_LUT[ii]) + ","
    cpp_file_text = cpp_file_text + "const uint8_t " + map_name + "_struct::item_LUT[] = {" + temp + "};\n"
    
    temp = ""
    for ii in range(0, len(item_pos)):
        if ii == len(item_pos)-1:
            temp = temp + str(item_pos[ii])
        else:
            temp = temp + str(item_pos[ii]) + ","
    cpp_file_text = cpp_file_text + "const uint32_t " + map_name + "_struct::item_pos[] = {" + temp + "};\n"
    
    temp = ""
    for ii in range(0, len(item_in_list)):
        if ii == len(item_in_list)-1:
            temp = temp + str(item_in_list[ii])
        else:
            temp = temp + str(item_in_list[ii]) + ","
    cpp_file_text = cpp_file_text + "const uint8_t " + map_name + "_struct::item_in_list[] = {" + temp + "};\n"
    
    ###############################################################################
    # Save the files
    ###############################################################################
    f_h = open("/home/pi/Documents/mbed_Graphics/output_maps/" + map_name_in + ".h", mode="w")
    f_h.write(h_file_text)
    f_h.close()
    
    f_cpp = open("/home/pi/Documents/mbed_Graphics/output_maps/" + map_name_in + ".cpp", mode="w")
    f_cpp.write(cpp_file_text)
    f_cpp.close()

def read_map_CPP(cpp_file_in):
    f_cpp = open(cpp_file_in, mode="r")
    content = f_cpp.readlines()
    f_cpp.close()
    dicta_names = ["map_array", "collision_array", "spawns_array", "npc_LUT", "npc_ai", "npc_text", "npc_pos", "obj_LUT", "obj_pos", "obj_collision", "item_LUT", "item_pos", "item_in_list"]
    dicta = {}
    kk = 0
    incr = 0;
    for ii in range(0, len(content)):
        content[ii] = content[ii].strip()
        a = content[ii].split("{", 1)
        if len(a) == 2:
            content[ii] = a[1]
        else:
            content[ii] = a[0]
        a = content[ii].split("};", 1)
        if len(a) == 2:
            content[ii] = a[0]
            incr = 1
        else:
            incr = 0
        if dicta_names[kk] in dicta:
            dicta[dicta_names[kk]] = dicta[dicta_names[kk]] + content[ii]
        else:
            dicta[dicta_names[kk]] = content[ii]
        kk = kk + incr
        
    for key in dicta:
        if key == "npc_text":
            #dicta[key] = dicta[key].split(",")
            dicta[key] = re.findall('"([^"]*)"', dicta[key])
        else:
            if dicta[key] == '':
                dicta[key] = 0
            else:
                if (key == "npc_pos") or (key == "obj_pos") or (key == "item_pos"):
                    dicta[key] = [np.uint32(i) for i in dicta[key].split(",")]
                elif (key == "map_array"):
                    dicta[key] = [np.uint16(i) for i in dicta[key].split(",")]
                elif key == "obj_collision":
                    dicta[key] = [np.bool(i) for i in dicta[key].split(",")]
                else:
                    dicta[key] = [np.uint8(i) for i in dicta[key].split(",")]
            
    return(dicta)

def read_map_H(h_file_in):
    f_h = open(h_file_in, mode="r")
    content = f_h.readlines()
    f_h.close()
    dicta = {}
    for ii in range(0, len(content)):
        content[ii] = content[ii].strip()
        a = content[ii].split("world_x", 1)
        if len(a) == 2:
            dicta["map_x"] = [int(s) for s in re.findall(r'\d+', a[1])]
        a = content[ii].split("world_y", 1)
        if len(a) == 2:
            dicta["map_y"] = [int(s) for s in re.findall(r'\d+', a[1])]
    
    return(dicta)

def output_map_CPP_v1(map_name_in, map_x_in, map_y_in, map_array_in, collision_array_in, npc_obj_array_in, spawns_array_in):
    map_name = map_name_in
    map_x = np.uint32(map_x_in)
    map_y = np.uint32(map_y_in)
    map_n = map_x * map_y
    
    # values = sprite number
    map_array = map_array_in
    # 0 = collide, 1 = np collide, anything else = warp to number number
    collision_array = collision_array_in
    # 0 = no npc, any number >1 is the npc number in the npc_LUT odd elements
    npc_array = np.zeros(map_n, dtype='uint8')
    #npc_obj_array = np.empty(map_n, dtype=NPC)
    npc_obj_array = npc_obj_array_in
    # true = can spawn, false = can't spawn
    spawns_array = spawns_array_in
    
    # number of npcs
    npc_n = np.uint32(0)
    ll = 2
    for ii in range(0, map_n):
        if npc_obj_array[ii].NPC_id_num != 0:
            npc_array[ii] = ll
            npc_n = npc_n + 1
            ll = ll + 1
    # pairs: ID -> NPC type
    npc_LUT = np.zeros(npc_n*2, dtype='uint8')
    # ai type - half the size of NPC_LUT
    npc_move = np.zeros(npc_n, dtype='uint8')
    # npc text
    npc_text = []
    # npc position
    npc_pos = np.zeros(npc_n, dtype='uint32')
    jj = 0
    kk = 0
    for ii in range(0, map_n):
        if npc_obj_array[ii].NPC_id_num != 0:
            npc_LUT[kk] = npc_array[ii]
            npc_text.append(npc_obj_array[ii].text)
            npc_move[jj] = npc_obj_array[ii].ai
            npc_pos[jj] = ii
            jj = jj + 1
            kk = kk + 1
            npc_LUT[kk] = npc_obj_array[ii].NPC_id_num
            kk = kk + 1
    
    # number of types of npc
    #dicta = {}
    #for ii in range(0, npc_list.size):
    #    dicta[ii] = sum(npc_LUT[1::2] == ii)
    
    ###############################################################################
    # Build the .h file:
    ###############################################################################
    h_file_text = ""
    h_file_text = h_file_text + "struct " + map_name + "_struct {\n"
    h_file_text = h_file_text + "\tconst static uint32_t world_y = " + str(map_y) + ";\n"
    h_file_text = h_file_text + "\tconst static uint32_t world_x = " + str(map_x) + ";\n"
    h_file_text = h_file_text + "\tconst static uint32_t world_n = " + str(map_n) + ";\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "\tconst static uint8_t map[];\n"
    h_file_text = h_file_text + "\tconst static uint8_t collision[];\n"
    h_file_text = h_file_text + "\tconst static bool spawns[];\n"
    h_file_text = h_file_text + "\n"
    h_file_text = h_file_text + "\tconst static uint32_t npc_n = " + str(npc_n) + ";\n"
    h_file_text = h_file_text + "\tconst static uint8_t npc_LUT[];\n"
    h_file_text = h_file_text + "\tconst static uint8_t npc_move[];\n"
    h_file_text = h_file_text + "\tstatic const std::string npc_text[];\n"
    h_file_text = h_file_text + "\tconst static uint32_t npc_pos[];\n"
    h_file_text = h_file_text + "};\n"
        
    ###############################################################################
    # Build the .cpp file:
    ###############################################################################
    cpp_file_text = ""
    cpp_file_text = cpp_file_text + "const uint8_t " + map_name + "_struct::map[] = {"
    for ii in range(0, map_y):
        for jj in range(0, map_x):
            cpp_file_text = cpp_file_text + str(map_array[jj + (ii*map_x)]) + ","
        cpp_file_text = cpp_file_text + "\n"
    cpp_file_text = cpp_file_text[:-2]
    cpp_file_text = cpp_file_text + "};\n"
    cpp_file_text = cpp_file_text + "\n"
    
    cpp_file_text = cpp_file_text + "const uint8_t " + map_name + "_struct::collision[] = {"
    for ii in range(0, map_y):
        for jj in range(0, map_x):
            cpp_file_text = cpp_file_text + str(collision_array[jj + (ii*map_x)]) + ","
        cpp_file_text = cpp_file_text + "\n"
    cpp_file_text = cpp_file_text[:-2]
    cpp_file_text = cpp_file_text + "};\n"
    cpp_file_text = cpp_file_text + "\n"
    
    cpp_file_text = cpp_file_text + "const bool " + map_name + "_struct::spawns[] = {"
    for ii in range(0, map_y):
        for jj in range(0, map_x):
            cpp_file_text = cpp_file_text + str(spawns_array[jj + (ii*map_x)]) + ","
        cpp_file_text = cpp_file_text + "\n"
    cpp_file_text = cpp_file_text[:-2]
    cpp_file_text = cpp_file_text + "};\n"
    cpp_file_text = cpp_file_text + "\n"
    
    temp = ""
    for ii in range(0, len(npc_LUT)):
        if ii == len(npc_LUT)-1:
            temp = temp + str(npc_LUT[ii])
        else:
            temp = temp + str(npc_LUT[ii]) + ","
    cpp_file_text = cpp_file_text + "const uint8_t " + map_name + "_struct::npc_LUT[] = {" + temp + "};\n"
    
    temp = ""
    for ii in range(0, len(npc_move)):
        if ii == len(npc_move)-1:
            temp = temp + str(npc_move[ii])
        else:
            temp = temp + str(npc_move[ii]) + ","
    cpp_file_text = cpp_file_text + "const uint8_t " + map_name + "_struct::npc_move[] = {" + temp + "};\n"
    
    temp = ""
    for ii in range(0, len(npc_text)):
        if ii == len(npc_text)-1:
            temp = temp + "\"" + npc_text[ii] + "\""
        else:
            temp = temp + "\"" + npc_text[ii] + "\"" + ","
    cpp_file_text = cpp_file_text + "const std::string " + map_name + "_struct::npc_text[] = {" + temp + "};\n"
    
    temp = ""
    for ii in range(0, len(npc_pos)):
        if ii == len(npc_pos)-1:
            temp = temp + str(npc_pos[ii])
        else:
            temp = temp + str(npc_pos[ii]) + ","
    cpp_file_text = cpp_file_text + "const uint32_t " + map_name + "_struct::npc_pos[] = {" + temp + "};\n"
    
    ###############################################################################
    # Save the files
    ###############################################################################
    f_h = open(os.environ['PATH_FROG']+"/trunk/output_maps/" + map_name_in + ".h", mode="w")
    f_h.write(h_file_text)
    f_h.close()
    
    f_cpp = open(os.environ['PATH_FROG']+"/trunk/output_maps/" + map_name_in + ".cpp", mode="w")
    f_cpp.write(cpp_file_text)
    f_cpp.close()
    
def read_map_CPP_v1(cpp_file_in):
    f_cpp = open(cpp_file_in, mode="r")
    content = f_cpp.readlines()
    f_cpp.close()
    dicta_names = ["map_array", "collision_array", "spawns_array", "npc_LUT", "npc_ai", "npc_text", "npc_pos"]
    dicta = {}
    kk = 0
    incr = 0;
    for ii in range(0, len(content)):
        content[ii] = content[ii].strip()
        a = content[ii].split("{", 1)
        if len(a) == 2:
            content[ii] = a[1]
        else:
            content[ii] = a[0]
        a = content[ii].split("};", 1)
        if len(a) == 2:
            content[ii] = a[0]
            incr = 1
        else:
            incr = 0
        if dicta_names[kk] in dicta:
            dicta[dicta_names[kk]] = dicta[dicta_names[kk]] + content[ii]
        else:
            dicta[dicta_names[kk]] = content[ii]
        kk = kk + incr
        
    for key in dicta:
        if key == "npc_text":
            #dicta[key] = dicta[key].split(",")
            dicta[key] = re.findall('"([^"]*)"', dicta[key])
        else:
            if dicta[key] == '':
                dicta[key] = 0
            else:
                if key == "npc_pos":
                    dicta[key] = [np.uint32(i) for i in dicta[key].split(",")]
                else:
                    dicta[key] = [np.uint8(i) for i in dicta[key].split(",")]
            
    return(dicta)
    
# TEST SAVING #
###self.current_map = np.loadtxt(path_in, dtype='uint8', delimiter=',')
#this_map = np.genfromtxt("/home/pi/Documents/mbed_Graphics/old_maps/map004.out", dtype='float64', delimiter=',')
#if np.isnan(this_map[0, np.size(this_map, 1)-1]):
#    this_map = this_map[0:np.size(this_map, 0), 0:np.size(this_map, 1)-1]
#this_map = np.uint8(this_map)
#
#map_x = np.size(this_map, 1)
#map_y = np.size(this_map, 0)
#map_n = map_x * map_y
#
#this_map2 = np.reshape(this_map, map_n)
#current_map = this_map2
#current_collision = np.zeros(map_n, dtype='uint8')
#current_npc = np.empty(map_n, dtype=NPC)
#for ii in range(0, map_n):
#    current_npc[ii] = npc_list[0]
#current_npc[2] = npc_list[3].createCopy()
#current_npc[2].set_ai(1)
#current_npc[2].set_text("Hi")
#current_npc[5] = npc_list[7].createCopy()
#current_npc[5].set_ai(2)
#current_npc[5].set_text("Yo")
#current_spawn = np.zeros(map_n, dtype='uint8')
#
#output_map_CPP("test_new", map_x, map_y, current_map, current_collision, current_npc, current_spawn)

# TEST LOADING #
#dict_cpp = read_map_CPP("/home/pi/Documents/mbed_Graphics/output_maps/map002.cpp")
#dict_h = read_map_H("/home/pi/Documents/mbed_Graphics/output_maps/test_new.h")




    
