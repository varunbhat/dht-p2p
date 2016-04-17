for server in `cat cs_servers.txt`;do
        ssh -i vb $server.cs.colostate.edu -l anvesh "ps -ef |grep unstructpp | grep anvesh | grep -v grep"
done

