#!/usr/bin/env python3

import argparse
import sys

from lithomancy import load_sticks, touching, Stick, Stone
from svgout import output

DESC = """
Lithomancy, an interpreter and viewer for the esoteric 
programming language Sticks and Stones.
https://esolangs.org/wiki/Sticks_and_Stones
"""


def next_stick(current: Stick, sticks: list[Stick], cond):
    for i, s in enumerate(sticks):
        if s == current:
            try:
                return sticks[i + 1]
            except IndexError as e:
                return None


def run(sticks, stones, lithomancer=None):
    distance = lambda a,b: abs(((b[0] - a[0])**2 + (b[1] - a[1])**2)**0.5)
    rtouching = lambda a,b: 1 >= distance(a.pos, b.pos) 
    output_primed = False
    stick = sticks[0]
    while stick:
        if stick.material in 'abc':
            s = stick.material
            stones[s].move(stick.change)

        # Output hack:
        if output_primed and rtouching(stones['b'], stones['c']):
            # print("B and C are touching!")
            print(chr(int(distance(stones['a'].pos, stones['b'].pos) - 1)), end='')
            output_primed = False
        elif not rtouching(stones['b'], stones['c']):
            output_primed = True
        stick = next_stick(stick, sticks, touching(stones))


def main():
    parser = argparse.ArgumentParser(description=DESC)
    parser.add_argument('source', help='Input source file')
    parser.add_argument('-d', '--debug', help='debug', action='store_true')
    args = parser.parse_args()

    stones = {
        'a': Stone(Stone.AMETHYST, (0, 1.118)),
        'b': Stone(Stone.BERYL, (0.5, 0)),
        'c': Stone(Stone.CHALCEDONY, (0, 0.5))}

    sticks = load_sticks(args.source)

    source = output(sticks)
   
    # Convert source sticks to SVG:
    with open('source.svg', 'w') as f:
        f.write(str(source))

    # Run the sticks:
    lithomancer = None
    run(sticks, stones, lithomancer)

    # print(f'Touching? : {touching(stones)}')
    print('\n\n== Final state ==')
    for stone in stones.values():
        print(f'{stone.name}: {stone.pos}')


if __name__ == '__main__':
    main()
