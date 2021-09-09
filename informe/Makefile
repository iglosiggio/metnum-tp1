all: informe.pdf

informe.pdf: all_correlations.pdf big_same_single.pdf big_shuffled_single.pdf \
             error_histogram.pdf shuffled_round_robin_42.pdf                  \
             shuffled_single_3.pdf strategic_wins.pdf
	latexmk -pdf main.tex
	mv main.pdf $@

%.pdf: ../experimentacion/%.pdf
	cp $^ $@

../experimentacion/%.pdf:
	$(MAKE) -C ../experimentacion/ $*.pdf

clean:
	latexmk -C
	rm -f *.pdf *.dot

.PHONY: clean all
