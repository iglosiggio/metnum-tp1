#include <iostream>
#include <fstream>
#include "colleyMatrixMethod.h"
#include "winningPercentage.h"

using namespace std;

vector<vector<int>> readMatrixFromFile(const string filePath, int *teamQuantity, int *matchesQuantity) {
    vector<vector<int>> resultMatrix;
    ifstream file;
    file.open(filePath);

    if (file.is_open()) {
        file >> *teamQuantity;
        file >> *matchesQuantity;

        for (int i = 0; i < *matchesQuantity; ++i) {
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

void saveRankingToFile(const vector<double> ranking, const string filePath) {
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
        cout << "3: metodo a considerar: 0 CMM, 1 WP, 2 alternativo" << endl;
        return 1;
    }

    vector<string> params(argv + 1, argv + argc);

    int teamQuantity = 0;
    int matchesQuantity = 0;
    vector<vector<int>> resultMatrix = readMatrixFromFile(params[0], &teamQuantity, &matchesQuantity);
    vector<double> ranking;

    if (params[2] == "0") {
        ranking = colleyMatrixMethod::calculateLeaderboard(teamQuantity, matchesQuantity, resultMatrix);
    } else if (params[2] == "1") {
        ranking = winningPercentage::calculateLeaderboard(teamQuantity, matchesQuantity, resultMatrix);
    } else if (params[2] == "2") {
        //TODO: ranking = ...::calculateLeaderboard(teamQuantity, matchesQuantity, resultMatrix);
    } else {
        cout << "Metodo a considerar invalido. Los posibles son: 0 CMM, 1 WP, 2 alternativo" << endl;
        return 1;
    }

    saveRankingToFile(ranking, params[1]);
}
