#pragma once
#include "config.h"
#include <vector>

using namespace std;

class winningPercentage {
public:
    static vector<metnum_float_t> calculateLeaderboard(int teams, int matches, const vector<vector<int>>& resultMatrix);
};
