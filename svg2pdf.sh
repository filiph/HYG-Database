#!/bin/bash

DIR="$(pwd)"

for i in $@; do
  echo "svg2pdf: Converting $i to pdf."
  full_path="$DIR/$i"
  pdf_path="$(basename "$i" .svg).pdf"
  full_pdf_path="$DIR/$pdf_path"
  /Applications/Inkscape.app/Contents/Resources/bin/inkscape --without-gui --export-pdf="$full_pdf_path" "$full_path"
done
