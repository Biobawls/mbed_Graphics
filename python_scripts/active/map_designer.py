#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon July 03 00:00:00 2018

@author: Biobawls
"""

# bug: sometimes you get an error about not being able to find image
# comment out canvas.createimage in SpritePanel, run the script, close all windows, uncomment canvas.createimage in SpritePanel, run, it should now work

# Bleh, so much dependancies for no real reason, but I don't know how to avoid it :(
# I think maybe creating some kind of array that holds the handles gets passed into the objects
# which means breaking the constructors

import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as tkf
import tkinter.scrolledtext as tkst
from PIL import Image, ImageTk
import numpy as np
import scipy as sp
import glob
import sprites
import pandas as pd
import re
from npc_definitions import npc_list
from npc_definitions import NPC
from obj_definitions import obj_list
from obj_definitions import OBJ
from item_definitions import item_list
from item_definitions import ITEM
from map_output_C import output_map_CPP
from map_output_C import read_map_CPP
from map_output_C import read_map_H
from map_output_C import read_map_CPP_v1

###############################################################################
# Sprite selection panel
###############################################################################
class SpritePanel(tk.Frame):
    def __init__(self, root, path_in, n_rows, sprite_scaling, show_x_sprites, show_y_sprites):
        tk.Frame.__init__(self, root)
        
        self.n_rows = n_rows
        self.sprite_scaling = sprite_scaling
        self.selected_sprite = 0
        
        # load an image
        file_list = sorted(glob.glob("%s%s" % (path_in, "/*.bmp")))
        total_spritesheet = np.zeros((sprites.sprite_y*(((np.size(file_list))//n_rows)+1), sprites.sprite_x*n_rows), dtype='uint8')
        jj = 0
        for ii in range(0, np.size(file_list)):
            this_sprite = sprites.bitmap_fix(file_list[ii])
            if ii%n_rows == 0:
                jj = jj + 1
            export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
            total_spritesheet[(jj-1)*sprites.sprite_y:jj*sprites.sprite_y, (ii%n_rows)*sprites.sprite_x:((ii%n_rows)*sprites.sprite_x)+sprites.sprite_x] = export_sprite
        
        disp_sprite = np.zeros((np.size(total_spritesheet, 0), np.size(total_spritesheet, 1), 3), dtype='uint8')
        disp_sprite[:, :, 0] = ((np.right_shift(total_spritesheet, 5) & 7) / 7) * 255
        disp_sprite[:, :, 1] = ((np.right_shift(total_spritesheet, 2) & 7) / 7) * 255
        disp_sprite[:, :, 2] = ((total_spritesheet & 3) / 3) * 255
        
        disp_sprite_r = sp.misc.imresize(disp_sprite, [np.size(disp_sprite, 0)*sprite_scaling, np.size(disp_sprite, 1)*sprite_scaling, np.size(disp_sprite, 2)], interp='nearest', mode=None)
        
        sprite_pane_width = sprite_scaling*sprites.sprite_x*show_x_sprites
        sprite_pane_height = sprite_scaling*sprites.sprite_y*show_y_sprites

        # position the frame within the window
        self.pack(expand="no", fill="none", side="right")
        
        # create a canvas in the frame (for drawing stuff)
        self.canvas = tk.Canvas(self, relief="sunken")
        # dictate the size of the canvas
        self.canvas.config(width=sprite_pane_width, height=sprite_pane_height, highlightthickness=0)
        
        # create a vertical scroll bar for the frame
        self.sbarV = tk.Scrollbar(self, orient="vertical")
        # create a horizontal scroll bar for the frame
        self.sbarH = tk.Scrollbar(self, orient="horizontal")
        
        # bind the scroll bars to the canvas
        self.sbarV.config(command=self.canvas.yview)
        self.sbarH.config(command=self.canvas.xview)
        
        # bind the canvas to the scroll bars
        self.canvas.config(yscrollcommand=self.sbarV.set)
        self.canvas.config(xscrollcommand=self.sbarH.set)
        
        # put the scroll bars in the window
        self.sbarV.pack(side="right", fill="y")
        self.sbarH.pack(side="bottom", fill="x")
        
        # bind the mouse button 1
        self.canvas.bind("<Button 1>", self.select_sprite)
        
        # put the canvas in the window
        self.canvas.pack(side="left", expand="yes", fill="both")
        
        # convert the array into a Image object
        im=Image.fromarray(disp_sprite_r, 'RGB')
        
        # set the starting point of the scroll
        width,height=im.size
        self.canvas.config(scrollregion=(0,0,width,height))
        
        # convert the Image object into something that can be used in TK
        self.im2 = ImageTk.PhotoImage(image=im)
        
        # Put the image in the canvas
        self.imgtag = self.canvas.create_image(0,0,anchor="nw",image=self.im2)
        
    def select_sprite(self, event):
        canvas = event.widget
        x_pix = np.uint32(canvas.canvasx(event.x))
        y_pix = np.uint32(canvas.canvasy(event.y))
        x_pos = x_pix//(sprites.sprite_x*self.sprite_scaling)
        y_pos = y_pix//(sprites.sprite_y*self.sprite_scaling)
        self.selected_sprite = x_pos + (y_pos * self.n_rows)

###############################################################################
# Map panel
###############################################################################
class MapPanel(tk.Frame):
    def __init__(self, root, sprite_select, npc_select, npc_control, obj_select, obj_control, item_select, item_controls, sprite_sheet_path):
        tk.Frame.__init__(self, root)
        
        self.handle_SpritePanel = sprite_select
        self.handle_NPCPanel = npc_select
        self.handle_NPCControl = npc_control
        self.handle_OBJPanel = obj_select
        self.handle_OBJControl = obj_control
        self.handle_ITEMPanel = item_select
        self.handle_ITEMControl = item_controls
        self.edit_mode = 1
        self.last_selected_npc = 0
        
        self.map_x = 1
        self.map_y = 1
        self.map_n = self.map_x * self.map_y
        self.generate_map()
        
        self.set_sprite_path(sprite_sheet_path)
        self.load_sprite_sheet()
        
        self.pack(expand="no", fill="none", side="left")
        
        # create a canvas in the frame (for drawing stuff)
        self.canvas = tk.Canvas(self, relief="sunken")
        # dictate the size of the canvas
        self.canvas.config(width=400, height=300, highlightthickness=0)
        
        # create a vertical scroll bar for the frame
        self.sbarV = tk.Scrollbar(self, orient="vertical")
        # create a horizontal scroll bar for the frame
        self.sbarH = tk.Scrollbar(self, orient="horizontal")
        
        # bind the scroll bars to the canvas
        self.sbarV.config(command=self.canvas.yview)
        self.sbarH.config(command=self.canvas.xview)
        
        # bind the canvas to the scroll bars
        self.canvas.config(yscrollcommand=self.sbarV.set)
        self.canvas.config(xscrollcommand=self.sbarH.set)
        
        # put the scroll bars in the window
        self.sbarV.pack(side="right", fill="y")
        self.sbarH.pack(side="bottom", fill="x")

        self.rebind_event()
        
        # put the canvas in the window
        self.canvas.pack(side="left", expand="yes", fill="both")
        
    def load_sprite_sheet(self):
        file_list = sorted(glob.glob("%s%s" % (self.sprite_path, "/*.bmp")))
        
        total_spritesheet = np.zeros((sprites.sprite_y, sprites.sprite_x*np.size(file_list)), dtype='uint8')
        for ii in range(0, np.size(file_list)):
            this_sprite = sprites.bitmap_fix(file_list[ii])
            export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
            total_spritesheet[0:sprites.sprite_y, ii*sprites.sprite_x:(ii*sprites.sprite_x)+sprites.sprite_x] = export_sprite
            
        self.sprite_sheet = total_spritesheet
        
    def rebind_event(self):
        if self.edit_mode == 1:
            self.canvas.bind("<Button 1>", self.change_map_element)
        if self.edit_mode == 2:
            self.canvas.bind("<Button 1>", self.change_npc_element)
        if self.edit_mode == 3:
            self.canvas.bind("<Button 1>", self.change_obj_element)
        if self.edit_mode == 4:
            self.canvas.bind("<Button 1>", self.change_item_element)
        if self.edit_mode == 5:
            self.canvas.bind("<Button 1>", self.change_collision_element)
        if self.edit_mode == 6:
            self.canvas.bind("<Button 1>", self.change_spawn_element)
        self.update_map_display()
        self.last_selected_npc = 0
        
    def change_map_element(self, event):
        canvas = event.widget
        x_pix = np.uint32(canvas.canvasx(event.x))
        y_pix = np.uint32(canvas.canvasy(event.y))
        x_pos = x_pix//sprites.sprite_x
        y_pos = y_pix//sprites.sprite_y
        self.current_map[x_pos+(y_pos*self.map_x)] = self.handle_SpritePanel.selected_sprite
        self.update_map_display()
        
    def change_npc_element(self, event):
        canvas = event.widget
        x_pix = np.uint32(canvas.canvasx(event.x))
        y_pix = np.uint32(canvas.canvasy(event.y))
        x_pos = x_pix//sprites.sprite_x
        y_pos = y_pix//sprites.sprite_y
        # place mode
        if self.handle_NPCControl.edit_mode == 0:
            self.current_npc[x_pos+(y_pos*self.map_x)] = self.handle_NPCPanel.selected_npc.createCopy()
        elif self.handle_NPCControl.edit_mode == 1:
            self.handle_NPCPanel.update_selection(self.current_npc[x_pos+(y_pos*self.map_x)])
            self.last_selected_npc = self.current_npc[x_pos+(y_pos*self.map_x)]
        else:
            pass
        self.handle_NPCControl.npc_pos_x.set(x_pos)
        self.handle_NPCControl.npc_pos_y.set(y_pos)
        self.update_map_display()
        
    def change_obj_element(self, event):
        canvas = event.widget
        x_pix = np.uint32(canvas.canvasx(event.x))
        y_pix = np.uint32(canvas.canvasy(event.y))
        x_pos = x_pix//sprites.sprite_x
        y_pos = y_pix//sprites.sprite_y
        if self.handle_OBJControl.edit_mode == 0:
            self.current_obj[x_pos+(y_pos*self.map_x)] = self.handle_OBJPanel.selected_obj.createCopy()
        elif self.handle_OBJControl.edit_mode == 1:
            self.handle_OBJPanel.update_selection(self.current_obj[x_pos+(y_pos*self.map_x)])
            self.last_selected_obj = self.current_obj[x_pos+(y_pos*self.map_x)]
        else:
            pass
        self.handle_OBJControl.obj_pos_x.set(x_pos)
        self.handle_OBJControl.obj_pos_y.set(y_pos)
        self.update_map_display()
        
    def change_item_element(self, event):
        canvas = event.widget
        x_pix = np.uint32(canvas.canvasx(event.x))
        y_pix = np.uint32(canvas.canvasy(event.y))
        x_pos = x_pix//sprites.sprite_x
        y_pos = y_pix//sprites.sprite_y
        if self.handle_ITEMControl.edit_mode == 0:
            self.current_item[x_pos+(y_pos*self.map_x)] = self.handle_ITEMPanel.selected_item.createCopy()
        elif self.handle_ITEMControl.edit_mode == 1:
            self.handle_ITEMPanel.update_selection(self.current_item[x_pos+(y_pos*self.map_x)])
            self.last_selected_item = self.current_item[x_pos+(y_pos*self.map_x)]
        else:
            pass
        self.handle_ITEMControl.item_pos_x.set(x_pos)
        self.handle_ITEMControl.item_pos_y.set(y_pos)
        self.update_map_display()
        
    def change_collision_element(self, event):
        canvas = event.widget
        x_pix = np.uint32(canvas.canvasx(event.x))
        y_pix = np.uint32(canvas.canvasy(event.y))
        x_pos = x_pix//sprites.sprite_x
        y_pos = y_pix//sprites.sprite_y
        if self.current_collision[x_pos+(y_pos*self.map_x)] == 0:
            self.current_collision[x_pos+(y_pos*self.map_x)] = 1
        else:
            self.current_collision[x_pos+(y_pos*self.map_x)] = 0
        self.update_map_display()
        
    def change_spawn_element(self, event):
        canvas = event.widget
        x_pix = np.uint32(canvas.canvasx(event.x))
        y_pix = np.uint32(canvas.canvasy(event.y))
        x_pos = x_pix//sprites.sprite_x
        y_pos = y_pix//sprites.sprite_y
        if self.current_spawn[x_pos+(y_pos*self.map_x)] == 0:
            self.current_spawn[x_pos+(y_pos*self.map_x)] = 1
        else:
            self.current_spawn[x_pos+(y_pos*self.map_x)] = 0
        self.update_map_display()
        
    def set_sprite_path(self, path_in):
        self.sprite_path = path_in
        
    def generate_map(self):
        self.current_map = np.zeros(self.map_n, dtype='uint16')
        self.current_collision = np.zeros(self.map_n, dtype='uint8')
        self.current_npc = np.empty(self.map_n, dtype=NPC)
        self.current_obj = np.empty(self.map_n, dtype=OBJ)
        self.current_item = np.empty(self.map_n, dtype=ITEM)
        for ii in range(0, self.map_n):
            self.current_npc[ii] = npc_list[0]
            self.current_obj[ii] = obj_list[0]
            self.current_item[ii] = item_list[0]

        self.current_spawn = np.zeros(self.map_n, dtype='uint8')
        #self.current_map = np.ones((self.map_y, self.map_x), dtype='uint8')
        #self.current_npc = np.ones((self.map_y, self.map_x), dtype='uint8')*7
        #self.current_collision = np.ones((self.map_y, self.map_x), dtype='uint8')*7
        #self.current_spawn = np.ones((self.map_y, self.map_x), dtype='uint8')*7
        
    def load_map_bitmap(self, path_in):
        this_map = sprites.bitmap_fix(path_in)
        this_map = np.left_shift(this_map[:, :, 0], 5) + np.left_shift(this_map[:, :, 1], 2) + this_map[:, :, 2]
        
        self.map_x = np.size(this_map, 1)
        self.map_y = np.size(this_map, 0)
        self.map_n = self.map_x * self.map_y
        
        this_map = np.uint16(np.reshape(this_map, self.map_n))
        self.current_map = this_map
        self.current_collision = np.zeros(self.map_n, dtype='uint8')
        self.current_npc = np.empty(self.map_n, dtype=NPC)
        self.current_obj = np.empty(self.map_n, dtype=OBJ)
        self.current_item = np.empty(self.map_n, dtype=ITEM)
        for ii in range(0, self.map_n):
            self.current_npc[ii] = npc_list[0]
            self.current_obj[ii] = obj_list[0]
            self.current_item[ii] = item_list[0]
        self.current_spawn = np.zeros(self.map_n, dtype='uint8')
        
    def load_map_text(self, path_in):
        #self.current_map = np.loadtxt(path_in, dtype='uint8', delimiter=',')
        this_map = np.genfromtxt(path_in, dtype='float64', delimiter=',')
        if np.isnan(this_map[0, np.size(this_map, 1)-1]):
            this_map = this_map[0:np.size(this_map, 0), 0:np.size(this_map, 1)-1]
        this_map = np.uint16(this_map)
        
        self.map_x = np.size(this_map, 1)
        self.map_y = np.size(this_map, 0)
        self.map_n = self.map_x * self.map_y
        
        this_map = np.reshape(this_map, self.map_n)
        self.current_map = this_map
        self.current_collision = np.zeros(self.map_n, dtype='uint8')
        self.current_npc = np.empty(self.map_n, dtype=NPC)
        self.current_obj = np.empty(self.map_n, dtype=OBJ)
        self.current_item = np.empty(self.map_n, dtype=ITEM)
        for ii in range(0, self.map_n):
            self.current_npc[ii] = npc_list[0]
            self.current_obj[ii] = obj_list[0]
            self.current_item[ii] = item_list[0]
        self.current_spawn = np.zeros(self.map_n, dtype='uint8')
        
    def update_map_display(self):        
        total_map = np.zeros((self.map_y*sprites.sprite_y, self.map_x*sprites.sprite_x), dtype='uint8')
        total_overlay_map = np.zeros((self.map_y*sprites.sprite_y, self.map_x*sprites.sprite_x), dtype='uint8')
        for ii in range(0, self.map_x):
            for jj in range(0, self.map_y):
                this_sprite_index = self.current_map[ii+(jj*self.map_x)]
                total_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = self.sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x]
                if self.edit_mode == 1:
                    pass
                if self.edit_mode == 2:
                    this_sprite_index = self.current_npc[ii+(jj*self.map_x)].down1
                    total_overlay_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = sprites.sprite_indexing(self.current_npc[ii+(jj*self.map_x)].down1_index, self.sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x])
                if self.edit_mode == 3:
                    this_sprite_index = self.current_obj[ii+(jj*self.map_x)].sprite
                    total_overlay_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = sprites.sprite_indexing(self.current_obj[ii+(jj*self.map_x)].sprite_index, self.sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x])
                if self.edit_mode == 4:
                    this_sprite_index = self.current_item[ii+(jj*self.map_x)].sprite
                    total_overlay_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = self.sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x]
                if self.edit_mode == 5:
                    this_sprite_index = self.current_collision[ii+(jj*self.map_x)]
                    if this_sprite_index == 0:
                        total_overlay_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = 224
                    else:
                        total_overlay_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = 28
                if self.edit_mode == 6:
                    this_sprite_index = self.current_spawn[ii+(jj*self.map_x)]
                    if this_sprite_index == 0:
                        total_overlay_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = 0
                    else:
                        total_overlay_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = 255
        
        disp_map = np.zeros((np.size(total_map, 0), np.size(total_map, 1), 4), dtype='uint8')
        disp_map[:, :, 0] = ((np.right_shift(total_map, 5) & 7) / 7) * 255
        disp_map[:, :, 1] = ((np.right_shift(total_map, 2) & 7) / 7) * 255
        disp_map[:, :, 2] = ((total_map & 3) / 3) * 255
        disp_map[:, :, 3] = np.ones(np.shape(total_map)) * 255
        
        if self.edit_mode == 1:
            disp_overlay = np.zeros((np.size(total_overlay_map, 0), np.size(total_overlay_map, 1), 4), dtype='uint8')
        if self.edit_mode == 2:
            disp_overlay = np.zeros((np.size(total_overlay_map, 0), np.size(total_overlay_map, 1), 4), dtype='uint8')
            disp_overlay[:, :, 0] = ((np.right_shift(total_overlay_map, 5) & 7) / 7) * 255
            disp_overlay[:, :, 1] = ((np.right_shift(total_overlay_map, 2) & 7) / 7) * 255
            disp_overlay[:, :, 2] = ((total_overlay_map & 3) / 3) * 255
            temp = np.ones((np.size(total_overlay_map, 0), np.size(total_overlay_map, 1)), dtype='uint8') * 255
            temp[total_overlay_map == self.handle_NPCPanel.selected_npc.alpha_pixel] = 0
            disp_overlay[:, :, 3] = temp
        if self.edit_mode == 3:
            disp_overlay = np.zeros((np.size(total_overlay_map, 0), np.size(total_overlay_map, 1), 4), dtype='uint8')
            disp_overlay[:, :, 0] = ((np.right_shift(total_overlay_map, 5) & 7) / 7) * 255
            disp_overlay[:, :, 1] = ((np.right_shift(total_overlay_map, 2) & 7) / 7) * 255
            disp_overlay[:, :, 2] = ((total_overlay_map & 3) / 3) * 255
            temp = np.ones((np.size(total_overlay_map, 0), np.size(total_overlay_map, 1)), dtype='uint8') * 255
            temp[total_overlay_map == self.handle_OBJPanel.selected_obj.alpha_pixel] = 0
            disp_overlay[:, :, 3] = temp
        if self.edit_mode == 4:
            disp_overlay = np.zeros((np.size(total_overlay_map, 0), np.size(total_overlay_map, 1), 4), dtype='uint8')
            disp_overlay[:, :, 0] = ((np.right_shift(total_overlay_map, 5) & 7) / 7) * 255
            disp_overlay[:, :, 1] = ((np.right_shift(total_overlay_map, 2) & 7) / 7) * 255
            disp_overlay[:, :, 2] = ((total_overlay_map & 3) / 3) * 255
            temp = np.ones((np.size(total_overlay_map, 0), np.size(total_overlay_map, 1)), dtype='uint8') * 255
            temp[total_overlay_map == self.handle_ITEMPanel.selected_item.alpha_pixel] = 0
            disp_overlay[:, :, 3] = temp
        if self.edit_mode == 5:
            disp_overlay = np.zeros((np.size(total_overlay_map, 0), np.size(total_overlay_map, 1), 4), dtype='uint8')
            disp_overlay[:, :, 0] = ((np.right_shift(total_overlay_map, 5) & 7) / 7) * 255
            disp_overlay[:, :, 1] = ((np.right_shift(total_overlay_map, 2) & 7) / 7) * 255
            disp_overlay[:, :, 2] = ((total_overlay_map & 3) / 3) * 255
            temp = np.ones((np.size(total_overlay_map, 0), np.size(total_overlay_map, 1)), dtype='uint8') * 255
            temp[::2] = 0
            disp_overlay[:, :, 3] = temp
        if self.edit_mode == 6:
            disp_overlay = np.zeros((np.size(total_overlay_map, 0), np.size(total_overlay_map, 1), 4), dtype='uint8')
            disp_overlay[:, :, 0] = ((np.right_shift(total_overlay_map, 5) & 7) / 7) * 255
            disp_overlay[:, :, 1] = ((np.right_shift(total_overlay_map, 2) & 7) / 7) * 255
            disp_overlay[:, :, 2] = ((total_overlay_map & 3) / 3) * 255
            temp = np.ones((np.size(total_overlay_map, 0), np.size(total_overlay_map, 1)), dtype='uint8') * 255
            temp[::2] = 0
            disp_overlay[:, :, 3] = temp

        # convert the array into a Image object
        #im=Image.fromarray(disp_map, 'RGB')
        imMap = Image.fromarray(disp_map, 'RGBA')
        imOVR = Image.fromarray(disp_overlay, 'RGBA')
        imMap.paste(imOVR, (0, 0), imOVR)
        
        # set the starting point of the scroll
        width,height=imMap.size
        self.canvas.config(scrollregion=(0,0,width,height))
        
        # convert the Image object into something that can be used in TK
        self.im2 = ImageTk.PhotoImage(image=imMap)
        
        # Put the image in the canvas
        self.imgtag = self.canvas.create_image(0,0,anchor="nw",image=self.im2)
        
    def load_current_map(self, map_array, map_x, map_y):
        self.current_map = map_array
        self.map_x = map_x
        self.map_y = map_y
        self.map_n = map_x * map_y
        
    def load_current_collision(self, collision_array):
        self.current_collision = collision_array
        
    def load_current_spawn(self, spawn_array):
        self.current_spawn = spawn_array
        
    # legacy
    def load_Cv1_current_npc(self, npc_LUT_array, npc_text_array, npc_ai_array, npc_pos_array):
        self.current_npc = np.empty(self.map_n, dtype=NPC)
        for ii in range(0, self.map_n):
            self.current_npc[ii] = self.handle_NPCPanel.npc_list[0]
        if npc_LUT_array == 0:
            return
        for ii in range(0, len(npc_pos_array)):
            #npc_num = npc_LUT_array[ii]
            npc_type = npc_LUT_array[(ii*2)+1]
            npc_ai = npc_ai_array[ii]
            npc_text = npc_text_array[ii]
            npc_pos = npc_pos_array[ii]
            
            self.current_npc[npc_pos] = self.handle_NPCPanel.npc_list[npc_type].createCopy()
            self.current_npc[npc_pos].set_ai(npc_ai)
            self.current_npc[npc_pos].set_text(npc_text)
            
    def load_current_npc(self, npc_LUT_array, npc_text_array, npc_ai_array, npc_pos_array):
        self.current_npc = np.empty(self.map_n, dtype=NPC)
        for ii in range(0, self.map_n):
            self.current_npc[ii] = self.handle_NPCPanel.npc_list[0]
        if npc_LUT_array == 0:
            return
        for ii in range(0, len(npc_pos_array)):
            #npc_num = npc_LUT_array[ii]
            npc_type = npc_LUT_array[ii]
            npc_ai = npc_ai_array[ii]
            npc_text = npc_text_array[ii]
            npc_pos = npc_pos_array[ii]
            
            self.current_npc[npc_pos] = self.handle_NPCPanel.npc_list[npc_type].createCopy()
            self.current_npc[npc_pos].set_ai(npc_ai)
            self.current_npc[npc_pos].set_text(npc_text)
            
    ## legacy
    def load_empty_current_obj(self):
        self.current_obj = np.empty(self.map_n, dtype=OBJ)
        for ii in range(0, self.map_n):
            self.current_obj[ii] = obj_list[0]
            
    def load_current_obj(self, obj_LUT_array, obj_pos_array, obj_collision_array):
        self.current_obj = np.empty(self.map_n, dtype=OBJ)
        for ii in range(0, self.map_n):
            self.current_obj[ii] = self.handle_OBJPanel.obj_list[0]
        if obj_LUT_array == 0:
            return
        for ii in range(0, len(obj_pos_array)):
            obj_type = obj_LUT_array[ii]
            obj_collision = obj_collision_array[ii]
            obj_pos = obj_pos_array[ii]
            
            self.current_obj[obj_pos] = self.handle_OBJPanel.obj_list[obj_type].createCopy()
            self.current_obj[obj_pos].set_collision(obj_collision)
            
    # legacy
    def load_empty_current_item(self):
        self.current_item = np.empty(self.map_n, dtype=ITEM)
        for ii in range(0, self.map_n):
            self.current_item[ii] = item_list[0]
            
    def load_current_item(self, item_LUT_array, item_pos_array, item_global_list):
        self.current_item = np.empty(self.map_n, dtype=ITEM)
        for ii in range(0, self.map_n):
            self.current_item[ii] = item_list[0]
        if item_LUT_array == 0:
            return
        for ii in range(0, len(item_pos_array)):
            item_type = item_LUT_array[ii]
            item_global_pos = item_global_list[ii]
            item_pos = item_pos_array[ii]
            
            self.current_item[item_pos] = item_list[item_type].createCopy()
            self.current_item[item_pos].set_global_index(item_global_pos)
        
#    def update_map_image(self):
#        total_map = np.zeros((self.map_y*sprites.sprite_y, self.map_x*sprites.sprite_x), dtype='uint8')
#        for ii in range(0, self.map_x):
#            for jj in range(0, self.map_y):
#                this_sprite_index = self.current_map[jj, ii]
#                #thing = total_spritesheet[(0*sprites.sprite_y):(0*sprites.sprite_y)+sprites.sprite_y-1, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x-1]
#                total_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = self.sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x]
#        
#        disp_map = np.zeros((np.size(total_map, 0), np.size(total_map, 1), 3), dtype='uint8')
#        disp_map[:, :, 0] = ((np.right_shift(total_map, 5) & 7) / 7) * 255
#        disp_map[:, :, 1] = ((np.right_shift(total_map, 2) & 7) / 7) * 255
#        disp_map[:, :, 2] = ((total_map & 3) / 3) * 255
#        
#        # convert the array into a Image object
#        im=Image.fromarray(disp_map, 'RGB')
#        
#        # convert the Image object into something that can be used in TK
#        self.im2 = ImageTk.PhotoImage(image=im)
#        self.canvas.itemconfig(self.imgtag, image=self.im2)

###############################################################################
# Map control buttons
###############################################################################
class MapControls(tk.Frame):
    def __init__(self, root, map_panel, bitmap_paths, text_paths):
        tk.Frame.__init__(self, root)
        
        self.textmap_path = text_paths
        
        # Handles
        self.handle_MapPanel = map_panel
        
        # Layout
        # Drop down
        self.map_frame00 = tk.Frame(master=root)
        self.map_frame00.grid(row=0, column=0, columnspan=2, sticky="nw")
        # Load button
        self.map_frame10 = tk.Frame(master=root)
        self.map_frame10.grid(row=1, column=0, columnspan=2, sticky="nw")
        # Save button
        self.map_frame20 = tk.Frame(master=root)
        self.map_frame20.grid(row=2, column=0, columnspan=2, sticky="nw")
        # Refresh button
        self.map_frame30 = tk.Frame(master=root)
        self.map_frame30.grid(row=3, column=0, columnspan=2, sticky="nw")
        # Filename textbox
        self.map_frame40 = tk.Frame(master=root)
        self.map_frame40.grid(row=4, column=0, columnspan=2, sticky="nw")
        # Map size X
        self.map_frame50 = tk.Frame(master=root)
        self.map_frame50.grid(row=5, column=0, columnspan=1, sticky="nw")
        # Map size Y
        self.map_frame51 = tk.Frame(master=root)
        self.map_frame51.grid(row=5, column=1, columnspan=1,  sticky="nw")
        # Create button
        self.map_frame60 = tk.Frame(master=root)
        self.map_frame60.grid(row=6, column=0, columnspan=2,  sticky="nw")
        # Edit button
        self.map_frame70 = tk.Frame(master=root)
        self.map_frame70.grid(row=7, column=0, columnspan=2,  sticky="nw")
        # load bmp and out button
        self.map_frame80 = tk.Frame(master=root)
        self.map_frame80.grid(row=8, column=0, columnspan=1,  sticky="nw")
        self.map_frame81 = tk.Frame(master=root)
        self.map_frame81.grid(row=8, column=1, columnspan=1,  sticky="nw")
        self.map_frame90 = tk.Frame(master=root)
        self.map_frame90.grid(row=9, column=0, columnspan=1,  sticky="nw")
        
        # Handles
        # drop downs
        self.map_panel_dropdown = MapDropDown(self.map_frame00, bitmap_paths, text_paths)
        #self.map_panel_dropdown.load_bitmap_maps()
        #self.map_panel_dropdown.load_text_maps()
        self.map_panel_dropdown.load_C_maps()
        # buttons
        self.map_load_button = tk.Button(self.map_frame10, text="Load", command=lambda: self.load_map())
        self.map_load_button.pack()
        self.map_save_button = tk.Button(self.map_frame20, text="Save", command=lambda: self.save_map())
        self.map_save_button.pack()
        self.map_refresh_button = tk.Button(self.map_frame30, text="Refresh", command=lambda: self.refresh_map())
        self.map_refresh_button.pack()
        self.map_create_button = tk.Button(self.map_frame60, text="Create", command=lambda: self.create_map())
        self.map_create_button.pack()
        self.map_edit_text = tk.StringVar()
        self.map_edit_text.set("Map edit")
        self.map_edit_button = tk.Button(self.map_frame70, textvariable=self.map_edit_text, command=lambda: self.edit_map())
        self.map_edit_button.pack()
        self.map_load_bmp_button = tk.Button(self.map_frame80, text="Load bmp", command=lambda: self.load_bmp_map())
        self.map_load_bmp_button.pack()
        self.map_load_text_button = tk.Button(self.map_frame81, text="Load text", command=lambda: self.load_text_map())
        self.map_load_text_button.pack()
        self.map_load_text_button = tk.Button(self.map_frame90, text="Load C.v1", command=lambda: self.load_v1_C_map())
        self.map_load_text_button.pack()
        # text boxes
        self.map_mapname_entry = tk.Entry(self.map_frame40, textvariable=self.map_panel_dropdown.choice, width=25)
        self.map_mapname_entry.pack()
        self.map_mapx_entry = tk.Entry(self.map_frame50, width=12)
        self.map_mapx_entry.insert(0, "0")
        self.map_mapx_entry.pack()
        self.map_mapy_entry = tk.Entry(self.map_frame51, width=12)
        self.map_mapy_entry.insert(0, "0")
        self.map_mapy_entry.pack()
        
    def load_map(self):
        this_sel = self.map_panel_dropdown.get_selection()
        n = re.split(r"\.", this_sel)
        filen = n[0]
        dicta_cpp = read_map_CPP(filen + ".cpp")
        dicta_h = read_map_H(filen + ".h")
        dicta = {**dicta_cpp, **dicta_h}
        
        self.handle_MapPanel.load_current_map(dicta["map_array"], dicta["map_x"][0], dicta["map_y"][0])
        self.handle_MapPanel.load_current_collision(dicta["collision_array"])
        self.handle_MapPanel.load_current_spawn(dicta["spawns_array"])
        self.handle_MapPanel.load_current_npc(dicta["npc_LUT"], dicta["npc_text"], dicta["npc_ai"], dicta["npc_pos"])
        self.handle_MapPanel.load_current_obj(dicta["obj_LUT"], dicta["obj_pos"], dicta["obj_collision"])
        self.handle_MapPanel.load_current_item(dicta["item_LUT"], dicta["item_pos"], dicta["item_in_list"])
        
        self.handle_MapPanel.update_map_display()
        self.map_mapx_entry.delete(0, 'end')
        self.map_mapx_entry.insert(0, str(self.handle_MapPanel.map_x))
        self.map_mapy_entry.delete(0, 'end')
        self.map_mapy_entry.insert(0, str(self.handle_MapPanel.map_y))
        
    def load_v1_C_map(self):
        this_sel = self.map_panel_dropdown.get_selection()
        n = re.split(r"\.", this_sel)
        filen = n[0]
        dicta_cpp = read_map_CPP_v1(filen + ".cpp")
        dicta_h = read_map_H(filen + ".h")
        dicta = {**dicta_cpp, **dicta_h}
        
        self.handle_MapPanel.load_current_map(dicta["map_array"], dicta["map_x"][0], dicta["map_y"][0])
        self.handle_MapPanel.load_current_collision(dicta["collision_array"])
        self.handle_MapPanel.load_current_spawn(dicta["spawns_array"])
        self.handle_MapPanel.load_Cv1_current_npc(dicta["npc_LUT"], dicta["npc_text"], dicta["npc_ai"], dicta["npc_pos"])
        self.handle_MapPanel.load_empty_current_obj()
        self.handle_MapPanel.load_empty_current_item()
        
#        self.map_mapx_entry.delete(0, 'end')
#        self.map_mapx_entry.insert(0, str(dicta["map_x"][0]))
#        self.map_mapy_entry.delete(0, 'end')
#        self.map_mapy_entry.insert(0, str(dicta["map_y"][0]))
#        this_sel = self.map_panel_dropdown.get_selection()
#        n = re.split(r"\.", this_sel)
#        fileexten = n[-1]
#        if "bmp" in fileexten:
#            self.handle_MapPanel.load_map_bitmap(this_sel)
#        if "out" in fileexten:
#            self.handle_MapPanel.load_map_text(this_sel)
        self.handle_MapPanel.update_map_display()
        self.map_mapx_entry.delete(0, 'end')
        self.map_mapx_entry.insert(0, str(self.handle_MapPanel.map_x))
        self.map_mapy_entry.delete(0, 'end')
        self.map_mapy_entry.insert(0, str(self.handle_MapPanel.map_y))
        
    def save_map(self):
        # remove the dot at the end
        n = re.split(r"\.", self.map_mapname_entry.get())
        this_sel = n[0]
        #self.textmap_path
        #np.savetxt(self.textmap_path + "/" + this_sel + ".out", self.handle_MapPanel.current_map, delimiter=',',fmt='%i',newline=',\n')
        output_map_CPP(this_sel, self.handle_MapPanel.map_x, self.handle_MapPanel.map_y, self.handle_MapPanel.current_map, self.handle_MapPanel.current_collision, self.handle_MapPanel.current_npc, self.handle_MapPanel.current_spawn, self.handle_MapPanel.current_obj, self.handle_MapPanel.current_item)
        
    def load_bmp_map(self):
        filename =  tkf.askopenfilename(initialdir = self.map_panel_dropdown.bitmap_path ,title = "Select file",filetypes = (("bmp files","*.bmp"),("all files","*.*")))
        if not filename:
            return
        self.handle_MapPanel.load_map_bitmap(filename)
        self.handle_MapPanel.update_map_display()
        self.map_mapx_entry.delete(0, 'end')
        self.map_mapx_entry.insert(0, str(self.handle_MapPanel.map_x))
        self.map_mapy_entry.delete(0, 'end')
        self.map_mapy_entry.insert(0, str(self.handle_MapPanel.map_y))
        
    def load_text_map(self):
        filename =  tkf.askopenfilename(initialdir = self.map_panel_dropdown.textmap_path ,title = "Select file",filetypes = (("text files","*.out"),("all files","*.*")))
        if not filename:
            return
        self.handle_MapPanel.load_map_text(filename)
        self.handle_MapPanel.update_map_display()
        self.map_mapx_entry.delete(0, 'end')
        self.map_mapx_entry.insert(0, str(self.handle_MapPanel.map_x))
        self.map_mapy_entry.delete(0, 'end')
        self.map_mapy_entry.insert(0, str(self.handle_MapPanel.map_y))
        
    def refresh_map(self):
        self.map_panel_dropdown.clear_list()
        self.map_panel_dropdown.load_C_maps()
        #self.handle_MapPanel.load_bitmap_maps()
        #self.handle_MapPanel.load_text_maps()

    def create_map(self):
        x = np.uint32(self.map_mapx_entry.get())
        y = np.uint32(self.map_mapy_entry.get())
        self.handle_MapPanel.map_x = x
        self.handle_MapPanel.map_y = y
        self.handle_MapPanel.map_n = x * y
        self.handle_MapPanel.generate_map()
        self.handle_MapPanel.current_map = self.handle_MapPanel.current_map + self.handle_MapPanel.handle_SpritePanel.selected_sprite
        self.handle_MapPanel.update_map_display()
        
    def edit_map(self):
        self.handle_MapPanel.edit_mode = self.handle_MapPanel.edit_mode + 1
        if self.handle_MapPanel.edit_mode > 6:
            self.handle_MapPanel.edit_mode = 1
            
        if self.handle_MapPanel.edit_mode == 1:
            self.map_edit_text.set("Map edit")
        if self.handle_MapPanel.edit_mode == 2:
            self.map_edit_text.set("NPC edit")
        if self.handle_MapPanel.edit_mode == 3:
            self.map_edit_text.set("OBJ edit")
        if self.handle_MapPanel.edit_mode == 4:
            self.map_edit_text.set("item edit")
        if self.handle_MapPanel.edit_mode == 5:
            self.map_edit_text.set("Collision edit")
        if self.handle_MapPanel.edit_mode == 6:
            self.map_edit_text.set("Spawn edit")
            
        self.handle_MapPanel.rebind_event()

###############################################################################
# Drop down menu for map selections
###############################################################################
class MapDropDown(tk.Frame):
    def __init__(self, root, bitmap_path, textmap_path):
        tk.Frame.__init__(self, root)

        self.bitmap_path = bitmap_path
        self.textmap_path = textmap_path

        self.choice = tk.StringVar()

        #self.option = tk.OptionMenu(root, self.choice, [])
        self.option = ttk.Combobox(root, textvariable=self.choice, state="readonly")
        #self.option.bind('<<ComboboxSelected>>', self.get_selection)
        self.option.pack()
        self.option.config(width=20)
        
        self.clear_list()
        
    def load_C_maps(self):
        map_C_list = sorted(glob.glob("%s%s" % (self.textmap_path, "/*.cpp")))
        # prepare a Series
        s = pd.Series()
        # For each .bmp found add it's filename and path+filename to the Series
        for this_map in map_C_list:
            n = re.split(r"/", this_map)
            filename = n[-1]
            s2 = pd.Series(this_map, index=[filename])
            s = s.append(s2)
        # store the current Series
        self.map_series = self.map_series.append(s)
        # force the list of maps to update
        self.update_list(self.map_series.index)
        
    def load_bitmap_maps(self):
        map_bmp_list = sorted(glob.glob("%s%s" % (self.bitmap_path, "/*.bmp")))
        # prepare a Series
        s = pd.Series()
        # For each .bmp found add it's filename and path+filename to the Series
        for this_map in map_bmp_list:
            n = re.split(r"/", this_map)
            filename = n[-1]
            s2 = pd.Series(this_map, index=[filename])
            s = s.append(s2)
        # store the current Series
        self.map_series = self.map_series.append(s)
        # force the list of maps to update
        self.update_list(self.map_series.index)
        
    def load_text_maps(self):
        map_out_list = sorted(glob.glob("%s%s" % (self.textmap_path, "/*.out")))
        s = pd.Series()
        for this_map in map_out_list:
            n = re.split(r"/", this_map)
            filename = n[-1]
            s2 = pd.Series(this_map, index=[filename])
            s = s.append(s2)
            #m = re.search(r"[0-9].out", this_map)
            #if m is not None:
                #n = re.split(r"/", this_map)
                #filename = n[-1]
                #s2 = pd.Series(this_map, index=[filename])
                #s = s.append(s2)
        self.map_series = self.map_series.append(s)
        self.update_list(self.map_series.index)

    def clear_list(self):
        # clears the drop down list
        self.option['values'] = ['']
        s = pd.Series()
        self.map_series = s
        
    def update_list(self, new_entries):
        self.option['values'] = ['']
        if len(self.map_series) == 0:
            return
        choices = self.map_series.index
        self.choice.set(choices[0])
        self.option['values'] = choices.tolist()
            
    def get_selection(self):
        return self.map_series.get(self.choice.get())
  
###############################################################################
# NPC control buttons
###############################################################################
class NPCControls(tk.Frame):
    def __init__(self, root, sprite_path, npc_list_in):
        tk.Frame.__init__(self, root)
        
        # 0 = place, 1 = edit properties
        self.edit_mode = 0
        
        # Layout
        self.npc_frame00 = tk.Frame(master=root)
        self.npc_frame00.grid(row=0, column=0, columnspan=2, sticky="nw")
        # npc list drop down
        self.npc_frame10 = tk.Frame(master=root)
        self.npc_frame10.grid(row=1, column=0, columnspan=2, sticky="nw")
        # edit mode button
        self.npc_frame20 = tk.Frame(master=root)
        self.npc_frame20.grid(row=2, column=0, columnspan=1, sticky="nw")
        # sprite cycle
        self.npc_frame21 = tk.Frame(master=root)
        self.npc_frame21.grid(row=2, column=1, columnspan=1, sticky="nw")
        # npc textbox
        self.npc_frame30 = tk.Frame(master=root)
        self.npc_frame30.grid(row=3, column=0, columnspan=1, sticky="nw")
        self.npc_frame31 = tk.Frame(master=root)
        self.npc_frame31.grid(row=3, column=1, columnspan=1, sticky="nw")
        # npc aibox
        self.npc_frame40 = tk.Frame(master=root)
        self.npc_frame40.grid(row=4, column=0, columnspan=1, sticky="nw")
        self.npc_frame41 = tk.Frame(master=root)
        self.npc_frame41.grid(row=4, column=1, columnspan=1, sticky="nw")
        # npc save
        self.npc_frame50 = tk.Frame(master=root)
        self.npc_frame50.grid(row=5, column=0, columnspan=2, sticky="nw")
        # npc position details
        self.npc_frame60 = tk.Frame(master=root)
        self.npc_frame60.grid(row=6, column=0, columnspan=1, sticky="nw")
        self.npc_frame61 = tk.Frame(master=root)
        self.npc_frame61.grid(row=6, column=1, columnspan=1, sticky="nw")
        
        # Handles
        self.handle_NPCSelector = NPCSelector(self.npc_frame00, sprite_path, npc_list_in, self)
        
        # selected npc text
        self.npc_choice = tk.StringVar()
        self.npc_choice.set(self.handle_NPCSelector.selected_npc.NPC_id)
        self.npc_choice_label = tk.Label(self.npc_frame10, textvariable=self.npc_choice)
        self.npc_choice_label.config(width=16)
        self.npc_choice_label.pack()
        
        # edit mode        
        self.npc_edit_text = tk.StringVar()
        self.npc_edit_text.set("Place")
        self.npc_editmode_button = tk.Button(self.npc_frame20, textvariable=self.npc_edit_text, command=lambda: self.edit_mode_func())
        self.npc_editmode_button.pack()
        
        # sprite cycle mode        
        self.npc_index_text = tk.StringVar()
        self.npc_index_text.set("down1")
        self.npc_index_button = tk.Button(self.npc_frame21, textvariable=self.npc_index_text, command=lambda: self.index_cycle_func())
        self.npc_index_button.pack()
        
        # text box
        self.npc_label_text = tk.Label(self.npc_frame30, text="NPC TEXT", width=8)
        self.npc_label_text.pack()
        self.npc_entry_text = tk.Entry(self.npc_frame31, width=8)
        self.npc_entry_text.insert(0, self.handle_NPCSelector.selected_npc.text)
        self.npc_entry_text.pack()
        
        self.npc_label_ai = tk.Label(self.npc_frame40, text="NPC AI", width=8)
        self.npc_label_ai.pack()
        self.npc_entry_ai = tk.Entry(self.npc_frame41, width=8)
        self.npc_entry_ai.insert(0, str(self.handle_NPCSelector.selected_npc.ai))
        self.npc_entry_ai.pack()
        
        # save edits
        self.npc_save_button = tk.Button(self.npc_frame50, text="Save", command=lambda: self.save_npc())
        self.npc_save_button.pack()
        
        # npc positions
        self.npc_pos_x = tk.StringVar()
        self.npc_pos_y = tk.StringVar()
        self.npc_pos_x.set("NULL")
        self.npc_pos_y.set("NULL")
        self.npc_pos_x_label = tk.Label(self.npc_frame60, textvariable=self.npc_pos_x)
        self.npc_pos_y_label = tk.Label(self.npc_frame61, textvariable=self.npc_pos_y)
        self.npc_pos_x_label.config(width=8)
        self.npc_pos_y_label.config(width=8)
        self.npc_pos_x_label.pack()
        self.npc_pos_y_label.pack()
        
    def edit_mode_func(self):
        if self.edit_mode == 0:
            self.edit_mode = 1
            self.npc_edit_text.set("Selection")
        elif self.edit_mode == 1:
            self.edit_mode = 0
            self.npc_edit_text.set("Place")
        else:
            self.edit_mode = 0
            self.npc_edit_text.set("Place")
            
    def index_cycle_func(self):
        pass        
        
    def save_npc(self):
        if self.handle_MapPanel.last_selected_npc != 0:
            self.handle_MapPanel.last_selected_npc.set_ai(np.uint8(self.npc_entry_ai.get()))
            self.handle_MapPanel.last_selected_npc.set_text(self.npc_entry_text.get())
        self.handle_NPCSelector.update_selection(self.handle_NPCSelector.npc_list["empty"])
       
###############################################################################
# OBJ control buttons
###############################################################################
class OBJControls(tk.Frame):
    def __init__(self, root, sprite_path, obj_list_in):
        tk.Frame.__init__(self, root)
        
        self.edit_mode = 0
        
        # Layout
        self.obj_frame00 = tk.Frame(master=root)
        self.obj_frame00.grid(row=0, column=0, columnspan=2, sticky="nw")
        # obj list drop down
        self.obj_frame10 = tk.Frame(master=root)
        self.obj_frame10.grid(row=1, column=0, columnspan=2, sticky="nw")
        # edit mode button
        self.obj_frame20 = tk.Frame(master=root)
        self.obj_frame20.grid(row=2, column=0, columnspan=2, sticky="nw")
        # obj collision radio button
        self.obj_frame30 = tk.Frame(master=root)
        self.obj_frame30.grid(row=3, column=0, columnspan=2, sticky="nw")
        # obj save
        self.obj_frame40 = tk.Frame(master=root)
        self.obj_frame40.grid(row=4, column=0, columnspan=2, sticky="nw")
        # obj position
        self.obj_frame50 = tk.Frame(master=root)
        self.obj_frame50.grid(row=5, column=0, columnspan=1, sticky="nw")
        self.obj_frame51 = tk.Frame(master=root)
        self.obj_frame51.grid(row=5, column=1, columnspan=1, sticky="nw")
        # obj textbox
        self.obj_frame60 = tk.Frame(master=root)
        self.obj_frame60.grid(row=6, column=0, columnspan=2, sticky="nw")
        
        # Handles
        self.handle_OBJSelector = OBJSelector(self.obj_frame00, sprite_path, obj_list_in, self)
        
        # Selected object text
        self.obj_choice = tk.StringVar()
        self.obj_choice.set(self.handle_OBJSelector.selected_obj.OBJ_id)
        self.obj_choice_label = tk.Label(self.obj_frame10, textvariable=self.obj_choice)
        self.obj_choice_label.config(width=16)
        self.obj_choice_label.pack()
        
        # edit mode button
        self.obj_edit_text = tk.StringVar()
        self.obj_edit_text.set("Place")
        self.obj_editmode_button = tk.Button(self.obj_frame20, textvariable=self.obj_edit_text, command=lambda: self.edit_mode_func())
        self.obj_editmode_button.pack()
        
        # collision check button
        self.obj_collision_choice = tk.IntVar()
        self.obj_collision_choice.set(0)

        self.obj_collision_checkbox = tk.Checkbutton(self.obj_frame30, text="Collision", variable=self.obj_collision_choice)
        self.obj_collision_checkbox.pack()
        
        # save edits
        self.obj_save_button = tk.Button(self.obj_frame40, text="Save", command=lambda: self.save_obj())
        self.obj_save_button.pack()
        
        # obj positions
        self.obj_pos_x = tk.StringVar()
        self.obj_pos_y = tk.StringVar()
        self.obj_pos_x.set("NULL")
        self.obj_pos_y.set("NULL")
        self.obj_pos_x_label = tk.Label(self.obj_frame50, textvariable=self.obj_pos_x)
        self.obj_pos_y_label = tk.Label(self.obj_frame51, textvariable=self.obj_pos_y)
        self.obj_pos_x_label.config(width=8)
        self.obj_pos_y_label.config(width=8)
        self.obj_pos_x_label.pack()
        self.obj_pos_y_label.pack()
        
        # obj properties
        self.objprop = { 'OBJ_id': tk.StringVar(value="NULL"),
                         'OBJ_id_num' : tk.StringVar(value="NULL"),
                         'sprite' : tk.StringVar(value="NULL"),
                         'sprite_index' : tk.StringVar(value="NULL"),
                         'alpha_pixel' : tk.StringVar(value="NULL"),
                         'collision' : tk.StringVar(value="NULL")}
                
        self.objprop_scroll = tkst.ScrolledText(self.obj_frame60,
            wrap   = tk.WORD,
            width  = 24,
            height = 4,
        )
        self.objprop_scroll.pack()
        self.update_objprop_scroll()
        
    def edit_mode_func(self):
        if self.edit_mode == 0:
            self.edit_mode = 1
            self.obj_edit_text.set("Selection")
        elif self.edit_mode == 1:
            self.edit_mode = 0
            self.obj_edit_text.set("Place")
        else:
            self.edit_mode = 0
            self.obj_edit_text.set("Place")

    def save_obj(self):
        if self.handle_MapPanel.last_selected_obj != 0:
            self.handle_MapPanel.last_selected_obj.set_collision(np.uint8(self.obj_collision_choice.get()))
        self.handle_OBJSelector.update_selection(self.handle_OBJSelector.obj_list["nothing"])
        
    def update_objprop_scroll(self):
        for this_prop in self.objprop:
            self.objprop_scroll.insert("end", this_prop + ": " + self.objprop[this_prop].get() + "\n")
        self.objprop_scroll.config(state="disabled")
        
    def update_objprop(self):
        for this_prop in self.objprop:
            self.objprop[this_prop].set(getattr(self.handle_OBJSelector.selected_obj, this_prop))
        self.objprop_scroll.config(state="normal")
        self.objprop_scroll.delete('1.0', "end")
        
###############################################################################
# ITEM control buttons
###############################################################################
class ITEMControls(tk.Frame):
    def __init__(self, root, sprite_path, item_list_in):
        tk.Frame.__init__(self, root)
        
        self.edit_mode = 0
        
        # Layout
        self.item_frame00 = tk.Frame(master=root)
        self.item_frame00.grid(row=0, column=0, columnspan=2, sticky="nw")
        # item list drop down
        self.item_frame10 = tk.Frame(master=root)
        self.item_frame10.grid(row=1, column=0, columnspan=2, sticky="nw")
        # edit mode button
        self.item_frame20 = tk.Frame(master=root)
        self.item_frame20.grid(row=2, column=0, columnspan=2, sticky="nw")
        # item position
        self.item_frame30 = tk.Frame(master=root)
        self.item_frame30.grid(row=3, column=0, columnspan=1, sticky="nw")
        self.item_frame31 = tk.Frame(master=root)
        self.item_frame31.grid(row=3, column=1, columnspan=1, sticky="nw")
        # item textbox
        self.item_frame40 = tk.Frame(master=root)
        self.item_frame40.grid(row=4, column=0, columnspan=2, sticky="nw")
        
        # Handles
        self.handle_ITEMSelector = ITEMSelector(self.item_frame00, sprite_path, item_list_in, self)
        
        # Selected object text
        self.item_choice = tk.StringVar()
        self.item_choice.set(self.handle_ITEMSelector.selected_item.ITEM_id)
        self.item_choice_label = tk.Label(self.item_frame10, textvariable=self.item_choice)
        self.item_choice_label.config(width=16)
        self.item_choice_label.pack()
        
        # edit mode button
        self.item_edit_text = tk.StringVar()
        self.item_edit_text.set("Place")
        self.item_editmode_button = tk.Button(self.item_frame20, textvariable=self.item_edit_text, command=lambda: self.edit_mode_func())
        self.item_editmode_button.pack()
        
        # item positions
        self.item_pos_x = tk.StringVar()
        self.item_pos_y = tk.StringVar()
        self.item_pos_x.set("NULL")
        self.item_pos_y.set("NULL")
        self.item_pos_x_label = tk.Label(self.item_frame30, textvariable=self.item_pos_x)
        self.item_pos_y_label = tk.Label(self.item_frame31, textvariable=self.item_pos_y)
        self.item_pos_x_label.config(width=8)
        self.item_pos_y_label.config(width=8)
        self.item_pos_x_label.pack()
        self.item_pos_y_label.pack()
        
        # item properties
        self.itemprop = {'ITEM_id': tk.StringVar(value="NULL"),
                         'ITEM_id_num' : tk.StringVar(value="NULL"),
                         'sprite' : tk.StringVar(value="NULL"),
                         'item_display_text' : tk.StringVar(value="NULL"),
                         'attack' : tk.StringVar(value="NULL"),
                         'attribute' : tk.StringVar(value="NULL"),
                         'skill_assignment' : tk.StringVar(value="NULL"),
                         'alpha_pixel' : tk.StringVar(value="NULL"),
                         'use' : tk.StringVar(value="NULL"),
                         'equip' : tk.StringVar(value="NULL"),
                         'in_list_index' : tk.StringVar(value="NULL")}
                
        self.itemprop_scroll = tkst.ScrolledText(self.item_frame40,
            wrap   = tk.WORD,
            width  = 24,
            height = 4,
        )
        self.itemprop_scroll.pack()
        self.update_itemprop_scroll()
        
    def edit_mode_func(self):
        if self.edit_mode == 0:
            self.edit_mode = 1
            self.item_edit_text.set("Selection")
        elif self.edit_mode == 1:
            self.edit_mode = 0
            self.item_edit_text.set("Place")
        else:
            self.edit_mode = 0
            self.item_edit_text.set("Place")
            
    def update_itemprop_scroll(self):
        for this_prop in self.itemprop:
            self.itemprop_scroll.insert("end", this_prop + ": " + self.itemprop[this_prop].get() + "\n")
        self.itemprop_scroll.config(state="disabled")
        
    def update_itemprop(self):
        for this_prop in self.itemprop:
            self.itemprop[this_prop].set(getattr(self.handle_ITEMSelector.selected_item, this_prop))
        self.itemprop_scroll.config(state="normal")
        self.itemprop_scroll.delete('1.0', "end")
        
###############################################################################
# NPC sprite viewer
###############################################################################
class NPCSelector(tk.Frame):
    def __init__(self, root, sprite_path, npc_list_in, npc_controls):
        tk.Frame.__init__(self, root)

        self.npc_list = npc_list_in
        self.selected_npc = npc_list[0]
        self.handle_NPCControls = npc_controls

        # position the frame within the window
        self.pack(expand="no", fill="none", side="right")
        
        # create a canvas in the frame (for drawing stuff)
        self.canvas = tk.Canvas(self, relief="sunken")
        # dictate the size of the canvas
        self.canvas.config(width=160, height=16, highlightthickness=0)
        
        # create a vertical scroll bar for the frame
        self.sbarV = tk.Scrollbar(self, orient="vertical")
        # create a horizontal scroll bar for the frame
        self.sbarH = tk.Scrollbar(self, orient="horizontal")
        
        # bind the scroll bars to the canvas
        self.sbarV.config(command=self.canvas.yview)
        self.sbarH.config(command=self.canvas.xview)
        
        # bind the canvas to the scroll bars
        self.canvas.config(yscrollcommand=self.sbarV.set)
        self.canvas.config(xscrollcommand=self.sbarH.set)
        
        # put the scroll bars in the window
        self.sbarV.pack(side="right", fill="y")
        self.sbarH.pack(side="bottom", fill="x")
        
        # bind the mouse button 1
        self.canvas.bind("<Button 1>", self.select_sprite)
        
        # put the canvas in the window
        self.canvas.pack(side="left", expand="yes", fill="both")
        
        self.set_sprite_path(sprite_path)
        self.load_sprite_sheet()
        self.update_display()
        
    def set_sprite_path(self, path_in):
        self.sprite_path = path_in
        
    def load_sprite_sheet(self):
        file_list = sorted(glob.glob("%s%s" % (self.sprite_path, "/*.bmp")))
        
        total_spritesheet = np.zeros((sprites.sprite_y, sprites.sprite_x*np.size(file_list)), dtype='uint8')
        for ii in range(0, np.size(file_list)):
            this_sprite = sprites.bitmap_fix(file_list[ii])
            export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
            total_spritesheet[0:sprites.sprite_y, ii*sprites.sprite_x:(ii*sprites.sprite_x)+sprites.sprite_x] = export_sprite
            
        self.sprite_sheet = total_spritesheet
        
    def update_display(self):
        npc_sprite_list = np.zeros((sprites.sprite_y, sprites.sprite_x*self.npc_list.size), dtype='uint8')
        for ii in range(0, self.npc_list.size):
            jj = 0
            this_sprite_index = self.npc_list[ii].down1
            npc_sprite_list[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = sprites.sprite_indexing(self.npc_list[ii].down1_index, self.sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x])
        
        disp_map = np.ones((np.size(npc_sprite_list, 0), np.size(npc_sprite_list, 1), 3), dtype='uint8')
        disp_map[:, :, 0] = ((np.right_shift(npc_sprite_list, 5) & 7) / 7) * 255
        disp_map[:, :, 1] = ((np.right_shift(npc_sprite_list, 2) & 7) / 7) * 255
        disp_map[:, :, 2] = ((npc_sprite_list & 3) / 3) * 255
        
        # convert the array into a Image object
        im=Image.fromarray(disp_map, 'RGB')
        
        # set the starting point of the scroll
        width,height=im.size
        self.canvas.config(scrollregion=(0,0,width,height))
        
        # convert the Image object into something that can be used in TK
        self.im2 = ImageTk.PhotoImage(image=im)
        
        # Put the image in the canvas
        self.imgtag = self.canvas.create_image(0,0,anchor="nw",image=self.im2)
        
    def select_sprite(self, event):
        canvas = event.widget
        x_pix = np.uint32(canvas.canvasx(event.x))
        y_pix = np.uint32(canvas.canvasy(event.y))
        x_pos = x_pix//sprites.sprite_x
        y_pos = y_pix//sprites.sprite_y
        self.selected_npc = self.npc_list[x_pos + y_pos].createCopy()
        self.selected_npc.set_text("default text")
        self.selected_npc.set_ai(0)
        # update the control objects
        self.handle_NPCControls.npc_choice.set(self.selected_npc.NPC_id)
        self.handle_NPCControls.npc_entry_text.delete(0, 'end')
        self.handle_NPCControls.npc_entry_text.insert(0, self.selected_npc.text)
        self.handle_NPCControls.npc_entry_ai.delete(0, 'end')
        self.handle_NPCControls.npc_entry_ai.insert(0, str(self.selected_npc.ai))
        
    def update_selection(self, npc_in):
        self.selected_npc = npc_in
        self.handle_NPCControls.npc_choice.set(self.selected_npc.NPC_id)
        self.handle_NPCControls.npc_entry_text.delete(0, 'end')
        self.handle_NPCControls.npc_entry_text.insert(0, self.selected_npc.text)
        self.handle_NPCControls.npc_entry_ai.delete(0, 'end')
        self.handle_NPCControls.npc_entry_ai.insert(0, str(self.selected_npc.ai))

###############################################################################
# OBJ sprite viewer
###############################################################################
class OBJSelector(tk.Frame):
    def __init__(self, root, sprite_path, obj_list_in, obj_controls):
        tk.Frame.__init__(self, root)

        self.obj_list = obj_list_in
        self.selected_obj = obj_list[0]
        self.handle_OBJControls = obj_controls

        # position the frame within the window
        self.pack(expand="no", fill="none", side="right")
        
        # create a canvas in the frame (for drawing stuff)
        self.canvas = tk.Canvas(self, relief="sunken")
        # dictate the size of the canvas
        self.canvas.config(width=160, height=16, highlightthickness=0)
        
        # create a vertical scroll bar for the frame
        self.sbarV = tk.Scrollbar(self, orient="vertical")
        # create a horizontal scroll bar for the frame
        self.sbarH = tk.Scrollbar(self, orient="horizontal")
        
        # bind the scroll bars to the canvas
        self.sbarV.config(command=self.canvas.yview)
        self.sbarH.config(command=self.canvas.xview)
        
        # bind the canvas to the scroll bars
        self.canvas.config(yscrollcommand=self.sbarV.set)
        self.canvas.config(xscrollcommand=self.sbarH.set)
        
        # put the scroll bars in the window
        self.sbarV.pack(side="right", fill="y")
        self.sbarH.pack(side="bottom", fill="x")
        
        # bind the mouse button 1
        self.canvas.bind("<Button 1>", self.select_sprite)
        
        # put the canvas in the window
        self.canvas.pack(side="left", expand="yes", fill="both")
        
        self.set_sprite_path(sprite_path)
        self.load_sprite_sheet()
        self.update_display()
        
    def set_sprite_path(self, path_in):
        self.sprite_path = path_in
        
    def load_sprite_sheet(self):
        file_list = sorted(glob.glob("%s%s" % (self.sprite_path, "/*.bmp")))
        
        total_spritesheet = np.zeros((sprites.sprite_y, sprites.sprite_x*np.size(file_list)), dtype='uint8')
        for ii in range(0, np.size(file_list)):
            this_sprite = sprites.bitmap_fix(file_list[ii])
            export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
            total_spritesheet[0:sprites.sprite_y, ii*sprites.sprite_x:(ii*sprites.sprite_x)+sprites.sprite_x] = export_sprite
            
        self.sprite_sheet = total_spritesheet
        
    def update_display(self):
        obj_sprite_list = np.zeros((sprites.sprite_y, sprites.sprite_x*self.obj_list.size), dtype='uint8')
        for ii in range(0, self.obj_list.size):
            jj = 0
            this_sprite_index = self.obj_list[ii].sprite
            obj_sprite_list[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = sprites.sprite_indexing(self.obj_list[ii].sprite_index, self.sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x])
        
        disp_map = np.ones((np.size(obj_sprite_list, 0), np.size(obj_sprite_list, 1), 3), dtype='uint8')
        disp_map[:, :, 0] = ((np.right_shift(obj_sprite_list, 5) & 7) / 7) * 255
        disp_map[:, :, 1] = ((np.right_shift(obj_sprite_list, 2) & 7) / 7) * 255
        disp_map[:, :, 2] = ((obj_sprite_list & 3) / 3) * 255
        
        # convert the array into a Image object
        im=Image.fromarray(disp_map, 'RGB')
        
        # set the starting point of the scroll
        width,height=im.size
        self.canvas.config(scrollregion=(0,0,width,height))
        
        # convert the Image object into something that can be used in TK
        self.im2 = ImageTk.PhotoImage(image=im)
        
        # Put the image in the canvas
        self.imgtag = self.canvas.create_image(0,0,anchor="nw",image=self.im2)
        
    def select_sprite(self, event):
        canvas = event.widget
        x_pix = np.uint32(canvas.canvasx(event.x))
        y_pix = np.uint32(canvas.canvasy(event.y))
        x_pos = x_pix//sprites.sprite_x
        y_pos = y_pix//sprites.sprite_y
        self.selected_obj = self.obj_list[x_pos + y_pos].createCopy()
        # update the control objects
        self.handle_OBJControls.obj_choice.set(self.selected_obj.OBJ_id)
        self.handle_OBJControls.obj_collision_choice.set(self.selected_obj.collision)
        self.handle_OBJControls.update_objprop()
        self.handle_OBJControls.update_objprop_scroll()
        
    def update_selection(self, obj_in):
        self.selected_obj = obj_in
        self.handle_OBJControls.obj_choice.set(self.selected_obj.OBJ_id)
        self.handle_OBJControls.obj_collision_choice.set(self.selected_obj.collision)
        self.handle_OBJControls.update_objprop()
        self.handle_OBJControls.update_objprop_scroll()

###############################################################################
# ITEM sprite viewer
###############################################################################
class ITEMSelector(tk.Frame):
    def __init__(self, root, sprite_path, item_list_in, item_controls):
        tk.Frame.__init__(self, root)

        self.item_list = item_list_in
        self.selected_item = item_list[0]
        self.handle_ITEMControls = item_controls

        # position the frame within the window
        self.pack(expand="no", fill="none", side="right")
        
        # create a canvas in the frame (for drawing stuff)
        self.canvas = tk.Canvas(self, relief="sunken")
        # dictate the size of the canvas
        self.canvas.config(width=160, height=16, highlightthickness=0)
        
        # create a vertical scroll bar for the frame
        self.sbarV = tk.Scrollbar(self, orient="vertical")
        # create a horizontal scroll bar for the frame
        self.sbarH = tk.Scrollbar(self, orient="horizontal")
        
        # bind the scroll bars to the canvas
        self.sbarV.config(command=self.canvas.yview)
        self.sbarH.config(command=self.canvas.xview)
        
        # bind the canvas to the scroll bars
        self.canvas.config(yscrollcommand=self.sbarV.set)
        self.canvas.config(xscrollcommand=self.sbarH.set)
        
        # put the scroll bars in the window
        self.sbarV.pack(side="right", fill="y")
        self.sbarH.pack(side="bottom", fill="x")
        
        # bind the mouse button 1
        self.canvas.bind("<Button 1>", self.select_sprite)
        
        # put the canvas in the window
        self.canvas.pack(side="left", expand="yes", fill="both")
        
        self.set_sprite_path(sprite_path)
        self.load_sprite_sheet()
        self.update_display()
        
    def set_sprite_path(self, path_in):
        self.sprite_path = path_in
        
    def load_sprite_sheet(self):
        file_list = sorted(glob.glob("%s%s" % (self.sprite_path, "/*.bmp")))
        
        total_spritesheet = np.zeros((sprites.sprite_y, sprites.sprite_x*np.size(file_list)), dtype='uint8')
        for ii in range(0, np.size(file_list)):
            this_sprite = sprites.bitmap_fix(file_list[ii])
            export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
            total_spritesheet[0:sprites.sprite_y, ii*sprites.sprite_x:(ii*sprites.sprite_x)+sprites.sprite_x] = export_sprite
            
        self.sprite_sheet = total_spritesheet
        
    def update_display(self):
        item_sprite_list = np.zeros((sprites.sprite_y, sprites.sprite_x*self.item_list.size), dtype='uint8')
        for ii in range(0, self.item_list.size):
            jj = 0
            this_sprite_index = self.item_list[ii].sprite
            item_sprite_list[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = self.sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x]
        
        disp_map = np.ones((np.size(item_sprite_list, 0), np.size(item_sprite_list, 1), 3), dtype='uint8')
        disp_map[:, :, 0] = ((np.right_shift(item_sprite_list, 5) & 7) / 7) * 255
        disp_map[:, :, 1] = ((np.right_shift(item_sprite_list, 2) & 7) / 7) * 255
        disp_map[:, :, 2] = ((item_sprite_list & 3) / 3) * 255
        
        # convert the array into a Image object
        im=Image.fromarray(disp_map, 'RGB')
        
        # set the starting point of the scroll
        width,height=im.size
        self.canvas.config(scrollregion=(0,0,width,height))
        
        # convert the Image object into something that can be used in TK
        self.im2 = ImageTk.PhotoImage(image=im)
        
        # Put the image in the canvas
        self.imgtag = self.canvas.create_image(0,0,anchor="nw",image=self.im2)
        
    def select_sprite(self, event):
        canvas = event.widget
        x_pix = np.uint32(canvas.canvasx(event.x))
        y_pix = np.uint32(canvas.canvasy(event.y))
        x_pos = x_pix//sprites.sprite_x
        y_pos = y_pix//sprites.sprite_y
        self.selected_item = self.item_list[x_pos + y_pos].createCopy()
        # update the control objects
        self.handle_ITEMControls.item_choice.set(self.selected_item.ITEM_id)
        self.handle_ITEMControls.update_itemprop()
        self.handle_ITEMControls.update_itemprop_scroll()
        
    def update_selection(self, item_in):
        self.selected_item = item_in
        self.handle_ITEMControls.item_choice.set(self.selected_item.ITEM_id)
        self.handle_ITEMControls.update_itemprop()
        self.handle_ITEMControls.update_itemprop_scroll()

# create window instance
root = tk.Tk()
root.geometry("800x600") #You want the size of the app to be 500x500
root.resizable(0, 0) #Don't allow resizing in the x or y direction

# frame layout on grids
# Map
layout_00 = tk.Frame(master=root, bd=1, bg="red")
layout_00.grid(row=0, column=0, rowspan=2, sticky="nw")
# Map controls
layout_01 = tk.Frame(master=root, bd=1, bg="green")
layout_01.grid(row=0, column=1, rowspan=2, sticky="nw")
# Sprites
layout_20 = tk.Frame(master=root)
layout_20.grid(row=2, column=0)
# NPCs
layout_02 = tk.Frame(master=root, bg="yellow")
layout_02.grid(row=0, column=2, sticky="nw")
# OBJs
layout_21 = tk.Frame(master=root, bg="grey")
layout_21.grid(row=2, column=1, sticky="nw")
# OBJs
layout_22 = tk.Frame(master=root, bg="magenta")
layout_22.grid(row=2, column=2, sticky="nw")

# Handles
sprite_panel = SpritePanel(layout_20, "/home/pi/Documents/mbed_Graphics/bitmap_sprites", 6, 4, 6, 3)
npc_controls = NPCControls(layout_02, "/home/pi/Documents/mbed_Graphics/bitmap_sprites", npc_list)
obj_controls = OBJControls(layout_21, "/home/pi/Documents/mbed_Graphics/bitmap_sprites", obj_list)
item_controls = ITEMControls(layout_22, "/home/pi/Documents/mbed_Graphics/bitmap_sprites", item_list)
map_panel = MapPanel(layout_00, sprite_panel, npc_controls.handle_NPCSelector, npc_controls, obj_controls.handle_OBJSelector, obj_controls, item_controls.handle_ITEMSelector, item_controls, "/home/pi/Documents/mbed_Graphics/bitmap_sprites")
map_controls = MapControls(layout_01, map_panel, "/home/pi/Documents/mbed_Graphics/old_maps", "/home/pi/Documents/mbed_Graphics/output_maps")
npc_controls.handle_MapPanel = map_panel
obj_controls.handle_MapPanel = map_panel
item_controls.handle_MapPanel = map_panel

# display the window
root.update()
root.mainloop()



#file_list = sorted(glob.glob("%s%s" % ("/home/pi/Documents/mbed_Graphics/bitmap_sprites", "/*.bmp")))
#        
#total_spritesheet = np.zeros((sprites.sprite_y, sprites.sprite_x*np.size(file_list)), dtype='uint8')
#for ii in range(0, np.size(file_list)):
#    this_sprite = sprites.bitmap_fix(file_list[ii])
#    export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
#    total_spritesheet[0:sprites.sprite_y, ii*sprites.sprite_x:(ii*sprites.sprite_x)+sprites.sprite_x] = export_sprite
#sprite_sheet = total_spritesheet
#
#current_map = np.genfromtxt("/home/pi/Documents/mbed_Graphics/output_maps/map003.out", dtype='float64', delimiter=',')
#if np.isnan(current_map[0, np.size(current_map, 1)-1]):
#    current_map = current_map[0:np.size(current_map, 0), 0:np.size(current_map, 1)-1]
#current_map = np.uint8(current_map)
#map_x = np.size(current_map, 1)
#map_y = np.size(current_map, 0)
#             
#total_map = np.zeros((map_y*sprites.sprite_y, map_x*sprites.sprite_x), dtype='uint8')
#for ii in range(0, map_x):
#    for jj in range(0, map_y):
#        this_sprite_index = current_map[jj, ii]
#        #thing = total_spritesheet[(0*sprites.sprite_y):(0*sprites.sprite_y)+sprites.sprite_y-1, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x-1]
#        total_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x]
#        
#disp_map = np.ones((np.size(total_map, 0), np.size(total_map, 1), 4), dtype='uint8')
#disp_map[:, :, 0] = ((np.right_shift(total_map, 5) & 7) / 7) * 255
#disp_map[:, :, 1] = ((np.right_shift(total_map, 2) & 7) / 7) * 255
#disp_map[:, :, 2] = ((total_map & 3) / 3) * 255
#disp_map[:, :, 3] = disp_map[:, :, 3] * 255
#      
#npc_map = np.zeros(np.shape(total_map), dtype='uint8')
#npc_map[7, 2] = 2;
#npc_map[15, 23] = 5;
#npc_map[23, 40] = 4;
#npc_map[27, 31] = 3;
#total_npc_map = np.zeros((map_y*sprites.sprite_y, map_x*sprites.sprite_x), dtype='uint8')
#for ii in range(0, map_x):
#    for jj in range(0, map_y):
#        this_sprite_index = 7
#        if npc_map[jj, ii] != 0:
#            this_sprite_index = 16
#        #thing = total_spritesheet[(0*sprites.sprite_y):(0*sprites.sprite_y)+sprites.sprite_y-1, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x-1]
#        total_npc_map[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x]
#  
#disp_npc_map = np.zeros((np.size(total_npc_map, 0), np.size(total_npc_map, 1), 4), dtype='uint8')
#disp_npc_map[:, :, 0] = ((np.right_shift(total_npc_map, 5) & 7) / 7) * 255
#disp_npc_map[:, :, 1] = ((np.right_shift(total_npc_map, 2) & 7) / 7) * 255
#disp_npc_map[:, :, 2] = ((total_npc_map & 3) / 3) * 255
#temp = np.ones((np.size(total_npc_map, 0), np.size(total_npc_map, 1)), dtype='uint8') * 255
#temp[total_npc_map == 28] = 0
#disp_npc_map[:, :, 3] = temp
## convert the array into a Image object
#imageHead = Image.fromarray(disp_map, 'RGBA')
#imageHand = Image.fromarray(disp_npc_map, 'RGBA')
#
#imageHead.paste(imageHand, (0, 0), imageHand)
## Convert the Image object into a TkPhoto object
#tkimage = ImageTk.PhotoImage(imageHead)    
#
#panel1 = tk.Label(root, image=tkimage)
##panel1 = tk.Label(root)
#panel1.grid(row=0, column=0, sticky='E')





######
#file_list = sorted(glob.glob("%s%s" % ("/home/pi/Documents/mbed_Graphics/bitmap_sprites", "/*.bmp")))
#        
#total_spritesheet = np.zeros((sprites.sprite_y, sprites.sprite_x*np.size(file_list)), dtype='uint8')
#for ii in range(0, np.size(file_list)):
#    this_sprite = sprites.bitmap_fix(file_list[ii])
#    export_sprite = np.left_shift(this_sprite[:, :, 0], 5) + np.left_shift(this_sprite[:, :, 1], 2) + this_sprite[:, :, 2]
#    total_spritesheet[0:sprites.sprite_y, ii*sprites.sprite_x:(ii*sprites.sprite_x)+sprites.sprite_x] = export_sprite
#sprite_sheet = total_spritesheet
#
#npc_sprite_list = np.zeros((sprites.sprite_y, sprites.sprite_x*npc_list.size), dtype='uint8')
#for ii in range(0, npc_list.size):
#    jj = 0
#    this_sprite_index = npc_list[ii].down1
#    npc_sprite_list[(jj*sprites.sprite_y):(jj*sprites.sprite_y)+sprites.sprite_y, (ii*sprites.sprite_x):(ii*sprites.sprite_x)+sprites.sprite_x] = sprite_sheet[0*sprites.sprite_y:(0*sprites.sprite_y)+sprites.sprite_y, this_sprite_index*sprites.sprite_x:(this_sprite_index*sprites.sprite_x)+sprites.sprite_x]
#
#disp_map = np.ones((np.size(npc_sprite_list, 0), np.size(npc_sprite_list, 1), 3), dtype='uint8')
#disp_map[:, :, 0] = ((np.right_shift(npc_sprite_list, 5) & 7) / 7) * 255
#disp_map[:, :, 1] = ((np.right_shift(npc_sprite_list, 2) & 7) / 7) * 255
#disp_map[:, :, 2] = ((npc_sprite_list & 3) / 3) * 255
#
## convert the array into a Image object
#imageHead = Image.fromarray(disp_map, 'RGB')
#
## Convert the Image object into a TkPhoto object
#tkimage = ImageTk.PhotoImage(imageHead)    
#
#panel1 = tk.Label(root, image=tkimage)
##panel1 = tk.Label(root)
#panel1.grid(row=0, column=0, sticky='E')