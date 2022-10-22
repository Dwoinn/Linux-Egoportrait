#!/usr/bin/python3

import argparse
import pathlib
from video import Webcam

parser = argparse.ArgumentParser(description='Linux Egoportrait\nVirtual Webcam with masked background')
parser.add_argument('--width', '-W', type=int, default=1280, help="Width of the input and output video")
parser.add_argument('--height', '-H', type=int, default=720, help="Height of the input and output video")
parser.add_argument('--input', '-i', type=int, default=0, help="Input webcam id")
parser.add_argument('--output', '-o', type=int, default=7, help="Output virtual webcam id (video4linux2)")
parser.add_argument('--background-image', '-b', dest='background_image', help="Path of the background image")
parser.add_argument('--background-name', '-B', dest='background_name', help="Name of the default background image", 
                      choices=['datacenter', 'officespace1', 'officespace2' ,'server-room-nightmare'])
parser.add_argument('--level', '-l', type=float, default=0.75, help="Segmentation level")

args = parser.parse_args()

print(args)

WIDTH = args.width
HEIGHT = args.height
DEVICE_INPUT = args.input
DEVICE_OUTPUT = f"/dev/video{args.output}"
SEGMENTATION_LEVEL = args.level
BLUR = False

current_path = pathlib.Path(__file__).parent.resolve()

match args.background_name:
  case "datacenter":
    BACKGROUND_PATH=f"{current_path}/backgrounds/datacenter.jpeg"
  case "officespace1":
    BACKGROUND_PATH=f"{current_path}/backgrounds/officespace1.jpg"
  case "officespace2":
    BACKGROUND_PATH=f"{current_path}/backgrounds/officespace2.jpg"
  case "server-room-nightmare":
    BACKGROUND_PATH=f"{current_path}/backgrounds/server-room-nightmare.png"
  case _:
    BACKGROUND_PATH = args.background_image

if BACKGROUND_PATH is None:
  BLUR = True

webcam = Webcam(DEVICE_INPUT, DEVICE_OUTPUT, WIDTH, HEIGHT)

if not BLUR:
  webcam.set_background(BACKGROUND_PATH)

while True:
  webcam.process(SEGMENTATION_LEVEL)