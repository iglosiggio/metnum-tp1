#include <iostream>
#include <fstream>
#include "config.h"
#include "colleyMatrixMethod.h"
#include "winningPercentage.h"
#include "justice.h"
#include "elo.h"

using namespace std;

vector<vector<int>> readMatrixFromFile(const string filePath, int *teams, int *matches) {
    vector<vector<int>> resultMatrix;
    ifstream file;
    file.open(filePath);

    if (file.is_open()) {
        file >> *teams;
        file >> *matches;

        for (int i = 0; i < *matches; ++i) {
            vector<int> match;
            for (int j = 0; j < 5; ++j) {
                int val;
                file >> val;
                match.push_back(val);
            }
            resultMatrix.push_back(match);
        }
    }

    return resultMatrix;
}

void saveRankingToFile(const vector<metnum_float_t> ranking, const string filePath) {
    vector<vector<int>> resultMatrix;
    ofstream file;
    file.open(filePath);

    if (file.is_open()) {
        for (int i = 0; i < ranking.size(); ++i) {
            file << ranking[i] << endl;
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 4) {
        cout << "La cantidad de parametros es incorrecta" << endl;
        cout << "1: path al archivo de entrada con los partidos y resultados de la competencia" << endl;
        cout << "2: salida con el ranking correspondiente" << endl;
        cout << "3: metodo a considerar: 0 CMM, 1 WP, 2 justice, 3 elo" << endl;
        return 1;
    }

    vector<string> params(argv + 1, argv + argc);

    int teams = 0;
    int matches = 0;
    vector<vector<int>> resultMatrix = readMatrixFromFile(params[0], &teams, &matches);
    vector<metnum_float_t> ranking;

    if (params[2] == "0") {
        ranking = colleyMatrixMethod::calculateLeaderboard(teams, matches, resultMatrix);
    } else if (params[2] == "1") {
        ranking = winningPercentage::calculateLeaderboard(teams, matches, resultMatrix);
    } else if (params[2] == "2") {
        ranking = justice::calculateLeaderboard(teams, matches, resultMatrix);
    } else if (params[2] == "3") {
        ranking = elo::calculateLeaderboard(teams, matches, resultMatrix);
    } else {
        cout << "Metodo a considerar invalido. Los posibles son: 0 CMM, 1 WP, 2 justice, 3 elo" << endl;
        return 1;
    }

    saveRankingToFile(ranking, params[1]);
}
