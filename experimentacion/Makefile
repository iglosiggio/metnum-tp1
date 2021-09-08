OBJS=colleyMatrixMethod.f$(METNUM_FLOAT_WIDTH).o \
      winningPercentage.f$(METNUM_FLOAT_WIDTH).o \
                justice.f$(METNUM_FLOAT_WIDTH).o \
                    elo.f$(METNUM_FLOAT_WIDTH).o \
                    tp1.f$(METNUM_FLOAT_WIDTH).o
CXXFLAGS += -std=c++17 -O2

# El diseño original de este Makefile era para permitir compilar el mismo\
# código con distintos floats. No terminamos usando eso.
#BINARIOS = tp.f32 tp.f64 tp.f80 optimize-wins
BINARIOS = tp.f64 optimize-wins

GRAFICOS = strategic_wins.pdf shuffled_single_3.pdf \
           shuffled_round_robin_42.pdf big_shuffled_single.pdf \
           big_same_single.pdf all_correlations.pdf \
           error_histogram.pdf

all: $(BINARIOS) $(GRAFICOS)

tp.f32:
	$(MAKE) METNUM_FLOAT_WIDTH=32 build
tp.f64:
	$(MAKE) METNUM_FLOAT_WIDTH=64 build
tp.f80:
	$(MAKE) METNUM_FLOAT_WIDTH=80 build

tp.f$(METNUM_FLOAT_WIDTH) build: $(OBJS)
	$(CXX) $(CXXFLAGS) $^ -o tp.f$(METNUM_FLOAT_WIDTH)

%.f$(METNUM_FLOAT_WIDTH).o: ../src/%.cpp
	$(CXX) $(CXXFLAGS) -DMETNUM_FLOAT_WIDTH=$(METNUM_FLOAT_WIDTH) -c $< -o $@


OBJS_64=../src/colleyMatrixMethod.cpp \
         ../src/winningPercentage.cpp \
                   ../src/justice.cpp \
                       ../src/elo.cpp
optimize-wins: $(OBJS_64)

experimental-data:
	./sample_tournament.py

experimental-results-f64: experimental-data tp.f64
	./run_all.sh

experimental-results-f64/%: experimental-results-f64
	#

correlations.txt: experimental-results-f64
	./compare_rankings.py --compare-all > correlations.txt

naive-opt.txt: optimize-wins experimental-data
	@echo =====================
	@echo === naive-opt.txt ===
	@echo "Éste es un proceso muy largo, si lo querés correr de verdad ejecutá:"
	@echo "./optimize-wins 15 experimental-data/shuffled-round-robin-16.txt > naive-opt.txt"
	@echo En lugar de eso voy a usar "`naive-opt-old.txt`"
	@echo === naive-opt.txt ===
	@echo =====================
	@cp naive-opt-old.txt naive-opt.txt


big-tournaments/big-%.txt: experimental-data
	mkdir -p big-tournaments
	./concat_inputs.py experimental-data/$**.txt > $@

big-tournaments/big-%.cmm: big-tournaments/big-%.txt tp.f64
	./tp.f64 $< $@ 0

big-tournaments/big-%.wp: big-tournaments/big-%.txt tp.f64
	./tp.f64 $< $@ 1

big-tournaments/big-%.justice: big-tournaments/big-%.txt tp.f64
	./tp.f64 $< $@ 2

big-tournaments/big-%.elo: big-tournaments/big-%.txt tp.f64
	./tp.f64 $< $@ 3

strategic_wins.pdf: experimental-data naive-opt.txt
	./grafico_minmax_victorias.py

all_correlations.pdf: correlations.txt
	./grafico_correlacion_segun_torneo.py

error_histogram.pdf: tp.f64
	./compare_results.py

shuffled_single_3.pdf shuffled_round_robin_42.pdf big_shuffled_single.pdf big_same_single.pdf: \
  experimental-data                                              \
                                                                 \
  experimental-results-f64/shuffled-single-elimination-3.cmm     \
  experimental-results-f64/shuffled-single-elimination-3.wp      \
  experimental-results-f64/shuffled-single-elimination-3.justice \
  experimental-results-f64/shuffled-single-elimination-3.elo     \
                                                                 \
  experimental-results-f64/shuffled-round-robin-42.cmm           \
  experimental-results-f64/shuffled-round-robin-42.wp            \
  experimental-results-f64/shuffled-round-robin-42.justice       \
  experimental-results-f64/shuffled-round-robin-42.elo           \
                                                                 \
  big-tournaments/big-shuffled-single.cmm                        \
  big-tournaments/big-shuffled-single.wp                         \
  big-tournaments/big-shuffled-single.justice                    \
  big-tournaments/big-shuffled-single.elo                        \
                                                                 \
  big-tournaments/big-same-single.cmm                            \
  big-tournaments/big-same-single.wp                             \
  big-tournaments/big-same-single.justice                        \
  big-tournaments/big-same-single.elo
	./scatterplots_del_informe.py

clean:
	rm -f *.o tp.f32 tp.f64 tp.f80 optimize-wins *.pdf

.PHONY: build clean
