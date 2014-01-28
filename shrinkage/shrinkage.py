from __future__ import division
import csv
import pprint
from collections import defaultdict
from operator import attrgetter
from itertools import chain
from copy import deepcopy
import argparse
import sys
pp = pprint.PrettyPrinter(indent=4)


# Shrinkage.py
# Felix Sargent
# Computes desired shrinkage from a lumber lot.

parser = argparse.ArgumentParser(description='Calculate Shrinkage')
parser.add_argument('infile', metavar="file.csv", type=argparse.FileType('U'),
                    help='Required csv file')
parser.add_argument('-b', '--boards', action='store_false',
                    help="Hide board calculations")
parser.add_argument('-s', '--shrinkage', metavar='%', default=0.10, type=float,
                    help="Define desired shrinkage (default: .10)")
# parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
#                     default=sys.stdout)
args = parser.parse_args()


class Piece(object):

    """A piece of wood."""

    width = 0
    length = 0
    inches = 0
    bundle = 0
    board_feet = 0

    def __init__(self, width, length, inches, bundle):
        self.width = width  # in inches
        self.length = length  # in feet
        self.inches = inches  # thickness in inches
        self.bundle = bundle  # bundle number.

    def __repr__(self):
        return "Length: %s, Width: %s, Board Feet: %s " % (
            self.length, self.width, self.board_feet()
        )

    def board_feet(self):
        """
        Generate Board Feet.

        Returns Int

        """
        return (self.width * self.length * self.inches) / 12


class Bundle(object):

    """A bundle of pieces"""

    def __init__(self, bundle_id, pieces):
        self.bundle_id = bundle_id
        self.pieces = pieces

    def __repr__(self):
        return "Bundle ID: %s, Pieces: %s, Board Feet: %s" % (
            self.bundle_id,
            len(self.pieces),
            self.board_feet())

    def board_feet(self):
        return sum(a.board_feet() for a in self.pieces)

    def sort(self):
        self.pieces = sorted(self.pieces, key=attrgetter('length', 'width'))


def piece_maker(row):
    pieces = []
    for _ in range(int(row[3])):
        pieces.append(
            Piece(
                bundle=int(row[0]),
                inches=int(row[1]),
                length=int(row[2]),
                width=int(row[4])
            )
        )
    return pieces


def unshrink(dry_bundle):
    target = dry_bundle.board_feet() * (1 + args.shrinkage)
    max_length = max(piece.length for piece in dry_bundle.pieces)
    dry_bundle.sort()
    # Copy the bundle to a wet one
    wet_bundle = deepcopy(dry_bundle)

    while wet_bundle.board_feet() < target:
        if wet_bundle.pieces[0].length < max_length:
            wet_bundle.pieces[0].length = wet_bundle.pieces[0].length + 1
        elif wet_bundle.pieces[0].width < 12:  # No wood is wider than a foot
            wet_bundle.pieces[0].width = wet_bundle.pieces[0].width + 1
        else:
            break
        wet_bundle.sort()

    pp.pprint("Dry %s" % dry_bundle)
    if args.boards:
        pp.pprint(dry_bundle.pieces)
    pp.pprint("Wet %s" % wet_bundle)
    if args.boards:
        pp.pprint(wet_bundle.pieces)
    print(("Shrinkage: %s%%, Target: %s, distance from target: %s\n" %
          (args.shrinkage * 100, target, target - wet_bundle.board_feet())))

def log(string):
    f = open('shrinkage ' + str(args.shrinkage) + '.txt', 'a')
    f.write(string)
    f.close


def load_data():
    bundles = []
    with args.infile as csvfile:
        shrinkage_table = csv.reader(csvfile, delimiter=',')
        next(shrinkage_table)
        pieces = (chain.from_iterable(list(map(piece_maker, shrinkage_table))))
    bundle_dict = defaultdict(list)
    for piece in pieces:
        bundle_dict[piece.bundle].append(piece)
    bundle_dict = dict(bundle_dict)
    for k, v in list(bundle_dict.items()):
        bundles.append(Bundle(k, v))
    for bundle in bundles:
        unshrink(bundle)


load_data()
