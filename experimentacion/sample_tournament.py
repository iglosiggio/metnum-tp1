#!/usr/bin/env python3
import random

def sample_players(distribution, number_of_teams):
    """ Given a distribution function sample a list of teams """
    return [distribution() for _ in range(number_of_teams)]

def write_players_to(teams, filepath):
    """ Write a list of teams to a file """
    with open(filepath, 'w') as file:
        for team_elo in teams:
            file.write(f'{team_elo}\n')

def read_players_from(filepath):
    """ Read a list of teams from a file """
    with open(filepath, 'r') as file:
        return [float(team_elo) for team_elo in file.readlines()]

def popcount(v):
    """ Count the number of ones in the binary representation of v """
    assert v >= 0
    result = 0
    while v != 0:
        result += v & 1
        v >>= 1
    return result

def sample_game(elo_player_a, elo_player_b):
    """ Simulates a game between A and B according to their ELO scores.

        Returns a (points_player_a, points_player_b) tuple.
    """
    expected_a = 1 / (1 + 10**((elo_player_b - elo_player_a) / 400))
    return (1, 0) if random.random() <= expected_a else (0, 1)

def sample_player_order(player_elos):
    """ Returns a random permutation of [0,1,...,len(player_elos)]"""
    result = list(range(len(player_elos)))
    random.shuffle(result)
    return result

def sample_single_elimination_tournament(player_elos, player_ids, starting_match_id=0):
    """ Simulates a single-elimination tournament and returns the match
        results
    """
    assert len(player_elos) == len(player_ids)
    assert popcount(len(player_elos)) == 1
    num_players = len(player_ids)
    current_round = list(range(num_players))
    matches = []
    while len(current_round) >= 2:
        winners = []
        while len(current_round) >= 2:
            match_id = starting_match_id + len(matches)
            player_a = current_round.pop()
            player_b = current_round.pop()
            points_a, points_b = sample_game(player_elos[player_a], player_elos[player_b])
            matches.append((match_id, player_ids[player_a], points_a, player_ids[player_b], points_b))
            winners.append(player_a if points_a > points_b else player_b)
        current_round.extend(winners)
    return matches

def sample_round_robin_tournament(player_elos, player_ids, starting_match_id=0):
    """ Simulates a round-robin tournament and returns the match results.

        The scheduling code is based on
        https://en.wikipedia.org/wiki/Round-robin_tournament#Circle_method
    """
    assert len(player_elos) == len(player_ids)
    num_players = len(player_ids)
    team_order = list(range(num_players))
    number_of_rounds = num_players - 1
    should_skip_first = 0
    if num_players % 2 == 1:
        team_order.insert(0, num_players)
        number_of_rounds = num_players
        should_skip_first = 1
    matches = []
    for _ in range(number_of_rounds):
        half = (num_players + 1) // 2
        # 0   1   2   3 4 ...
        first_half = team_order[should_skip_first:half]
        # n-1 n-2 n-3 n-4 ...
        second_half = team_order[-1:should_skip_first+half-1:-1]
        for (player_a, player_b) in zip(first_half, second_half):
            match_id = starting_match_id + len(matches)
            points_a, points_b = sample_game(player_elos[player_a], player_elos[player_b])
            matches.append((match_id, player_ids[player_a], points_a, player_ids[player_b], points_b))
        team_order[1:] = team_order[-1:] + team_order[1:-1]
    return matches

def sample_group(group_num, group_size, player_elos, player_ids, matches, winners, starting_match_id):
    """ Samples a round-robin subtournament for a list of players.

        Returns the winners and appends all the played matches to `matches`
    """
    group_elos = player_elos[group_num * group_size: (group_num + 1) * group_size]
    group_ids = player_ids[group_num * group_size: (group_num + 1) * group_size]
    group_matches = sample_round_robin_tournament(group_elos, group_ids, starting_match_id)
    matches.extend(group_matches)
    points = { player_id: 0 for player_id in group_ids }
    for (_, player_a, points_a, player_b, points_b) in group_matches:
        if points_a > points_b:
            points[player_a] += 3
        elif points_a == points_b:
            points[player_a] += 1
            points[player_b] += 1
        else:
            points[player_b] += 3
    # El desempate viene "por el orden dado en la lista" que suponemos
    # aleatorio (esto vale porque `sorted` es estable!)
    sorted_ids = sorted(group_ids, key=lambda id: points[id])
    return sorted_ids[-winners:]

