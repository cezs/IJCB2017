#!/bin/sh

datacfg=/media/win/_/IJCB2017/cfg/ijcb2017.data
netcfg=/media/win/_/IJCB2017/cfg/ijcb2017-darknet19.cfg
cmd=${HOME}/Documents/packages/darknet_fork/darknet detector train

$cmd $datacfg $netcfg
