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

def sample_single_elimination_tournament(number_of_teams):
    assert popcount(number_of_teams) == 1
    current_round = list(range(number_of_teams))
    random.shuffle(current_round)
    matches = []
    while len(current_round) >= 2:
        first_match_of_round = -len(matches)-1
        while len(current_round) >= 2:
            match = (current_round.pop(), current_round.pop())
            matches.append(match)
        last_match_of_round = -len(matches)
        matches_played = range(first_match_of_round, last_match_of_round-1, -1)
        current_round.extend(matches_played)
    return matches

def sample_round_robin_tournament(number_of_teams):
    """ Round-robin tournament scheduling based on
        https://en.wikipedia.org/wiki/Round-robin_tournament#Circle_method
    """
    team_order = list(range(number_of_teams))
    number_of_rounds = number_of_teams - 1
    should_skip_first = 0
    random.shuffle(team_order)
    if number_of_teams % 2 == 1:
        team_order.insert(0, number_of_teams)
        number_of_rounds = number_of_teams
        should_skip_first = 1
    matches = []
    for round in range(number_of_rounds):
        half = (number_of_teams + 1) // 2
        # 0   1   2   3 4 ...
        first_half = team_order[should_skip_first:half]
        # n-1 n-2 n-3 n-4 ...
        second_half = team_order[-1:should_skip_first+half-1:-1]
        matches.extend(zip(first_half, second_half))
        team_order[1:] = team_order[-1:] + team_order[1:-1]
    return matches

def write_tournament_to(tournament, filepath):
    with open(filepath, 'w') as file:
        for (home_team_ref, visiting_team_ref) in tournament:
            file.write(f'{home_team_ref} {visiting_team_ref}\n')

def read_tournament_from(filepath):
    matches = []
    with open(filepath, 'r') as file:
        for line in file.readlines():
            (home_team_ref, sep, visiting_team_ref) = line.partition(' ')
            assert sep != ''
            home_team_ref = int(home_team_ref)
            visiting_team_ref = int(visiting_team_ref)
            matches.append((home_team_ref, visiting_team_ref))
    return matches

def tournament_to_dotfile(tournament):
    vertices = set(range(-1, -len(tournament)-1, -1))
    result = 'digraph {\n'
    for match_id, (home_team_ref, visiting_team_ref) in enumerate(tournament):
        result += f'"{home_team_ref}" -> "{-match_id-1}"\n'
        result += f'"{visiting_team_ref}" -> "{-match_id-1}"\n'
        vertices.add(home_team_ref)
        vertices.add(visiting_team_ref)
    for v in vertices:
        if v < 0:
            result += f'"{v}" [label="Match {-v}", shape=circle]\n'
        else:
            result += f'"{v}" [label="Team {v}"]\n'
    result += '}\n'
    return result

if __name__ == '__main__':
    print('Aún no terminé el script...')
    print('Corriendo un par de pruebas')

    print('1. Samplear poblaciones de jugadores')
    elo_distribution = lambda: random.gauss(1500, 400)
    teams = sample_players(elo_distribution, 128)
    print('Creados 128 jugadores desde una normal')
    write_players_to(teams, 'players.txt')
    print('Escritos en players.txt, chequeando que se puedan leer...')
    assert read_players_from('players.txt') == teams

    print('2. Crear torneos de eliminación simple')
    single_elimination_128 = sample_single_elimination_tournament(128)
    single_elimination_16 = sample_single_elimination_tournament(16)
    write_tournament_to(single_elimination_128, 'single-elimination-128.txt')
    write_tournament_to(single_elimination_16, 'single-elimination-16.txt')
    print('Escritos en single-elimination-{128,16}.txt, chequeando que se puedan leer...')
    assert read_tournament_from('single-elimination-128.txt') == single_elimination_128
    assert read_tournament_from('single-elimination-16.txt') == single_elimination_16

    print('3. Creando ligas')
    round_robin_30 = sample_round_robin_tournament(30)
    round_robin_11 = sample_round_robin_tournament(11)
    write_tournament_to(round_robin_30, 'round-robin-30.txt')
    write_tournament_to(round_robin_11, 'round-robin-11.txt')
    print('Escritos en round-robin-{30,11}.txt, chequeando que se puedan leer...')
    assert read_tournament_from('round-robin-30.txt') == round_robin_30
    assert read_tournament_from('round-robin-11.txt') == round_robin_11
