#!/bin/bash

set -o errexit # Exit on error

function npm-do { (PATH=$(npm bin):$PATH; eval $@;) }

bundle=bundle.js
jsMinifyFile=../orb/static/orb/apps/course_builder.js
cssMinifyFile=../orb/static/orb/apps/course_builder.css

if [ $env = "production" ]
    then
        bundle=bundle.min.js
fi

echo "Copying vendor files"
echo ""
cp vendor/$bundle ../orb/static/orb/apps/bundle.js

echo "Parcel compilation"
echo ""
NODE_ENV=$env node build.js --no-cache --config orb.yaml

if [ $env = "production" ]
    then
        echo "Minifying JS"
        echo "Minifying $jsMinifyFile"
        echo ""
        npm-do minify $jsMinifyFile --out-file $jsMinifyFile

        echo "Minifying CSS"
        echo "Minifying $cssMinifyFile"
        echo ""
        npm-do cleancss -o $cssMinifyFile $cssMinifyFile
        echo "Build complete."
fi
