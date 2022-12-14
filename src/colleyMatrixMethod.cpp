#include "colleyMatrixMethod.h"

using namespace std;

vector<metnum_float_t> colleyMatrixMethod::calculateLeaderboard(const int teams, const int matches, const vector<vector<int>>& resultMatrix) {
    vector<vector<metnum_float_t>> C;
    for (int i = 0; i < teams; ++i){
        C.push_back(vector<metnum_float_t>(teams,0));
        C[i][i] = 2;
    }

    vector<metnum_float_t> wins(teams,0);
    vector<metnum_float_t> losses(teams,0);

    for (int i = 0; i < matches; ++i){
        if (resultMatrix[i][2] > resultMatrix[i][4]) {
            wins[resultMatrix[i][1]]++;
            losses[resultMatrix[i][3]]++;
        } else {
            wins[resultMatrix[i][3]]++;
            losses[resultMatrix[i][1]]++;
        }
        C[resultMatrix[i][1]][resultMatrix[i][3]] -= 1;
        C[resultMatrix[i][3]][resultMatrix[i][1]] -= 1;

        C[resultMatrix[i][1]][resultMatrix[i][1]] += 1;
        C[resultMatrix[i][3]][resultMatrix[i][3]] += 1;
    }

    vector<metnum_float_t> b(teams, 0);
    for(int i = 0; i < teams; i++) {
        b[i] = 1 + (wins[i] - losses[i]) / 2;
    }

    for(int i = 0; i < C.size()-1; i++){
        for(int j = i+1; j < C.size(); j++){
            metnum_float_t m = C[j][i]/C[i][i];
            for (int k = i; k < C.size(); k++){
                C[j][k] = C[j][k] - m * C[i][k];
            }
            b[j] = b[j] - m * b[i];
        }
    }

    vector<metnum_float_t> result;

    for(int i = 0; i < C.size(); i++){
        result.push_back(-1);
    }

    for(int i = C.size()-1; i >= 0; i--){
        metnum_float_t res = b[i];
        for(int j = i+1; j < C.size(); j++){
            res = res - C[i][j]*result[j];
        }
        result[i] = res/C[i][i];
    }

    return result;
}
