#pragma once

#include <vector>

using namespace std;

class elo {
public:
    static vector<double> calculateLeaderboard(int teamQuantity, int matchesQuantity, vector<vector<int>> resultMatrix);
};
