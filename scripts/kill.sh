#!/bin/bash

for server in `cat cs_servers.txt`;do
#       ssh -i vb $server.cs.colostate.edu -l anvesh "hostname && ps -ef |grep unstructpp|grep .v|grep KilenjeNataraj| grep python | grep -v bash | xargs echo | awk {print\$2}"
        ssh -i vb $server.cs.colostate.edu -l anvesh "ps -ef |grep unstructpp | grep anvesh | grep -v grep |  awk {print\$2} | xargs kill -9"
#        ssh -i vb $server.cs.colostate.edu -l anvesh "ps -ef |grep python | grep unstructpp | grep -v grep | awk {print\$2} | xargs kill -9"
#        ssh -i vb $server.cs.colostate.edu -l anvesh "ps -ef |grep unstructpp | grep anvesh | grep -v bash"
done

