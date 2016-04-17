#!/bin/bash
cd ..
cat KilenjeNataraj_VarunBhat_Lab03/serverlist.txt | cut -d " " -f1 | xargs -n1 -i ssh -i ~/planetlab.pem  colostate_CNRL@{} "su - && cd .varun && ps -ef |grep python"
