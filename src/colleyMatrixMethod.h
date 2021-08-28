#pragma once
#include <vector>
#include "config.h"
using namespace std;

class colleyMatrixMethod {
public:
    static vector<metnum_float_t> calculateLeaderboard(int teams, int matches, vector<vector<int>> resultMatrix);
};
