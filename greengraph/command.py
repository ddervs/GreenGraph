from argparse import ArgumentParser
from greengrapher import greengraph


def process():

    parser = ArgumentParser(description="Plots amount of green space between two locations.")
    parser.add_argument('start', help='starting location, string')
    parser.add_argument('end', help='final location, string')
    parser.add_argument('--steps', type=int, default=20, help='number of calculated points, defaults to 20')
    parser.add_argument('--out', help='output file, "*.png" or "*.pdf"', default=False)
    arguments = parser.parse_args()

    greengraph(arguments.start, arguments.end, arguments.steps, arguments.out)

if __name__ == "__main__":
    process()