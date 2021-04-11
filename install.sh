#!/bin/bash

apt-get update
apt-get install -y --no-install-recommends wget tzdata libopencv-dev build-essential libssl-dev libpq-dev libcurl4-gnutls-dev libexpat1-dev gettext unzip python3-setuptools python3-pip python3-dev python3-venv git gcc g++ openjdk-8-jre openjdk-8-jdk nasm gnupg ca-certificates php software-properties-common python2
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
apt-get update
echo "deb https://download.mono-project.com/repo/ubuntu stable-focal main" | tee /etc/apt/sources.list.d/mono-official-stable.list
apt-get install -y --no-install-recommends mono-devel
apt-get clean

# Install PascalABC.NET
mkdir pascal
cd pascal
wget http://pascalabc.net/downloads/PABCNETC.zip
unzip PABCNETC.zip
rm PABCNETC.zip
cd -
