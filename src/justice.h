#pragma once
#include <vector>
#include "config.h"

using namespace std;

class justice {
public:
    static vector<metnum_float_t> calculateLeaderboard(int teamQuantity, int matchesQuantity, const vector<vector<int>>& resultMatrix);
};
