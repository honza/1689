set -e

BUILD=website

echo 'Compiling...'
python main.py -c -d $BUILD

echo 'Building epub...'
pandoc $BUILD/1689.md -o $BUILD/1689.epub

echo 'Building odt...'
pandoc $BUILD/1689.md -o $BUILD/1689.odt

echo 'Building doc...'
pandoc $BUILD/1689.md -o $BUILD/1689.doc

echo 'Building HTML...'
pandoc -s --css=style.css $BUILD/1689.md -o $BUILD/1689.html

echo 'Building mobi...'
ebook-convert $BUILD/1689.epub $BUILD/1689.mobi

echo 'Building PDF...'
xelatex $BUILD/1689.tex
rm 1689.aux 1689.log
mv 1689.pdf $BUILD/
cp style.css $BUILD/
cp index.html $BUILD/
