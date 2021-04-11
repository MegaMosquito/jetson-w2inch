# Example code using SPI to drive a Waveshare 2-inch LCD on an NVIDIA Jetson.
# Written by Glen Darling, April 2021.

import board
import datetime
import digitalio
import os
from PIL import Image, ImageDraw, ImageFont
import subprocess
import time
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789

# The gateway address and host address are expected to be in the environment
GATEWAY = os.environ['GATEWAY']
IPADDR = os.environ['IPADDR']

# Commands to check LAN, WAN, etc.
LAN_COMMAND = 'curl -sS https://' + GATEWAY + ' 2>/dev/null | wc -l'
WAN_COMMAND = 'curl -sS https://google.com 2>/dev/null | wc -l'
UPTIME_COMMAND = "uptime | awk '{printf \"up %s avg %.2f\", $3, $(NF-2)}'"

# Setup the display:
BAUDRATE = 24000000
spi = board.SPI()
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)
disp = st7789.ST7789(spi, rotation=90, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)

# Create an 'RGB' drawing canvas
if disp.rotation % 180 == 90:
  # Swap height/width when rotating to landscape!
  height = disp.width
  width = disp.height
else:
  width = disp.width
  height = disp.height
original = Image.new('RGB', (width, height))
draw = ImageDraw.Draw(original)

# Draw a white filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill="#FFFFFF")
disp.image(original)

# Load and scale the DarlingEvil logo image
logo = Image.open("darlingevil.jpg")
darlingevil = logo.resize((75, 75), Image.BICUBIC)
w, h = darlingevil.size

# Load the TTF font sizes for draw.text()
fontlogo = ImageFont.truetype('Ubuntu-M.ttf', 22)
fontstats = ImageFont.truetype('Ubuntu-M.ttf', 20)

# Loop forever, one frame per loop
a = 360
while True:

  # Blank white background to clear screen for next frame
  image = original.copy()
  draw = ImageDraw.Draw(image)

  # Add the darlingevil logo image (rotated to angle "a" in degrees)
  logo = darlingevil.copy()
  logo = logo.rotate(a, fillcolor="#FFFFFF")
  a -= 10
  if a < 0: a += 360
  image.paste(logo, (40, 25))

  # Add the darlingevil.com text
  draw.text((125, 52), "darlingevil.com", font=fontlogo, fill="#000000")

  # Gather some info to show
  lan = '0' != str(subprocess.check_output(LAN_COMMAND, shell=True)).strip()
  wan = '0' != str(subprocess.check_output(WAN_COMMAND, shell=True)).strip()
  lan_str = "UNREACHABLE!"
  lan_color = "#FF0000"
  if lan:
    lan_str = "(connected)"
    lan_color = "#00AA00"
  wan_str = "UNREACHABLE!"
  wan_color = "#FF0000"
  if wan:
    wan_str = "(reachable)"
    wan_color = "#00AA00"
  date_str = datetime.datetime.utcnow().strftime("UTC: %H:%M:%S")
  uptime = subprocess.check_output(UPTIME_COMMAND, shell=True)
  up_str = uptime.decode("utf-8").strip()

  # Draw the text content
  draw.text((40, 110), "IP addr: " + IPADDR, font=fontstats, fill="#0000FF")
  draw.text((40, 135), "Date: " + date_str, font=fontstats, fill="#0000FF")
  draw.text((40, 160), "Uptime: " + up_str, font=fontstats, fill="#0000FF")
  draw.text((40, 185), "LAN status: " + lan_str, font=fontstats, fill=lan_color)
  draw.text((40, 210), "WAN status: " + wan_str, font=fontstats, fill=wan_color)

  # Update the screen, then pause briefly before looping back
  disp.image(image)
  time.sleep(0.02)
