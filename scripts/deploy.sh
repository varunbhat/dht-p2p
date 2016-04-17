#!/bin/bash
cd ../../

cat KilenjeNataraj_VarunBhat_Lab03/serverlist.txt | cut -d " " -f1 | xargs -n1 -i ssh -i ~/planetlab.pem  colostate_CNRL@{} "rm -rf .varun/*"
tar -czvf KilenjeNataraj_VarunBhat_Lab03.tar.gz KilenjeNataraj_VarunBhat_Lab03/*
cat KilenjeNataraj_VarunBhat_Lab03/serverlist.txt | cut -d " " -f1 | xargs -n1 -i scp -i ~/planetlab.pem KilenjeNataraj_VarunBhat_Lab03.tar.gz  colostate_CNRL@{}:~/.varun/
# cat KilenjeNataraj_VarunBhat_Lab03/serverlist.txt | cut -d " " -f1 | xargs -n1 -i ssh -i ~/planetlab.pem  colostate_CNRL@{} "rm ~/varun/* -r"
cat KilenjeNataraj_VarunBhat_Lab03/serverlist.txt | cut -d " " -f1 | xargs -n1 -i ssh -i ~/planetlab.pem  colostate_CNRL@{} "cd .varun && hostname && tar -xzvf KilenjeNataraj_VarunBhat_Lab03.tar.gz"
