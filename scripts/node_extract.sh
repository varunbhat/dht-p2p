
cd ~/.varun/KilenjeNataraj_VarunBhat_Lab03/node
rm -rf ~/nodejs
wget https://nodejs.org/dist/v4.4.0/node-v4.4.0.tar.gz --no-check-certificate
tar -xzvf node-v4.4.0.tar.gz
cd node-v4.4.0
./configure --prefix=$HOME/nodejs
make
make install

#mv node-v4.4.0-linux-x64 nodejs
#mv nodejs $HOME/
#echo export PATH=$HOME/nodejs/bin:$PATH >> ~/.bashrc 
