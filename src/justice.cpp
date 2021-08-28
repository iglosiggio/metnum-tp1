#include "justice.h"

using namespace std;

/*
El ranking se basa en el
   porcentaje de ganados +
     el promedio de:
       la suma del winning percentage de los rivales a los que se le ganó
       la suma del losing percentage (1 - winning percentage) de los rivales con los que se perdió

En la primera pasada se calculan los ganados y jugados y
en la segunda la suma de los porcentajes de los rivales
*/

vector<metnum_float_t> justice::calculateLeaderboard(const int teamQuantity, const int matchesQuantity, const vector<vector<int>>& resultMatrix) {
    vector<metnum_float_t> results(teamQuantity, 0.0);
    vector<metnum_float_t> matchesQuantityPerTeam(teamQuantity, 0);
    vector<metnum_float_t> matchesRivals(teamQuantity, 0);

    for (int i = 0; i < matchesQuantity; ++i) {
        matchesQuantityPerTeam[resultMatrix[i][1]-1]++;
        matchesQuantityPerTeam[resultMatrix[i][3]-1]++;

        if (resultMatrix[i][2] > resultMatrix[i][4]) {
            results[resultMatrix[i][1]-1]++;
        } else {
            results[resultMatrix[i][3]-1]++;
        }
    }

    for (int i = 0; i < matchesQuantity; ++i) {

        if (resultMatrix[i][2] > resultMatrix[i][4]) {
            matchesRivals[resultMatrix[i][1]-1]+=results[resultMatrix[i][3]-1]/matchesQuantityPerTeam[resultMatrix[i][3]-1];
            matchesRivals[resultMatrix[i][3]-1]-=(1.0-results[resultMatrix[i][1]-1]/matchesQuantityPerTeam[resultMatrix[i][1]-1]);
        } else {
            matchesRivals[resultMatrix[i][1]-1]-=(1.0-results[resultMatrix[i][3]-1]/matchesQuantityPerTeam[resultMatrix[i][3]-1]);
            matchesRivals[resultMatrix[i][3]-1]+=(1.0-results[resultMatrix[i][1]-1]/matchesQuantityPerTeam[resultMatrix[i][3]-1]);
        }
    }

    for (int i = 0; i < results.size(); ++i) {
        results[i] = (results[i]+matchesRivals[i])/matchesQuantityPerTeam[i];
    }

    return results;
}
