#!/bin/bash

for i in $@; do
  /Applications/Inkscape.app/Contents/Resources/bin/inkscape --without-gui --export-pdf="$(basename $i .svg).pdf" $i
done
