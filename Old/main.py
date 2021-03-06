"""
@Title:         Main FreeDar code
@Description:   Analyses and visualizes data from arduino LIDAR setup
@Author:        R.D. Beerman
@Date:          10/04/2018
@License:
"""

from tkinter import *
from tkinter import messagebox
import numpy as np
import tools as tl
import pandas as pd
import serial

"""init TkInter"""
width = 1280
height = 720
tk = Tk()
tk.title("FreeDar")
tk.resizable(True, True)
# tk.wm_attributes("-topmost" 1)                     # enables the window to always be on the top
canvas = Canvas(tk, width=width, height=height, bd=0, highlightthickness=0)
canvas.pack(fill=BOTH, expand=1)
comport = StringVar(tk)
comport.set("COM1")
tk.update()

""""init Variables"""
angle = tl.e_angle_s(200, 2 * np.pi)                        # for testing
# data = tl.e_data_s(200, 2 * np.pi, 2, 4)                   # for testing, obsolete
x_array = []
y_array = []
lines = True
points = True
saving = False
connected = False
status = "Not Connected"
p_radius = 2
tick = 0

"""init Functions"""
def linesButtonSwitch():
    global lines
    if lines == True:
        canvas.delete("line_id")
        lines = False

    elif lines == False:
        lines = True


def pointsButtonSwitch():
    global points
    if points == True:
        canvas.delete("point_id")
        points = False
    elif points == False:
        points = True


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        canvas.destroy()


def resize(event):
    global center_x
    global center_y
    global width
    global height
    canvas.delete("grid_y", "grid_x", "grid_range1", "grid_range2")
    w, h = event.width, event.height
    canvas.create_line(w / 2, 0, w / 2, h, dash=4, tag="grid_y")
    canvas.create_line(0, h / 2, w, h / 2, dash=4, tag="grid_x")
    center_x = w / 2
    center_y = h / 2
    width = w
    height = h
    canvas.create_oval(center_x - 100, center_y - 100, center_x + 100, center_y + 100, dash=4, tag="grid_range1")
    canvas.create_oval(center_x - 200, center_y - 200, center_x + 200, center_y + 200, dash=4, tag="grid_range2")
    canvas.coords("text_range1", center_x, center_y - 100)
    canvas.coords("text_range2", center_x, center_y - 200)
    canvas.coords("text_status", width - 10, height)


def connect():
    global connected
    if connected == False:
        try:
            ser = serial.Serial(port='COM3', baudrate=9600)
        except serial.SerialException:
            print("Error: could not connect to sensor")
        connected = True


def savedata():
    global x_array
    global y_array
    global saving
    global status

    import datetime
    now = datetime.datetime.now()

    if saving == False:
        status = "Saving..."
        saving = True
    else:
        df = pd.DataFrame({'x': x_array, 'y': y_array})
        datetime = str(now.month) +"_"+ str(now.day) +"_"+ str(now.hour) +"_"+ str(now.minute)
        filename = "file_" + str(datetime) + ".csv"
        df.to_csv(filename)
        saving = False
        status = "Saved"

""""init UI"""
title = canvas.create_text(10, 10, text=' FreeDar Visualisation v1.0', anchor=NW)

center_y = height / 2
center_x = width / 2
grid_y = canvas.create_line(center_x, 0, center_x, height, dash=4, tag="grid_y")
grid_x = canvas.create_line(0, center_y, width, center_y, dash=4, tag="grid_x")
grid_range1 = canvas.create_oval(center_x-100, center_y-100, center_x+100, center_y+100, dash=4, tag="grid_range1")
text_range1 = canvas.create_text(center_x, center_y - 100, text='1 m', anchor=SW, tag="text_range1")
grid_range2 = canvas.create_oval(center_x-200, center_y-200, center_x+200, center_y+200, dash=4, tag="grid_range2")
text_range2 = canvas.create_text(center_x, center_y - 200, text='2 m', anchor=SW, tag="text_range2")

button_lines = Checkbutton(tk, text="Lines", anchor=W, variable=lines, onvalue=TRUE, offvalue=FALSE, command=linesButtonSwitch)
button_lines_window = canvas.create_window(10, 30, anchor=NW, window=button_lines)
button_lines.toggle()

button_points = Checkbutton(tk, text="Points", command=pointsButtonSwitch, anchor=W)
button_points_window = canvas.create_window(10, 60, anchor=NW, window=button_points)
button_points.toggle()

portselect = OptionMenu(tk, comport, "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7")
portselect_window = canvas.create_window(10, 120, anchor=NW, window=portselect)
portselect.pack()

button_save = Button(tk, text="Toggle Saving", command=savedata, anchor=W)
button_save.configure(width=15, activebackground="#33B5E5", relief=FLAT)
button_save = canvas.create_window(10, 90, anchor=NW, window=button_save)

while True:
    canvas.delete("point_id","line_id")                   # for refresh after one circle, for testing
    canvas.delete("text_status")                          # for refreshing the status field

    text_status = canvas.create_text(width-10, height, text=" Status: " + status, anchor=SE, tag="text_status")

    if saving == False:
        x_array = []                                      # purge x array
        y_array = []                                      # purge y_array

    for i in range(0, len(angle)):                         # Translate input data into coordinates
        if connected == True:
            data = float(ser.readline())
            y = center_y - np.sin(angle[i]) * data * 100
            x = center_x + np.cos(angle[i]) * data * 100
            x_array.append(x)
            y_array.append(y)
            status = "Connected"
            if lines == True:  # Plot coordinates as lines
                canvas.delete("line_id[i]")
                line_id = canvas.create_line(canvas.winfo_width() / 2, canvas.winfo_height() / 2, x, y, tag="line_id")

            if points == True:
                canvas.delete("point_id[i]")
                point_id = canvas.create_oval(x - p_radius, y - p_radius, x + p_radius,
                                              y + p_radius, width=0, fill='red', tag="point_id")
        if connected == False:
            satus = "Failed to connect"

            #time.sleep(0.01)
        tk.update()

    tick = tick + 1
    #print(tick)                                           # for debugging
    canvas.update_idletasks()
    #time.sleep(0.1)                                       # if slowdown is needed
    canvas.bind("<Configure>", resize)
    tk.protocol("WM_DELETE_WINDOW", on_closing)
    tk.update()

tk.mainloop()
ser.close()
