for i in `cat ../serverlist.txt`; do ssh -i ~/planetlab.pem -l colostate_CNRL $i "hostname && sudo ps -ef |grep python|grep varun|grep -v hostname" ;done
