#include <algorithm>
#include <fstream>
#include <iostream>
#include <iterator>
#include <numeric>
#include <random>
#include <unordered_map>
#include "../src/colleyMatrixMethod.h"
#include "../src/config.h"
#include "../src/elo.h"
#include "../src/justice.h"
#include "../src/winningPercentage.h"

using namespace std;

vector<vector<int>> readMatrixFromFile(const string& filePath, int& teams, int& matches) {
    vector<vector<int>> resultMatrix;
    ifstream file;
    file.open(filePath);

    if (file.is_open()) {
        file >> teams;
        file >> matches;

        for (int i = 0; i < matches; ++i) {
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

void saveRankingToFile(const vector<metnum_float_t>& ranking, const string& filePath) {
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
    if (argc != 3) {
        cout << "Usage: " << argv[0] << " <id_equipo> <archivo>" << endl;
        return 1;
    }

    int team_id_to_optimize = stoi(argv[1]);
    string filepath(argv[2]);

    int teams = 0;
    int matches = 0;
    vector<vector<int>> resultMatrix = readMatrixFromFile(filepath, teams, matches);
    vector<metnum_float_t> ranking;
    auto team_ids = compress_team_ids(resultMatrix);
    for (auto& match : resultMatrix) {
        match[1] = team_ids.id_to_compressed[match[1]];
        match[3] = team_ids.id_to_compressed[match[3]];
    }

    int compressed_team_id_to_optimize = team_ids.id_to_compressed[team_id_to_optimize];
    vector<int> rank_order(teams);
    iota(rank_order.begin(), rank_order.end(), 0);
    using scoring_method_t = vector<metnum_float_t> (*)(int, int, const vector<vector<int>>&);
    auto get_ranking_for = [&](scoring_method_t method) -> pair<int, metnum_float_t> {
        auto ranking = method(teams, matches, resultMatrix);
        vector<metnum_float_t> sorted_ranking(teams);
	sort(
            rank_order.begin(),
            rank_order.end(),
            [&](int a, int b) -> bool { return ranking[a] > ranking[b]; }
        );

        return {
            find(rank_order.begin(), rank_order.end(), compressed_team_id_to_optimize) - rank_order.begin(),
            ranking[compressed_team_id_to_optimize]
        };
    };

    vector<int> matches_played;
    int matches_won = 0;
    for (int i = 0; i < resultMatrix.size(); i++) {
        if (resultMatrix[i][1] == compressed_team_id_to_optimize) {
            if (resultMatrix[i][2] > resultMatrix[i][4]) matches_won++;
            matches_played.push_back(i);
        } else if (resultMatrix[i][3] == compressed_team_id_to_optimize) {
            if (resultMatrix[i][2] < resultMatrix[i][4]) matches_won++;
            matches_played.push_back(i);
        }
    }

    auto best_cmm_ranking = get_ranking_for(colleyMatrixMethod::calculateLeaderboard);
    auto best_wp_ranking = get_ranking_for(winningPercentage::calculateLeaderboard);
    auto best_justice_ranking = get_ranking_for(justice::calculateLeaderboard);
    auto best_elo_ranking = get_ranking_for(elo::calculateLeaderboard);

    cerr << "Initial rankings (with " << matches_won << " wins): " << endl;
    cerr << " - CMM:     " << best_cmm_ranking.first << "\t(" << best_cmm_ranking.second << ")" << endl;
    cerr << " - WP:      " << best_wp_ranking.first << "\t(" << best_wp_ranking.second << ")" << endl;
    cerr << " - Justice: " << best_justice_ranking.first << "\t(" << best_justice_ranking.second << ")" << endl;
    cerr << " - Elo:     " << best_elo_ranking.first << "\t(" << best_elo_ranking.second << ")" << endl;

    auto force = [&](int i, bool win) {
        if (resultMatrix[i][1] == compressed_team_id_to_optimize) {
            resultMatrix[i][2] = win;
            resultMatrix[i][4] = !win;
        } else if (resultMatrix[i][3] == compressed_team_id_to_optimize) {
            resultMatrix[i][2] = !win;
            resultMatrix[i][4] = win;
        }
    };
    const int NUM_TRIES = 100;
    vector<int> wins;
    mt19937 rnd{std::random_device{}()};
    for (int j : matches_played) force(j, 0);
    cout  << "#Wins"                                  << ","
          << "Best CMM Ranking"                       << ","
          << "Best WP Ranking"                        << ","
          << "Best Justice Ranking"                   << ","
          << "Best Elo Ranking"                       << ","
          << "CMM score for best CMM ranking"         << ","
          << "WP score for best WP ranking"           << ","
          << "Justice score for best Justice ranking" << ","
          << "Elo score for best Elo ranking        " << endl;
    for (int k = matches_played.size(); k >= 0; k--) {
        best_cmm_ranking = {teams+1, 0};
        best_wp_ranking = {teams+1, 0};
        best_justice_ranking = {teams+1, 0};
        best_elo_ranking = {teams+1, 0};

        for (int i = 0; i < NUM_TRIES; i++) {
            for (int j : matches_played) force(j, 0);
            wins.clear();
            sample(matches_played.begin(), matches_played.end(), back_inserter(wins), k, rnd);
            for (int j : wins) force(j, 1);

            auto cmm_ranking = get_ranking_for(colleyMatrixMethod::calculateLeaderboard);
            auto wp_ranking = get_ranking_for(winningPercentage::calculateLeaderboard);
            auto justice_ranking = get_ranking_for(justice::calculateLeaderboard);
            auto elo_ranking = get_ranking_for(elo::calculateLeaderboard);

            if (cmm_ranking.first < best_cmm_ranking.first)
                best_cmm_ranking = cmm_ranking;
            if (wp_ranking.first < best_wp_ranking.first)
                best_wp_ranking = wp_ranking;
            if (justice_ranking.first < best_justice_ranking.first)
                best_justice_ranking = justice_ranking;
            if (elo_ranking.first < best_elo_ranking.first)
                best_elo_ranking = elo_ranking;

            cerr << "." << flush;
        }
        cerr << endl;

        cout  << k                           << ","
              << best_cmm_ranking.first      << ","
              << best_wp_ranking.first       << ","
              << best_justice_ranking.first  << ","
              << best_elo_ranking.first      << ","
              << best_cmm_ranking.second     << ","
              << best_wp_ranking.second      << ","
              << best_justice_ranking.second << ","
              << best_elo_ranking.second     << endl;
    }
}
