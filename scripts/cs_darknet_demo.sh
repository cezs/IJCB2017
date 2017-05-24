#!/bin/sh

datacfg=/media/win/_/IJCB2017/cfg/ijcb2017.data
netcfg=/media/win/_/IJCB2017/cfg/ijcb2017-yolo-voc-bi-valid.cfg
weights=/media/win/_/IJCB2017/weights/ijcb2017-yolo-voc-train_15000.weights
cmd=${HOME}/Documents/packages/darknet_fork/darknet detector train

$cmd $datacfg $netcfg $weights -c 0
