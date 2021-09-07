OBJS=colleyMatrixMethod.f$(METNUM_FLOAT_WIDTH).o \
      winningPercentage.f$(METNUM_FLOAT_WIDTH).o \
                justice.f$(METNUM_FLOAT_WIDTH).o \
                    elo.f$(METNUM_FLOAT_WIDTH).o \
                    tp1.f$(METNUM_FLOAT_WIDTH).o
CXXFLAGS += -std=c++17 -O2

all: tp.f32 tp.f64 tp.f80 optimize-wins

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

clean:
	rm -f *.o tp.f32 tp.f64 tp.f80 optimize-wins

.PHONY: build clean
