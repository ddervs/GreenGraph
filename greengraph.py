#!/usr/bin/env python
from argparse import ArgumentParser
from classes import Greengraph
from matplotlib import pyplot as plt


if __name__ == "__main__":

    parser = ArgumentParser(description="Plots amount of green space between two locations.")
    parser.add_argument('start', help='starting location, string')
    parser.add_argument('end', help='final location, string')
    parser.add_argument('--steps', type=int, default=20, help='number of calculated points, defaults to 20')
    parser.add_argument('--out', help='output file, "*.png" or "*.pdf"', default=False)
    arguments = parser.parse_args()

    mygraph = Greengraph.Greengraph(arguments.start, arguments.end)
    data = mygraph.green_between(arguments.steps)
    plt.plot(data)
    if arguments.out:
        plt.savefig(arguments.out)
    else:
        plt.show()

