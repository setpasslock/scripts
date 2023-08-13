#!/bin/bash
url=$1

echo "OPTIONS:"
https -F --print h OPTIONS https://turbo.com "User-Agent: Googlebot/2.1 ( http://www.googlebot.com/bot.html)"
echo "----------------------------------------------------------------------------"


echo "GET"
https -F --print h GET $url "User-Agent: Googlebot/2.1 ( http://www.googlebot.com/bot.html)"
echo "----------------------------------------------------------------------------"

echo "HEAD"
https -F --print h HEAD $url "User-Agent: Googlebot/2.1 ( http://www.googlebot.com/bot.html)"
echo "----------------------------------------------------------------------------"

echo "CONNECT"
curl -X CONNECT $url:443 -I
echo "----------------------------------------------------------------------------"

echo "TRACE"
https -F --print h TRACE $url "User-Agent: Googlebot/2.1 ( http://www.googlebot.com/bot.html)"
echo "----------------------------------------------------------------------------"

echo "PUT"
https -F --print h PUT $url/kjewbfhapytrza.txt "User-Agent: Googlebot/2.1 ( http://www.googlebot.com/bot.html)"

