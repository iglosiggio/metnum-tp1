#pragma once
#include <vector>
#include "config.h"

using namespace std;

class elo {
public:
    static vector<metnum_float_t> calculateLeaderboard(int teamQuantity, int matchesQuantity, vector<vector<int>> resultMatrix);
};
