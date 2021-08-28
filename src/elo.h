#pragma once
#include <vector>
#include "config.h"

using namespace std;

class elo {
public:
    static vector<metnum_float_t> calculateLeaderboard(int teamQuantity, int matchesQuantity, const vector<vector<int>>& resultMatrix);
};
