#!/usr/bin/env python3
import math
from os import read

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

def compare_rankings(a: list[float], b: list[float]) -> float:
    """ Naive implementation of Spearman's rank correlation coefficient
    """
    assert len(a) == len(b)

    rank_a = rankings(a)
    rank_b = rankings(b)

    rank_a_mean = sum(rank_a) / len(rank_a)
    rank_b_mean = sum(rank_b) / len(rank_b)
    rank_a_variance = sum((rank - rank_a_mean)**2 for rank in rank_a) / (len(rank_a) - 1)
    rank_b_variance = sum((rank - rank_b_mean)**2 for rank in rank_b) / (len(rank_b) - 1)
    rank_a_stddev = math.sqrt(rank_a_variance)
    rank_b_stddev = math.sqrt(rank_b_variance)
    rank_covariance = sum((rank[0] - rank_a_mean) * (rank[1] - rank_b_mean) for rank in zip(rank_a, rank_b)) / (len(rank_a) - 1)
    return rank_covariance / (rank_a_stddev * rank_b_stddev)

if __name__ == '__main__':
    from sys import argv, exit
    if len(argv) != 3:
        print(f'Usage: {argv[0]} <file a> <file b>')
        exit(1)

    def read_players_from(filepath):
        """ Read a list of teams from a file """
        with open(filepath, 'r') as file:
            return [float(team_elo) for team_elo in file.readlines()]
    a = read_players_from(argv[1])
    b = read_players_from(argv[2])
    print('Rank correlation:', compare_rankings(a, b))
