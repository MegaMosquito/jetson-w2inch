# jetson-w2inch

Example python code using SPI to drive a small LCD on an NVIDIA Jetson nano.

I use this container to drive the [Waveshare 2-inch 320x240 LCD screen](https://smile.amazon.com/gp/product/B081Q79X2F/ref=ppx_yo_dt_b_asin_title_o05_s01?ie=UTF8&psc=1). You can usually find these for about $15 USD.

## Host Preparation:

For SPI on NVIDIA Jetson nanos, you need to run this on the *host*:

```
sudo mkdir -p /boot/dtb
sudo cp -v /boot/tegra210-p3448-0000-p3449-0000-[ab]0[02].dtb /boot/dtb/sudo
sudo find /opt/nvidia/jetson-io/ -mindepth 1 -maxdepth 1 -type d -exec touch {}/__init__.py \;
```

Then you need to run the interactive configuration tool:

```
sudo /opt/nvidia/jetson-io/jetson-io.py
```

And in that tool, enable the "SPI1" interface.

If you have trouble with SPI, connect a jumper between pin 19 (SPI1_MOSI) and pin 21 (SPI1_MISO) then run the `spidev_test` program provided in the Docker file. Usage details for that are also in the Dockerfile.

## Usage:

To build the container:

```
make build
```

To run the container (like a daemon, it never exits on its own, and restarts itself after reboots):

```
make run
```

To stop the container from running (and from restarting itself):

```
make stop
```

To clean up everything (remove containers and built images)

```
make clean
```

## More info

See the Makefile, Dockerfile, and python source file for more info. All are small files.

