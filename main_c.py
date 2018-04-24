"""
@Title:         Main FreeDar code
@Description:   Analyses and visualizes data from arduino LIDAR setup
@Author:        R.D. Beerman
@Date:          10/04/2018
@License:
"""
import tkinter as tk
from tkinter import messagebox
import numpy as np
import tools as tl
import pandas as pd
import serial


class Canvas(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.config_ui()
        self.config_background()
        self.config_vars()
        self.config_buttons()
        self.canvas.bind("<Configure>", self.resize)

    def config_ui(self):
        self.width = 1280
        self.height = 720
        self.master.title("FreeDar")
        self.master.resizable(True, True)
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bd=0, highlightthickness=0)
        self.canvas.pack(expand=1)
        return (self.canvas)

    def config_background(self):
        self.title = self.canvas.create_text(10, 10, text=' FreeDar Visualisation v1.0', anchor=tk.NW)

        self.center_y = self.height / 2
        self.center_x = self.width / 2

        self.grid_y = self.canvas.create_line(self.center_x, 0, self.center_x, self.height, dash=4, tag="grid_y")
        self.grid_x = self.canvas.create_line(0, self.center_y, self.width, self.center_y, dash=4, tag="grid_x")

        self.grid_range1 = self.canvas.create_oval(self.center_x - 100, self.center_y - 100, self.center_x + 100, self.center_y + 100, dash=4, tag="grid_range1")
        self.text_range1 = self.canvas.create_text(self.center_x, self.center_y - 100, text='1 m', anchor=tk.SW, tag="text_range1")

        self.grid_range2 = self.canvas.create_oval(self.center_x - 200, self.center_y - 200, self.center_x + 200, self.center_y + 200, dash=4, tag="grid_range2")
        self.text_range2 = self.canvas.create_text(self.center_x, self.center_y - 200, text='2 m', anchor=tk.SW, tag="text_range2")

    def config_vars(self):
        self.lines = tk.BooleanVar()
        self.lines.set(True)
        self.points = tk.BooleanVar()
        self.points.set(True)
        self.comport = tk.StringVar()
        self.comport.set = "COM1"

    def savedata(selfs):
        print("saving placeholder")

    def resize(self, event):
        self.canvas.delete("grid_y", "grid_x", "grid_range1", "grid_range2")
        self.w, self.h = event.width, event.height
        self.canvas.create_line(self.w / 2, 0, self.w / 2, self.h, dash=4, tag="grid_y")
        self.canvas.create_line(0, self.h / 2, self.w, self.h / 2, dash=4, tag="grid_x")
        self.center_x = self.w / 2
        self.center_y = self.h / 2
        self.width = self.w
        self.height = self.h
        self.canvas.create_oval(self.center_x - 100, self.center_y - 100, self.center_x + 100, self.center_y + 100, dash=4, tag="grid_range1")
        self.canvas.create_oval(self.center_x - 200, self.center_y - 200, self.center_x + 200, self.center_y + 200, dash=4, tag="grid_range2")
        self.canvas.coords("text_range1", self.center_x, self.center_y - 100)
        self.canvas.coords("text_range2", self.center_x, self.center_y - 200)
        self.canvas.coords("text_status", self.width - 10, self.height)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

    def config_buttons(self):
        self.button_lines = tk.Checkbutton(self.master, text="Lines", anchor=tk.W, variable=self.lines, onvalue=tk.TRUE, offvalue=tk.FALSE)
        self.button_lines_window = self.canvas.create_window(10, 30, anchor=tk.NW, window=self.button_lines)

        self.button_points = tk.Checkbutton(self.master, text="Points", anchor=tk.W, variable=self.points, onvalue=tk.TRUE, offvalue=tk.FALSE)
        self.button_points_window = self.canvas.create_window(10, 60, anchor=tk.NW, window=self.button_points)

        #self.portselect = tk.OptionMenu(self.master, self.comport, "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7")
        #self.portselect_window = self.canvas.create_window(10, 120, anchor=tk.NW, window=self.portselect)
        #self.portselect.pack()

        self.button_save = tk.Button(self.master, text="Toggle Saving", command=self.savedata, anchor=tk.W)
        self.button_save.configure(width=15, activebackground="#33B5E5", relief=tk.FLAT)
        self.button_save = self.canvas.create_window(10, 90, anchor=tk.NW, window=self.button_save)


tick = 1
root = tk.Tk()
mainWindow = Canvas(root)

while True:
    mainWindow.update()
    #print(tick)
    tick = tick + 1
    root.protocol("WM_DELETE_WINDOW", mainWindow.on_closing)

root.mainloop()
