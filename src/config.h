#pragma once

// Si quieren forzar algún tipo especifico pueden pasar
// -DMETNUM_FLOAT_WIDTH=<cantidad_de_bits> cómo parámetro al compilador
#ifdef METNUM_FLOAT_WIDTH
#  if METNUM_FLOAT_WIDTH == 32
using metnum_float_t = float;
#  elif METNUM_FLOAT_WIDTH == 64
using metnum_float_t = double;
#  elif METNUM_FLOAT_WIDTH == 80
using metnum_float_t = long double;
#  else
#    error "No conozco un float con el tamaño solicitado"
#  endif
#include <climits>
#else
// Sino comenten y descomenten estas líneas!
//using metnum_float_t = float;
using metnum_float_t = double;
//using metnum_float_t = long double;
#endif
