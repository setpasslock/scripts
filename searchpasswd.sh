#!/bin/bash
arg="$1"
curl -s "https://cirt.net/passwords?criteria=$arg" |pup -p "tbody text{}"

