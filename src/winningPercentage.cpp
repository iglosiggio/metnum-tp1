#include "winningPercentage.h"

using namespace std;

vector<double> winningPercentage::calculateLeaderboard(const int teamQuantity, const int matchesQuantity, const vector<vector<int>> resultMatrix) {
    vector<double> results(teamQuantity, 0.0);
    vector<int> matchesQuantityPerTeam(teamQuantity, 0);

    for (int i = 0; i < matchesQuantity; ++i) {
        matchesQuantityPerTeam[resultMatrix[i][1]-1]++;
        matchesQuantityPerTeam[resultMatrix[i][3]-1]++;

        if (resultMatrix[i][2] > resultMatrix[i][4]) {
            results[resultMatrix[i][1]-1]++;
        } else {
            results[resultMatrix[i][3]-1]++;
        }
    }

    for (int i = 0; i < results.size(); ++i) {
        results[i] = results[i]/matchesQuantityPerTeam[i];
    }

    return results;
}
