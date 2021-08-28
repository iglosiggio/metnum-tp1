#pragma once

// Si quieren forzar algún tipo especifico pueden pasar
// -DMETNUM_FLOAT_T=<tipo> cómo parámetro al compilador
#ifdef METNUM_FLOAT_T
using metnum_float_t = METNUM_FLOAT_T;
#else
// Sino comenten y descomenten estas líneas!
//using metnum_float_t = float;
using metnum_float_t = double;
//using metnum_float_t = long double;
#endif