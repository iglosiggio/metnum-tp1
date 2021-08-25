#pragma once

#include <vector>

using namespace std;

class winningPercentage {
public:
    static vector<double> calculateLeaderboard(int teams, int matches, vector<vector<int>> resultMatrix);
};
