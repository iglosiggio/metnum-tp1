#pragma once
#include <vector>
#include "config.h"
using namespace std;

class colleyMatrixMethod {
public:
    static vector<metnum_float_t> calculateLeaderboard(int teams, int matches, const vector<vector<int>>& resultMatrix);
};
