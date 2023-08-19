#!/bin/bash
for i in $(pip3 list -o | awk 'NR > 2 {print $1}'); do sudo pip3 install -U $i; done
