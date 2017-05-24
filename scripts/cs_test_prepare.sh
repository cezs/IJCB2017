#!/bin/sh

cp ijcb2017.test.list ijcb2017.valid.list
awk '{print "/media/win/_/IJCB2017/test/" $0}' ijcb2017.test.list.csv > ijcb2017.test.list
dos2unix ijcb2017.test.list

awk 'NR%1000==1 {file = FILENAME "_" sprintf("%04d", NR+999)} {print > file}' ijcb2017.test.list
