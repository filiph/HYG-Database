#!/bin/bash

DIR="$( cd "$( dirname "$0" )" && pwd )"
cd $DIR

python build.py "$@"

cd export && ../svg2pdf.sh ./*.svg && cd -

jekyll build -s ./jekyll -d ./appengine/static

mkdir -p ./appengine/static/download

cp ./export/stars.csv ./appengine/static/download/
cp ./export/*.md ./appengine/static/download/

zip -r -X -9 ./appengine/static/download/bundle-latest.zip ./export/*.pdf ./export/*.md ./export/*.csv
