# FreeDar
FreeDar is a simple utility for reading and saving data from a serial based [LIDAR](https://en.wikipedia.org/wiki/Lidar)/[RADAR](https://en.wikipedia.org/wiki/Radar) system.
By using a range finder sensor (such as a VL53L0X ToF sensor) and rotating it around a center axis and recording the measured range and relative angle at which the measurement was made, a point cloud can be made describing the surrounding area.

## Features
Freedar offers the following features, subject to change:

* Select serial port of sensor.
* Toggle between displaying options.
* Save data as .csv file.

Some of the planned features are:

* Ability to change scale.
* Combining data from multiple sensors.
* Line detection in point cloud using Hough Transform.
* Navigation using [SLAM](https://en.wikipedia.org/wiki/Simultaneous_localization_and_mapping).

## Hardware
FreeDar ingests it's data over a serial connection in the shape of: "range, angle". FreeDar is tested with a custom, arduino based LIDAR, the code for which is provided in ~\Arduino
The currently used VL53L0X ToF sensor has the advantage of being simple to work with, relatively fast and accurate. However, it's range is very limited at around 1 meter, so in the future a ultrasonic HC-SR04 will be used to provide range data at ranges higher than 1 meter.

## Dependencies
FreeDar is written in Python 3.6, it's dependencies are:

* tkinter
* numpy
* pandas
* time
* serial