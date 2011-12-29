#!/bin/sh

PARTS=~/.config/Fritzing/parts
SVG_PARTS=$PARTS/svg/user

echo "Copying svg to $SVG_PARTS/"
cp -v parts/svg/breadboard/* $SVG_PARTS/breadboard/
cp -v parts/svg/icon/* $SVG_PARTS/icon/
cp -v parts/svg/pcb/* $SVG_PARTS/pcb/
cp -v parts/svg/schematic/* $SVG_PARTS/schematic/
