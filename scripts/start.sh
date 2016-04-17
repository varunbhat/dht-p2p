#!/bin/bash

hostname
cd ~/.v/lab04/
#cd /home/varunbhat/PycharmProjects/Lab03/KilenjeNataraj_VarunBhat_Lab03
#virtualenv --distribute .env
. env/bin/activate

#pip install -r requirements.txt
#pwd

# python clear_bootstrap.py
#hostname && ps -ef |grep python|grep varun|grep -v hostname | awk {print\$2} | xargs kill -9
#ps -ef |grep python|grep anvesh | grep unstructpp | grep -v grep | awk {print\$2}
for i in {18500..18504};do sleep 0.2; setsid ./unstructpp -b 129.82.46.207 -p $i -n 10000 -u ALPHA >/dev/null 2>&1 < /dev/null & done
#setsid python $PWD/main.py -p 10223 -b 129.82.46.207 -n10000 >/dev/null 2>&1 < /dev/null &
