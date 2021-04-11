# Tested on NVIDIA Jetson nano 2GB. Expected to work on other Jetsons.

# Dockerized example code for this $15 screen:
#    https://smile.amazon.com/gp/product/B081Q79X2F/ref=ppx_yo_dt_b_asin_title_o05_s01?ie=UTF8&psc=1

# For SPI, you need to (on the *host*:
# sudo mkdir -p /boot/dtb
# sudo cp -v /boot/tegra210-p3448-0000-p3449-0000-[ab]0[02].dtb /boot/dtb/sudo
# sudo find /opt/nvidia/jetson-io/ -mindepth 1 -maxdepth 1 -type d -exec touch {}/__init__.py \;
#
# Then run this
#   sudo /opt/nvidia/jetson-io/jetson-io.py
# and configure spi1

FROM ubuntu:20.04
WORKDIR /

# Install python basics
RUN apt update && apt install -y \
  python3 python3-dev python3-pip \
  python3-pil git

# Optional dev tools
#RUN apt instll -y wget curl jq make vim

# Install the python GPIO library for Jetson
RUN pip3 install Jetson.GPIO
RUN pip3 install adafruit-circuitpython-busdevice
RUN pip3 install spidev
RUN pip3 install adafruit-blinka-displayio
RUN pip3 install adafruit-circuitpython-rgb-display
RUN pip3 install adafruit-circuitpython-st7735

# Copy over the SPI test code and build it (this is optional)
RUN git clone https://github.com/rm-hull/spidev-test
RUN cd spidev-test && gcc spidev_test.c -o /bin/spidev_test
# To test SPI on the nano, first connect a jumper wire between board
# pins #19 and #21 (the SPI1_MOSI and SPI1_MISO oins). Then run this:
#     spidev_test -D /dev/spidev0.0 -v
# The output line starting with "RX" should mirror the line starting with "TX".

# Copy over the DarlingEvil logo, the font, and the daemon code
COPY darlingevil.jpg /
COPY Ubuntu-M.ttf /
COPY jetson-w2inch.py /

# Run the daemon
CMD python3 /jetson-w2inch.py

