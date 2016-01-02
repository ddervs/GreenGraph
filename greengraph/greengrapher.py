from matplotlib import pyplot as plt

from greengraph.classes import Greengraph


def greengraph(start, end, steps=20, out=False):

    """ Graphs the number of green pixels between two locations.
    :param start: string, starting location, e.g. 'London'
    :param end: string, final location
    :param steps: int, number of steps
    :param out: string, plot file name *.png or *.pdf
                if False, no plot file made.
    :return:
    """

    mygraph = Greengraph.Greengraph(start, end)
    data = mygraph.green_between(steps)
    plt.plot(data)
    if out:
        plt.savefig(out)
    else:
        plt.show()