def sample_fifa_world_cup(player_elos, player_ids, starting_match_id=0):
    """ Simulates "FIFA World Cup (TM)"-like tournament (round-robin groups of
        four + single-elimination) and returns the match results.
    """
    assert len(player_elos) == len(player_ids)
    assert len(player_elos) == 32
    matches = []
    def sample_match(player_a, player_b):
        match_id = len(matches)
        points_a, points_b = sample_game(player_elos[player_a], player_elos[player_b])
        matches.append((match_id, player_a, points_a, player_b, points_b))
        return (player_a, player_b) if points_a > points_b else (player_b, player_a)
    # Basado en https://www.fifa.com/tournaments/mens/worldcup/qatar2022
    # 1. Fase de grupos
    A1, A2 = sample_group(0, 4, player_elos, player_ids, matches, 2, starting_match_id + len(matches))
    B1, B2 = sample_group(1, 4, player_elos, player_ids, matches, 2, starting_match_id + len(matches))
    C1, C2 = sample_group(2, 4, player_elos, player_ids, matches, 2, starting_match_id + len(matches))
    D1, D2 = sample_group(3, 4, player_elos, player_ids, matches, 2, starting_match_id + len(matches))
    E1, E2 = sample_group(4, 4, player_elos, player_ids, matches, 2, starting_match_id + len(matches))
    F1, F2 = sample_group(5, 4, player_elos, player_ids, matches, 2, starting_match_id + len(matches))
    G1, G2 = sample_group(6, 4, player_elos, player_ids, matches, 2, starting_match_id + len(matches))
    H1, H2 = sample_group(7, 4, player_elos, player_ids, matches, 2, starting_match_id + len(matches))
    # 2. Octavos
    W49, _ = sample_match(A1, B2)
    W50, _ = sample_match(C1, D2)
    W51, _ = sample_match(D1, C2)
    W52, _ = sample_match(B1, A2)
    W53, _ = sample_match(E1, F2)
    W54, _ = sample_match(G1, H2)
    W55, _ = sample_match(F1, E2)
    W56, _ = sample_match(H1, G2)
    # 3. Cuartos
    W57, _ = sample_match(W53, W54)
    W58, _ = sample_match(W49, W50)
    W59, _ = sample_match(W55, W56)
    W60, _ = sample_match(W51, W52)
    # 4. Semis
    W61, RU61 = sample_match(W57, W58)
    W62, RU62 = sample_match(W59, W60)
    # 5. Tercer lugar
    sample_match(RU61, RU62)
    # 6. Final
    sample_match(W61, W62)
    return matches

def write_matches_to(matches, filepath):
    """ Writes a list of matches to a file """
    teams = set()
    for match in matches:
        teams.add(match[1])
        teams.add(match[3])

    with open(filepath, 'w') as file:
        file.write(f'{len(teams)} {len(matches)}\n')
        for (match_id, player_a, points_a, player_b, points_b) in matches:
            file.write(f'{match_id} {player_a} {points_a} {player_b} {points_b}\n')

def read_matches_from(filepath):
    """ Reads a list of matches from a file """
    matches = []
    with open(filepath, 'r') as file:
        for line in file.readlines()[1:]:
            (match_id, player_a, points_a, player_b, points_b) = [int(v) for v in line.split(' ')]
            matches.append((match_id, player_a, points_a, player_b, points_b))
    return matches

if __name__ == '__main__':
    from sys import stdout

    random.seed(0xCAFECAFE) # Así a todos nos da lo mismo el script

    try:
        from os import mkdir
        mkdir('experimental-data')
    except FileExistsError:
        pass

    def sample_tournaments(name, amount, callback):
        from sys import stdout
        for i in range(100):
            stdout.write('.')
            stdout.flush()
            write_matches_to(callback(), f'experimental-data/{name}-{i}.txt')
        stdout.write('\n')
        stdout.flush()

    print('Corriendo un par de pruebas')

    print('1... Crear pool de jugadores (experimental-data/players.txt)')
    elo_distribution = lambda: random.gauss(1500, 400)
    players_1024 = sample_players(elo_distribution, 1024)
    write_players_to(players_1024, 'experimental-data/players.txt')

    print('2... Crear torneos de eliminación simple')
    print('2.1. Simulando 100 torneos distintos (shuffled-single-elimination-{0..99}.txt)')
    sample_tournaments('shuffled-single-elimination', 100, lambda: sample_single_elimination_tournament(players_1024, sample_player_order(players_1024)))
    print('2.2. Simulando 100 veces el mismo torneo (same-single-elimination-{0..99}.txt)')
    player_order = sample_player_order(players_1024)
    sample_tournaments('same-single-elimination', 100, lambda: sample_single_elimination_tournament(players_1024, player_order))

    print('3... Creando ligas')
    print('3.1. Simulando 100 torneos distintos (shuffled-round-robin-{0..99}.txt)')
    sample_tournaments('shuffled-round-robin', 100, lambda: sample_round_robin_tournament(players_1024, sample_player_order(players_1024)))
    print('3.2. Simulando 100 veces el mismo torneo (same-round-robin-{0..99}.txt)')
    sample_tournaments('same-round-robin', 100, lambda: sample_round_robin_tournament(players_1024, player_order))
    player_order = sample_player_order(players_1024)

    print('4... Creando torneos a-la-FIFA (usan los 32 primeros equipos)')
    print('4.1. Simulando 100 torneos distintos (shuffled-fifa-{0..99}.txt)')
    sample_tournaments('shuffled-fifa', 100, lambda: sample_fifa_world_cup(players_1024[:32], sample_player_order(players_1024[:32])))
    print('4.2. Simulando 100 veces el mismo torneo (same-fifa-{0..99}.txt)')
    player_order = sample_player_order(players_1024[:32])
    sample_tournaments('same-fifa', 100, lambda: sample_fifa_world_cup(players_1024[:32], player_order))
