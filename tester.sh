#!/usr/bin/env bash

Board = $(./chipboard -b)
echo $Board | ./chipboard -p > cpp.txt
echo $Board | python testPC.py > py.txt
ret = $(diff cpp.txt py.txt)
if [ $ret != "" ]; then
  echo $ret
fi
