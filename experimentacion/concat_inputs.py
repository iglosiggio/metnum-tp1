#!/usr/bin/env python3
""" Simple script for concatenating multiple inputs """
import sys

def main():
    """ Reads the list of inputs from argv and outputs the new matchfile to
        stdout
    """
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} <file 1> <file 2> ... <file n>')
        sys.exit(1)

    last_match_id = 0
    players = set()
    matches = []

    for filepath in sys.argv[1:]:
        with open(filepath, 'r', encoding='utf8') as file:
            for line in file.readlines()[1:]:
                (_, player_a, score_a, player_b, score_b) = [int(v) for v in line.split(' ')]
                players.add(player_a)
                players.add(player_b)
                matches.append((last_match_id, player_a, score_a, player_b,
                                score_b))
                last_match_id += 1

    print(len(players), len(matches))
    for match in matches:
        print(*match)

if __name__ == '__main__':
    main()
