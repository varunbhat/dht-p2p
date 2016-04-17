#!/bin/bash
#for i in `cat serverlist.txt`;do ssh -i ~/planetlab.pem -l colostate_CNRL $i "bash .varun/KilenjeNataraj_VarunBhat_Lab03/scripts/start.sh" ; done
cat cs_servers.txt  | xargs -i -n1 ssh -i vb {}.cs.colostate.edu -l anvesh "~/.v/lab04/scripts/start.sh"

