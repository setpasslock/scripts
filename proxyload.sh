#!/bin/bash

now=$PWD

#strict, round-robin, dynamic

conf=$1
proxy_path="$HOME/Opt/Proxy/PROXY-List/"
conf_path="$HOME/Myproxychain-conf/"


cd $proxy_path
#git pull && echo "Proxy List is Update"
cd -

if [ $conf = "-h" ]
then
    echo "proxyload.sh [strict, round-robin, dynamic]";

elif [ $conf = "strict" ]
then
	cp ~/Myproxychain-conf/strict_chain.conf $now
	cd $now
	for line in $(cat $proxy_path/socks5.txt)
	do
		proxy_ip=`echo $line | cut -d ":" -f 1`
        	proxy_port=`echo $line | cut -d ":" -f 2`
        	echo "socks4 $proxy_ip $proxy_port" >> strict_chain.conf
    	done

elif [ $conf = "dynamic" ]
then
	cp $HOME/Myproxychain-conf/dynamic_chains.conf $now
	cd $now
	for line in $(cat $proxy_path/socks5.txt)
    	do
        	proxy_ip=`echo $line | cut -d ":" -f 1`
        	proxy_port=`echo $line | cut -d ":" -f 2`
        	echo "socks4 $proxy_ip $proxy_port" >> dynamic_chains.conf
    	done

elif [ $conf = "round-robin" ]
then
        cp $HOME/Myproxychain-conf/round_robin_chainlen_3.conf $now
        cd $now
        for line in $(cat $proxy_path/socks5.txt)
        do
                proxy_ip=`echo $line | cut -d ":" -f 1`
                proxy_port=`echo $line | cut -d ":" -f 2`
                echo "socks4 $proxy_ip $proxy_port" >> round_robin_chainlen_3.conf
        done

fi
