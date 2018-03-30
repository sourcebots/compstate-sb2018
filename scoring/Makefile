
all: score-sheet-2018.pdf

%.pdf: %.svg
	inkscape -A colour-$@ $<
	gs -sOutputFile=$@ -sDEVICE=pdfwrite \
		-sColorConversionStrategy=Gray -dProcessColorModel=/DeviceGray \
		-dCompatibilityLevel=1.4 -dNOPAUSE -dBATCH colour-$@

clean:
	rm -f *.pdf
