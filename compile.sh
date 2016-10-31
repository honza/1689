BUILD=_build
python main.py -c -e -d $BUILD
pandoc $BUILD/1689.md -o $BUILD/1689.epub
pandoc -s --css=style.css $BUILD/1689.md -o $BUILD/1689.html
ebook-convert $BUILD/1689.epub $BUILD/1689.mobi
xelatex $BUILD/1689.tex
rm 1689.aux 1689.log
mv 1689.pdf $BUILD/
cp style.css $BUILD/
