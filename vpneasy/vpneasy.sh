#! /bin/bash

echo "Starting vpneasy"
echo "username = vpnbook"
sleep 1
if [ -d /$HOME/vpneasy ]
then
    echo "Cleaning the history"
    rm -rf /$HOME/vpneasy
    mkdir -p /$HOME/vpneasy/source
    mkdir /$HOME/vpneasy/password
else
    echo "Creating the relevant folders..."
    mkdir -p /$HOME/vpneasy/source/unzips
    mkdir /$HOME/vpneasy/password
fi


basip=`curl ipinfo.io |grep "country"`
wget -P $HOME/vpneasy/password/ https://www.vpnbook.com/password.php?t=0.59793800%201650355776 
echo "Okey, let's go.."
echo "Choose the server by typing its name"

select server in Poland Germany USA Canada France
do
    if [ $server == $Poland ] 
    then
        echo "Downloading resources..."
        wget https://www.vpnbook.com/free-openvpn-account/vpnbook-openvpn-pl226.zip -P /$HOME/vpneasy/source/
        echo "Resource download is complete, taking care of the zip..."
        unzip /$HOME/vpneasy/source/vpnbook-openvpn-pl226.zip -d /$HOME/vpneasy/source/unzips/
        for i in /$HOME/vpneasy/source/unzips/*
        do
            open $HOME/vpneasy/password/password.php\?t\=0.59793800\ 1650355776
            sleep 1
            sudo openvpn $i
            sleep 1
            sonip=`curl ipinfo.io |grep "country"`
            echo $sonip
            if [ $basip != $sonip ]
            then
                break
            else
                echo "Could not connect, trying other vpn files..."
                sleep 1
                continue    
            fi     
        done
        
    elif [ $server == $Germany ]
    then
        echo "Downloading resources..."
        wget https://www.vpnbook.com/free-openvpn-account/vpnbook-openvpn-de4.zip -P /$HOME/vpneasy/source/
        echo "Resource download is complete, taking care of the zip..."
        unzip /$HOME/vpneasy/source/vpnbook-openvpn-de4.zip -d /$HOME/vpneasy/source/unzips/
        for i in /$HOME/vpneasy/source/unzips/*
        do
            echo $i
            sudo openvpn $i
            open /$HOME/vpneasy/password/password.php\?t\=0.59793800\ 1650355776
            sonip=`curl ipinfo.io |grep "country"`
            if [ $basip != $sonip ]
            then
                break
            else
                echo "Could not connect, trying other vpn files..."
                sleep 1
                continue    
            fi     
        done
    elif [ $server == $USA ]
    then
    echo "Downloading resources..."
        wget https://www.vpnbook.com/free-openvpn-account/vpnbook-openvpn-us1.zip -P /$HOME/vpneasy/source/
        echo "Resource download is complete, taking care of the zip..."
        unzip /$HOME/vpneasy/source/vpnbook-openvpn-us1.zip -d /$HOME/vpneasy/source/unzips/
        for i in /$HOME/vpneasy/source/unzips/*
        do
            echo $i
            sudo openvpn $i
            sleep 2
            open /$HOME/vpneasy/password/password.php\?t\=0.59793800\ 1650355776
            sonip=`curl ipinfo.io |grep "country"`
            if [ $basip != $sonip ]
            then
                break
            else
                echo "Could not connect, trying other vpn files..."
                sleep 1
                continue    
            fi     
        done
    elif [ $server == $Canada ]
    then
    echo "Downloading resources..."
        wget https://www.vpnbook.com/free-openvpn-account/vpnbook-openvpn-ca222.zip -P /$HOME/vpneasy/source/
        echo "Resource download is complete, taking care of the zip..."
        unzip /$HOME/vpneasy/source/vpnbook-openvpn-ca222.zip -d /$HOME/vpneasy/source/unzips/
        for i in /$HOME/vpneasy/source/unzips/*
        do
            echo $i
            sudo openvpn $i
            open /$HOME/vpneasy/password/password.php\?t\=0.59793800\ 1650355776
            sonip=`curl ipinfo.io |grep "country"`
            if [ $basip != $sonip ]
            then
                break
            else
                echo "Could not connect, trying other vpn files..."
                sleep 1
                continue    
            fi     
        done
    
    
    elif [ $server == $France ]
    then
    echo "Downloading resources..."
        wget https://www.vpnbook.com/free-openvpn-account/vpnbook-openvpn-fr1.zip -P /$HOME/vpneasy/source/
        echo "Resource download is complete, taking care of the zip..."
        unzip /$HOME/vpneasy/source/vpnbook-openvpn-fr1.zip -d /$HOME/vpneasy/source/unzips/
        for i in /$HOME/vpneasy/source/unzips/*
        do
            echo $i
            sudo openvpn $i
            open /$HOME/vpneasy/password/password.php\?t\=0.59793800\ 1650355776
            sonip=`curl ipinfo.io |grep "country"`
            if [ $basip != $sonip ]
            then
                break
            else
                echo "Could not connect, trying other vpn files..."
                sleep 1
                continue    
            fi     
        done
    
    
    
    
    
    fi
done

