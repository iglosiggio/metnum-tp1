#pragma once

#include <vector>

using namespace std;

class winningPercentage {
public:
    static vector<double> calculateLeaderboard(int teamQuantity, int matchesQuantity, vector<vector<int>> resultMatrix);
};
