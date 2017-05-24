#!/bin/sh

destination=$1

for f in *.jpg
do
    convert $f "${f%.*}.png"
    convert "${f%.*}.png" $f
    echo "Converted $f"
done
