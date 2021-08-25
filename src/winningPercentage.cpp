#include "winningPercentage.h"

using namespace std;

vector<double> winningPercentage::calculateLeaderboard(const int teams, const int matches, const vector<vector<int>> resultMatrix) {
    vector<double> results(teams, 0.0);
    vector<double> matchesPerTeam(teams, 0.0);

    for (int i = 0; i < matches; ++i) {
        matchesPerTeam[resultMatrix[i][1]-1]++;
        matchesPerTeam[resultMatrix[i][3]-1]++;

        if (resultMatrix[i][2] > resultMatrix[i][4]) {
            results[resultMatrix[i][1]-1]++;
        } else {
            results[resultMatrix[i][3]-1]++;
        }
    }

    for (int i = 0; i < results.size(); ++i) {
        results[i] = results[i]/matchesPerTeam[i];
    }

    return results;
}
