FROM ubuntu:latest

RUN apt-get update

RUN apt-get install -y bluez bluetooth usbutils

COPY docker_entrypoint.sh /usr/src/app/docker_entrypoint.sh

ENTRYPOINT sh /usr/src/app/docker_entrypoint.sh