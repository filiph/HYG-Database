## For creating PDF maps, run the following in the root directory:

     python svg_export.py && cd export && ../svg2pdf.sh ./*.svg && cd -
     
Pre-requisites:

* Inkscape


## For creating the index file, run this:

    kramdown --template document export/index.md | htmldoc --cont --headfootsize 8.0 --format pdf14 - > export/index.pdf

Pre-requisites:

* kramdown (`sudo gem install kramdown`)