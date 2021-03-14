import sys
import os

import brute_force_naive
import brute_force_intelligent
import greedy_approximation

from util import Destination

SOLVERS = {
    "-bfn": brute_force_naive.solve,
    "-bfi": brute_force_intelligent.solve,
    "-ga": greedy_approximation.solve
}

"""
Parses an input file and returns the number of stations and the list of destinations.
Input files should be structured with a single number on the first line indicating the
desired number of stations, a single number on the second line indicating the maximum
distance one estimates people will travel to each station, a single number on the
third line indicating the tightness (how quickly LOS drops off before the max distance),
and the following lines each consisting of three comma-separated values indicating
the x coordinate, y coordinate, and population of a destination.

This function does not error-check inputs. Behavior undefined for badly structured input files.
"""
def parse_input(input_file):
    
    num_stations = 0
    destinations = []
    
    with open(input_file, "r") as f:
        # number of stations should be first number in input file
        num_stations = int(f.readline())
        # max distance should be second number
        max_distance = int(f.readline())
        # tightness should be third number
        tightness = int(f.readline())
        # remaining lines should be destination data
        for destination in f:
            # split the line and convert the resulting strings to integers
            data = [int(n) for n in destination.split(', ')]
            # first two numbers are x and y coordinates, last number is population
            destinations.append(Destination(x=data[0], y=data[1], population=data[2]))
    return num_stations, max_distance, tightness, destinations

def main(args):
    num_stations, max_distance, tightness, destinations = (
        parse_input(os.path.join("..", "samples", args[1])))
    solver = SOLVERS[args[2]]
    LOS, stations = solver(num_stations, max_distance, tightness, destinations)
    print("LOS =", LOS)
    for station in stations:
        print("Station at", station)

if __name__ == "__main__":
    main(sys.argv)