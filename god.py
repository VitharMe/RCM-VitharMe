import RPi.GPIO as GPIO

import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# Input pins:
L_pin = 27
R_pin = 23
C_pin = 4
U_pin = 17
D_pin = 22

A_pin = 5
B_pin = 6


GPIO.setmode(GPIO.BCM)

GPIO.setup(A_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(B_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(L_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(R_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(U_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(D_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up
GPIO.setup(C_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Input with pull-up

# Raspberry Pi pin configuration:
RST = 24
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = 2
shape_width = 20
top = padding
bottom = height-padding
x = padding

font = ImageFont.truetype('8.ttf', 6)
fontM = ImageFont.truetype('8.ttf', 15)

draw.text((x, top),    'Do you believe in God?',  font=font, fill=255)
draw.text((x, top+10), 'Yes', font=fontM, fill=255)
draw.text((x, top+40), 'No',  font=fontM, fill=255)
pu = 0
pd = 0
pb = 0

try:
    while 1:
        if GPIO.input(U_pin): # button is released
            draw.rectangle((60,15,70,32), outline=255, fill=pu)  #Up
        else: # button is pressed:
            draw.rectangle((60,15,70,32), outline=255, fill=1)  #Up filled
            pu = 1
            pd = 0

        if GPIO.input(D_pin): # button is released
            draw.rectangle((60,43,70,61), outline=255, fill=pd) #down
        else: # button is pressed:
            draw.rectangle((60,43,70,61), outline=255, fill=1) #down filled
            pu = 0
            pd = 1

        if GPIO.input(B_pin): # button is released
            pass
        else: # button is pressed:
            if pu == 1:
              draw.rectangle((0,0,width,height), outline=0, fill=0)
              draw.text((x, top), 'You believe in God',  font=font, fill=255)
              pb = 1
            else:
              draw.rectangle((0,0,width,height), outline=0, fill=0)
              draw.text((x, top), 'You not believe in God',  font=font, fill=255)
              pb = 1

        if not GPIO.input(A_pin) and not GPIO.input(B_pin) and not GPIO.input(C_pin):
            catImage = Image.open('happycat_oled_64.ppm').convert('1')
            disp.image(catImage)
        else:
            # Display image.
            disp.image(image)

        disp.display()
        time.sleep(.01)
        if pb == 1:
            break

except KeyboardInterrupt:
    GPIO.cleanup()
