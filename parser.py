import sys
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
parser.add_argument("-v", "--verbosity", action="count", default=0)

args = parser.parse_args()

print(args.x, args.y)
print(int(sys.argv[1]), int(sys.argv[2]))
print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))