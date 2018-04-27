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
import time
import serial


class Canvas(tk.Frame):
    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.config_ui()
        self.config_background()
        self.config_vars()
        self.config_port()
        self.config_statusbar()
        self.config_buttons()
        self.canvas.bind("<Configure>", self.resize)

    def config_ui(self):
        self.width = 1280
        self.height = 720
        self.master.title("FreeDar")
        self.master.resizable(True, True)
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bd=0, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=1)

    def config_background(self):
        self.title = self.canvas.create_text(10, 10, text=' FreeDar Visualisation v1.0', anchor=tk.NW)

        self.center_y = self.height / 2
        self.center_x = self.width / 2

        self.grid_y = self.canvas.create_line(self.center_x, 0, self.center_x, self.height, dash=4, tag="grid_y")
        self.grid_x = self.canvas.create_line(0, self.center_y, self.width, self.center_y, dash=4, tag="grid_x")

        self.grid_range1 = self.canvas.create_oval(self.center_x - 100, self.center_y - 100, self.center_x + 100, self.center_y + 100, dash=4, tag="grid_range1")
        self.text_range1 = self.canvas.create_text(self.center_x + 5, self.center_y - 100, text='1 m', anchor=tk.SW, tag="text_range1")

        self.grid_range2 = self.canvas.create_oval(self.center_x - 200, self.center_y - 200, self.center_x + 200, self.center_y + 200, dash=4, tag="grid_range2")
        self.text_range2 = self.canvas.create_text(self.center_x + 5, self.center_y - 200, text='2 m', anchor=tk.SW, tag="text_range2")

    def config_vars(self):
        self.lines = tk.BooleanVar()
        self.lines.set(True)
        self.points = tk.BooleanVar()
        self.points.set(True)

        self.comport = tk.StringVar()
        self.comport.set("COM1")
        self.connected = tk.BooleanVar()
        self.connected.set(False)
        self.saving = tk.BooleanVar()
        self.saving.set(False)
        self.button_save_text = tk.StringVar()
        self.button_save_text.set("Start saving")

        self.x_array = []
        self.y_array = []

        self.p_radius = 2

    def config_statusbar(self):
        self.statusbar = tk.Label(self.canvas, text="Standing By", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.statusbar_window = self.canvas.create_window(0, self.height, width=1920, anchor=tk.SW, window=self.statusbar, tag ="statusbar_window")

    def savedata(self):
        import datetime
        self.now = datetime.datetime.now()

        if self.saving.get() == False:
            self.statusbar.configure(text= "Saving...")
            self.button_save_text.set("Stop saving")
            self.saving.set(True)
        elif self.saving.get() == True:
            df = pd.DataFrame({'x': self.x_array, 'y': self.y_array})
            datetime = str(self.now.month) + "_" + str(self.now.day) + "_" + str(self.now.hour) + "_" + str(self.now.minute)
            self.filename = "file_" + str(datetime) + ".csv"
            df.to_csv(self.filename)
            self.saving.set(False)
            self.button_save_text.set("Start saving")
            self.statusbar.configure(text="Saved")

    def resize(self, event):
        self.canvas.delete("grid_y", "grid_x", "grid_range1", "grid_range2")
        self.w, self.h = event.width, event.height
        self.canvas.create_line(self.w / 2, 0, self.w / 2, self.h, dash=4, tag="grid_y")
        self.canvas.create_line(0, self.h / 2, self.w, self.h / 2, dash=4, tag="grid_x")
        self.center_x = self.w / 2
        self.center_y = self.h / 2
        self.canvas.create_oval(self.center_x - 100, self.center_y - 100, self.center_x + 100, self.center_y + 100, dash=4, tag="grid_range1")
        self.canvas.create_oval(self.center_x - 200, self.center_y - 200, self.center_x + 200, self.center_y + 200, dash=4, tag="grid_range2")
        self.canvas.coords("text_range1", self.center_x + 5, self.center_y - 100)
        self.canvas.coords("text_range2", self.center_x + 5, self.center_y - 200)
        self.canvas.coords("text_status", self.w - 10, self.h)
        self.canvas.coords("statusbar_window", 0, self.h)
        self.width = self.w
        self.height = self.h

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.master.destroy()

    def config_buttons(self):
        self.button_lines = tk.Checkbutton(self.canvas, text="Lines", anchor=tk.W, variable=self.lines, onvalue=tk.TRUE, offvalue=tk.FALSE)
        self.button_lines_window = self.canvas.create_window(10, 30, anchor=tk.NW, window=self.button_lines)

        self.button_points = tk.Checkbutton(self.canvas, text="Points", anchor=tk.W, variable=self.points, onvalue=tk.TRUE, offvalue=tk.FALSE)
        self.button_points_window = self.canvas.create_window(10, 60, anchor=tk.NW, window=self.button_points)

        self.button_save = tk.Button(self.canvas, textvariable=self.button_save_text, command=self.savedata, anchor=tk.NW)
        self.button_save.configure(activebackground="#33B5E5")
        self.button_save = self.canvas.create_window(10, 90, anchor=tk.NW, window=self.button_save)

    def config_port(self):
        self.comport_text = self.canvas.create_text(10, 130, anchor=tk.NW, text=" Select COM port:")

        self.comport_select = tk.OptionMenu(self.master, self.comport, "COM1", "COM2", "COM3", "COM4", "COM5", "COM6",
                                        "COM7", "SIM")
        self.comport_select.pack()
        self.portselect_window = self.canvas.create_window(10, 150, anchor=tk.NW, window=self.comport_select)

        self.button_connect = tk.Button(self.master, text="Connect", anchor=tk.NW, command=self.connect)
        self.button_connect.configure(activebackground="#33B5E5")
        self.button_connect = self.canvas.create_window(110, 151, anchor=tk.NW, window=self.button_connect)

    def connect(self):
        if self.connected.get() == False:                       # tries to connect when sim is selected, implement ifs
            try:
                ser = serial.Serial(port=self.comport.get(), baudrate=9600)
                self.connected.set(True)
            except serial.SerialException:
                self.statusbar.configure(text="Error: Could not connect to sensor")
        if self.connected.get() == True:
            try:
                ser.close()
            except UnboundLocalError:
                self.statusbar.configure(text="Disconnected")
                self.connected.set(False)

        if self.comport.get() == "SIM":
            self.angle = tl.e_angle_s(200, 2 * np.pi)  # for testing
            self.data = tl.e_data_s(200, 2 * np.pi, 2, 4)
            self.connected.set(True)
            self.statusbar.configure(text="Simulating data")

    def drawlines(self):
        for i in range(0, len(self.data)):  # Translate input data into coordinates
            y = self.center_y - np.sin(self.angle[i]) * self.data[i] * 100
            x = self.center_x + np.cos(self.angle[i]) * self.data[i] * 100

            self.x_array.append(x)
            self.y_array.append(y)

            if self.lines.get() == 1:  # Plot coordinates as lines
                self.canvas.delete("line_id[i]")
                self.line_id = self.canvas.create_line(self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2, x, y, tag="line_id")

            if self.points.get() == 1:
                self.canvas.delete("point_id[i]")
                self.point_id = self.canvas.create_oval(x - self.p_radius, y - self.p_radius, x + self.p_radius,
                                              y + self.p_radius, width=0, fill='red', tag="point_id")
                # time.sleep(0.01)
            self.canvas.update()
        self.canvas.delete("line_id", "point_id")

root = tk.Tk()
mainWindow = Canvas(root)

while True:
    mainWindow.update()
    if mainWindow.saving.get() == False:                        # purge array if not saving
        mainWindow.x_array = []
        mainWindow.y_array = []

    if mainWindow.connected.get() == True:                      # start drawing lines if connected
        mainWindow.drawlines()

    mainWindow.update_idletasks()
    mainWindow.update()
    root.protocol("WM_DELETE_WINDOW", mainWindow.on_closing)

root.mainloop()
