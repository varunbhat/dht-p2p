#!/bin/bash

sudo rm -rf Python-2.7.11* 
sudo rm -rf python
#sudo yum --nogpgcheck -y  install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel

wget https://www.python.org/ftp/python/2.7.11/Python-2.7.11.tgz
tar -xzf Python-2.7.11.tgz 

cd Python-2.7.11

./configure --prefix=$HOME/python
sudo rm -rf ~/python
make
make install
