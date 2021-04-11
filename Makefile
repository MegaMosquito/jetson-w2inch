# Container that uses SPI to drive a Waveshare 2-inch LCD on an NVIDIA Jetson.

DOCKERHUB_ID:=ibmosquito
NAME:="jetson-w2inch"
VERSION:="1.0.0"

# Get the gateway address
GATEWAY:=$(word 3, $(shell sh -c "ip route | grep default"))
# Get the host IP Address
CIDR=$(shell ip route | grep default | head -1 | sed 's/ proto dhcp / /' | cut -d' ' -f3 | cut -d'.' -f1-3).0/24
IPADDR=$(shell ip route | grep ${CIDR} | head -1 | sed 's/ proto [a-z]*//' | cut -d' ' -f7)

defaut: build run

build:
	docker build -t $(DOCKERHUB_ID)/$(NAME):$(VERSION) .

dev: stop
	docker run -it -v `pwd`:/outside \
	  --privileged \
	  --name ${NAME} \
	  --volume /dev:/dev \
	  --volume /opt:/opt \
	  -e GATEWAY=$(GATEWAY) \
	  -e IPADDR=$(IPADDR) \
	  $(DOCKERHUB_ID)/$(NAME):$(VERSION) /bin/bash

run: stop
	docker run -d \
	  --privileged \
	  --restart=unless-stopped \
	  --name ${NAME} \
	  --volume /dev:/dev \
	  --volume /opt:/opt \
	  -e GATEWAY=$(GATEWAY) \
	  -e IPADDR=$(IPADDR) \
	  $(DOCKERHUB_ID)/$(NAME):$(VERSION)

push:
	docker push $(DOCKERHUB_ID)/$(NAME):$(VERSION) 

stop:
	@docker rm -f ${NAME} >/dev/null 2>&1 || :

clean:
	@docker rmi -f $(DOCKERHUB_ID)/$(NAME):$(VERSION) >/dev/null 2>&1 || :

.PHONY: build dev run push stop clean
