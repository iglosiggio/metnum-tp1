#!/usr/bin/env python3
"""
Nuestra implementación del coeficiente de correlación de rankings de Spearman
"""
import math
import os
import sys

def rankings(scores: list[float]) -> list[int]:
    """ Given a list of scores returns a list containing the position in
        the ranking for each team. If multiple teams have the same score
        then they will share the position in the ranking.
    """
    n_teams = len(scores)
    # numpy.argsort pero a lo bestia
    sorted_idxs = sorted(range(n_teams), key=lambda idx: scores[idx], reverse=True)

    result = [None] * n_teams
    rank = 0
    prev_score = math.inf
    for idx in sorted_idxs:
        score = scores[idx]
        result[idx] = rank

        assert score <= prev_score
        if score < prev_score:
            # Si tienen el mismo score que empatan el puesto
            rank += 1
        prev_score = score

    return result

def compare_rankings(scores_a: list[float], scores_b: list[float]) -> float:
    """ Naive implementation of Spearman's rank correlation coefficient """
    assert len(scores_a) == len(scores_b)

    rank_a = rankings(scores_a)
    rank_b = rankings(scores_b)

    rank_a_mean = sum(rank_a) / len(rank_a)
    rank_b_mean = sum(rank_b) / len(rank_b)
    rank_a_variance = sum((rank - rank_a_mean)**2 for rank in rank_a) / (len(rank_a) - 1)
    rank_b_variance = sum((rank - rank_b_mean)**2 for rank in rank_b) / (len(rank_b) - 1)
    rank_a_stddev = math.sqrt(rank_a_variance)
    rank_b_stddev = math.sqrt(rank_b_variance)
    rank_covariance = sum((rank[0] - rank_a_mean) * (rank[1] - rank_b_mean)
                          for rank in zip(rank_a, rank_b)) / (len(rank_a) - 1)
    return rank_covariance / (rank_a_stddev * rank_b_stddev)

def read_players_from(filepath):
    """ Read a list of teams from a file """
    with open(filepath, 'r', encoding='utf8') as file:
        return [float(team_elo) for team_elo in file.readlines()]

def main():
    """ Toma dos rankings e imprime la correlación """
    if len(sys.argv) != 3:
        if len(sys.argv) == 2 and sys.argv[1] == '--compare-all':
            compare_all()
            sys.exit(0)
        print(f'Usage: {sys.argv[0]} <file a> <file b>')
        print(f'       {sys.argv[0]} --compare-all')
        sys.exit(1)

    scores_a = read_players_from(sys.argv[1])
    scores_b = read_players_from(sys.argv[2])
    print('Rank correlation:', compare_rankings(scores_a, scores_b))

def compare_all():
    """ Compara todos los rankings con el 'posta' """

    scores_posta = read_players_from('experimental-data/players.txt')

    for dirname, _, filenames in os.walk('experimental-results-f64'):
        for filename in filenames:
            if filename.startswith('shuffled-single-elimination') \
               or filename.startswith('shuffled-round-robin'):
                scores_nuestros = read_players_from(os.path.join(dirname, filename))
                correlacion = compare_rankings(scores_posta, scores_nuestros)
                print(correlacion, filename)

if __name__ == '__main__':
    main()
