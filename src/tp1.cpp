#include <iostream>
#include <fstream>
#include <unordered_map>
#include <algorithm>
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

void saveRankingToFile(const vector<metnum_float_t>& ranking, const string filePath) {
    vector<vector<int>> resultMatrix;
    ofstream file;
    file.open(filePath);

    if (file.is_open()) {
        for (int i = 0; i < ranking.size(); ++i) {
            file << ranking[i] << endl;
        }
    }
}

struct compressed_team_ids {
    unordered_map<int, int> id_to_compressed;
    vector<int> compressed_to_id;
};
struct compressed_team_ids compress_team_ids(const vector<vector<int>>& matches) {
    unordered_map<int, int> id_to_compressed;
    vector<int> compressed_to_id;
    int last_team_id = 0;
    bool inserted;
    for (auto& match : matches) {
        inserted = id_to_compressed.insert({match[1], last_team_id}).second;
        if (inserted) {
            last_team_id++;
            compressed_to_id.push_back(match[1]);
        }
        inserted = id_to_compressed.insert({match[3], last_team_id}).second;
        if (inserted) {
            last_team_id++;
            compressed_to_id.push_back(match[3]);
        }
    }
    return { id_to_compressed, compressed_to_id };
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
    auto team_ids = compress_team_ids(resultMatrix);
    for (auto& match : resultMatrix) {
        match[1] = team_ids.id_to_compressed[match[1]];
        match[3] = team_ids.id_to_compressed[match[3]];
    }

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

    vector<int> sorted_ids = team_ids.compressed_to_id;
    vector<metnum_float_t> sorted_ranking(teams);
    sort(sorted_ids.begin(), sorted_ids.end());
    for (int i = 0; i < ranking.size(); i++)
        sorted_ranking[i] = ranking[team_ids.id_to_compressed[sorted_ids[i]]];
    saveRankingToFile(sorted_ranking, params[1]);
}
