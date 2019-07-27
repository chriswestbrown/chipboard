#!/usr/bin/env bash

for i in {0..$1}
do
  echo $i
  ./chipboard -b > board.txt
  ./chipboard -p < board.txt > cpp.txt
  python -W ignore testPC.py < board.txt > py.txt
  diff cpp.txt py.txt
done
