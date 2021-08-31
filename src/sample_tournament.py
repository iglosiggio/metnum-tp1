""" Inputs:
    1. Distribución de las capacidades de los jugadores (default=gauss:1500,500)
    2. Cantidad de equipos
    3. Tipo de torneo a samplear:
        * Eliminación directa
        * Liga de n partidos (default=1)
        * Fase de grupos + Eliminación directa (las hojas del árbol de
          eliminación directa son ligas pequeñas, cómo la copa mundial FIFA).
        * Jerarquía de ligas (es decir, hay un árbol de ligas de el que
          siempre pasan los n mejores)
    4. Cantidad de torneos a simular
    Outputs:
    1. ground_truth.txt: Los scores generados para cada equipo
    2. schedule.txt: El torneo generado
    3. matches_N.txt: Los resultados del torneo
"""

import random

# List from https://docs.python.org/3/library/random.html#real-valued-distributions
real_valued_distributions = {
    'random': random.random,
    'uniform': random.uniform,
    'triangular': random.triangular,
    'betavariate': random.betavariate,
    'expovariate': random.expovariate,
    'gammavariate': random.gammavariate,
    'gauss': random.gauss,
    'lognormvariate': random.lognormvariate,
    'normalvariate': random.normalvariate,
    'vonmisesvariate': random.vonmisesvariate,
    'paretovariate': random.paretovariate,
    'weibullvariate': random.weibullvariate,
}
def sample_real(dist_name, *args, **kwargs):
    if dist_name not in real_valued_distributions:
        raise ValueError('The requested distribution is not implemented')
    return real_valued_distributions[dist_name](*args, **kwargs)

def parse_dist_arg(arg):
    """ Parses a distribution argument.

        Distribution arguments have the following shape:

        ```
            <distribution> := <dist_name> [':' <arg_list>]
                <arg_list> := <arg> [',' <arg_list>]
                     <arg> := [<arg_name> '='] <FLOAT>
               <dist_name> := <STRING>
                <arg_name> := <STRING>
        ```

        Returns a (dist_name, args, kwargs) triplet.
    """
    (dist_name, sep, all_args) = arg.partition(':')
    dist_name = dist_name.strip()
    all_args = all_args.strip()
    assert all_args != '' or sep == ''
    if sep == '':
        return (dist_name, [], {})
    assert all_args.find(':') == -1
    all_args = [arg for arg in all_args.split(',')]
    assert '' not in all_args
    args = []
    kwargs = {}
    for arg in all_args:
        (param_name, sep, value) = arg.partition('=')
        param_name = param_name.strip()
        value = value.strip()
        assert value == '' or sep == '='
        value = float(value) if sep != '' else float(param_name)
        if sep == '': args.append(value)
        else: kwargs[param_name] = value
    return (dist_name, args, kwargs)

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
    # aleatorio
    sorted_ids = sorted(group_ids, key=lambda id: points[id])
    return sorted_ids[:winners]

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
    with open(filepath, 'w') as file:
        for (match_id, player_a, points_a, player_b, points_b) in matches:
            file.write(f'{match_id} {player_a} {points_a} {player_b} {points_b}\n')

def read_matches_from(filepath):
    """ Reads a list of matches from a file """
    matches = []
    with open(filepath, 'r') as file:
        for line in file.readlines():
            (match_id, player_a, points_a, player_b, points_b) = [int(v) for v in line.split(' ')]
            matches.append((match_id, player_a, points_a, player_b, points_b))
    return matches

if __name__ == '__main__':
    print('Aún no terminé el script...')
    print('Corriendo un par de pruebas')

    print('1. Samplear poblaciones de jugadores')
    elo_distribution = lambda: random.gauss(1500, 400)
    players_128 = sample_players(elo_distribution, 128)
    print('Creados 128 jugadores desde una normal')
    write_players_to(players_128, 'players.txt')
    print('Escritos en players.txt, chequeando que se puedan leer...')
    assert read_players_from('players.txt') == players_128

    print('2. Crear torneos de eliminación simple')
    single_elimination_128 = sample_single_elimination_tournament(players_128, sample_player_order(players_128))
    single_elimination_16 = sample_single_elimination_tournament(players_128[:16], sample_player_order(players_128[:16]))
    write_matches_to(single_elimination_128, 'single-elimination-128.txt')
    write_matches_to(single_elimination_16, 'single-elimination-16.txt')
    print('Escritos en single-elimination-{128,16}.txt, chequeando que se puedan leer...')
    assert read_matches_from('single-elimination-128.txt') == single_elimination_128
    assert read_matches_from('single-elimination-16.txt') == single_elimination_16

    print('3. Creando ligas')
    round_robin_30 = sample_round_robin_tournament(players_128[:30], sample_player_order(players_128[:30]))
    round_robin_11 = sample_round_robin_tournament(players_128[:11], sample_player_order(players_128[:11]))
    write_matches_to(round_robin_30, 'round-robin-30.txt')
    write_matches_to(round_robin_11, 'round-robin-11.txt')
    print('Escritos en round-robin-{30,11}.txt, chequeando que se puedan leer...')
    assert read_matches_from('round-robin-30.txt') == round_robin_30
    assert read_matches_from('round-robin-11.txt') == round_robin_11

    print('4. Creando un torneo a-la-FIFA')
    fifa = sample_fifa_world_cup(players_128[:32], sample_player_order(players_128[:32]))
    write_matches_to(fifa, 'fifa.txt')
    assert read_matches_from('fifa.txt') == fifa
