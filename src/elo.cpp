#include <cmath>
#include "elo.h"

using namespace std;

/*
Para cada partido entre equipos A y B se calcula el puntaje esperado de cada uno. Por ejemplo,
el esperado de A es 1 / (1 + 10^((eloB-eloA)/400)).
Luego el nuevo elo de A va a depender tanto de su elo actual, del puntaje obtenido en el partido
y del puntaje esperado. La fórmula es: eloA = eloA + K*(resultadoA-esperadoA).
Donde K es una constante que depende del elo del jugador:
    K = 32: para jugadores por debajo de 2100
    K = 24: para jugadores entre 2100 y 2400
    K = 16: para jugadores por encima de 2400
Mientras que el resultado puede ser 1 o 0 ya que no hay empates.    
*/
vector<metnum_float_t> elo::calculateLeaderboard(const int teamQuantity, const int matchesQuantity, const vector<vector<int>>& resultMatrix) {
    vector<metnum_float_t> elo(teamQuantity, 0);

    auto factorK = [](metnum_float_t elo) -> metnum_float_t {
        if (elo < 2100) return 32;
        if (elo > 2400) return 16;
        return 24;
    };

    for (int i = 0; i < matchesQuantity; ++i) {
        metnum_float_t eloA = elo[resultMatrix[i][1]-1];
        metnum_float_t eloB = elo[resultMatrix[i][3]-1];
        metnum_float_t esperadoA = 1 / (1 + pow(10,((eloB-eloA)/400)));
        metnum_float_t esperadoB = 1 / (1 + pow(10,((eloA-eloB)/400)));

        if (resultMatrix[i][2] > resultMatrix[i][4]) {
            //results[resultMatrix[i][1]-1]++;
            elo[resultMatrix[i][1]-1] = eloA + factorK(eloA)*(1-esperadoA);
            elo[resultMatrix[i][3]-1] = eloB + factorK(eloB)*(0-esperadoB);
        } else {
            //results[resultMatrix[i][3]-1]++;
            elo[resultMatrix[i][1]-1] = eloA + factorK(eloA)*(0-esperadoA);
            elo[resultMatrix[i][3]-1] = eloB + factorK(eloB)*(1-esperadoB);
        }

    }

    return elo;
}
