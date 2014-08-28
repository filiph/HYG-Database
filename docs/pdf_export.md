## For creating PDF maps, run the following in the root directory:

     python svg_export.py && cd export && ../svg2pdf.sh ./*.svg && cd -
     
Pre-requisites:

* Inkscape

## For creating the ZIP file

    mv export 2d-star-map-v1.1-literary && zip -r -X -9 2d-star-map-v1.1-literary.zip ./2d-star-map-v1.1-literary && mv 2d-star-map-v1.1-literary export


## For creating the index file, run this:

    kramdown --template document export/index.md | htmldoc --cont --headfootsize 8.0 --format pdf14 - > export/index.pdf
    
and

    kramdown --template document export/index_all.md | htmldoc --cont --headfootsize 8.0 --format pdf14 - > export/index_all.pdf

Pre-requisites:

* kramdown (`sudo gem install kramdown`)