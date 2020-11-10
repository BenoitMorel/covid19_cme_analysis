#!/bin/bash

# Path to the tree vis genesis app
VISCMD="/home/lczech/Dropbox/HITS/genesis/bin/apps/colorize_tree_metadata"

mkdir -p svg
mkdir -p png
mkdir -p pdf

rm -f svg/*.svg
rm -f png/*.png
rm -f pdf/*.pdf

# Make svg trees with the genesis app
for tree in `ls newick/*.newick` ; do
	${VISCMD} ${tree} - ${tree}
done
echo ""

# Convert to PNG with Inkscape
for svg in `ls newick/*.svg` ; do
	echo "inkscape png $svg"
	inkscape --without-gui --export-png="${svg}.png" --export-area-drawing --export-background "#FFFFFF" --export-background-opacity 1.0 --export-height 5000 ${svg}
done
echo ""

# Convert to PDF with Inkscape
for svg in `ls newick/*.svg` ; do
	echo "inkscape pdf $svg"
	inkscape --without-gui --export-pdf="${svg}.pdf" --export-area-drawing --export-background "#FFFFFF" --export-background-opacity 1.0 --export-height 100 ${svg}
done

mv newick/*.svg svg/
mv newick/*.png png/
mv newick/*.pdf pdf/
