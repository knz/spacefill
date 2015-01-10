#! /usr/bin/env python3
# Hilbert and Moore curve generators.
# Requires Python 3.3+.

def hilbert(n, x0, y0, xi, xj, yi, yj):
    """Generate a Hilbert curve.

    This function returns a generator that yields the (x,y) coordinates
    of the Hilbert curve points from 0 to 4^n-1.

    Arguments:
    n      -- the base-4 logarithm of the number of points (ie. the function generates 4^n points).
    x0, y0 -- offset to add to all generated point coordinates.
    xi, yi -- projection-plane coordinates of the curve's I vector (i.e. horizontal, "X" axis).
    xj, yj -- projection-plane coordinates of the curve's J vector (i.e. vertical, "Y" axis).
    """
    if n <= 0:
        yield (x0 + (xi + yi) / 2, y0 + (xj + yj) / 2)
    else:
        yield from hilbert(n - 1, x0,               y0,               yi/2, yj/2, xi/2, xj/2)
        yield from hilbert(n - 1, x0 + xi/2,        y0 + xj/2,        xi/2, xj/2, yi/2, yj/2)
        yield from hilbert(n - 1, x0 + xi/2 + yi/2, y0 + xj/2 + yj/2, xi/2, xj/2, yi/2, yj/2)
        yield from hilbert(n - 1, x0 + xi/2 + yi,   y0 + xj/2 + yj,  -yi/2,-yj/2,-xi/2,-xj/2)

def moore(n, x0, y0, xi, xj, yi, yj):
    """Generate a Moore curve.

    This function returns a generator that yields the (x,y) coordinates
    of the Moore curve points from 0 to 4^n-1.

    Arguments:
    n      -- the base-4 logarithm of the number of points (ie. the function generates 4^n points).
    x0, y0 -- offset to add to all generated point coordinates.
    xi, yi -- projection-plane coordinates of the curve's I vector (i.e. horizontal, "X" axis).
    xj, yj -- projection-plane coordinates of the curve's J vector (i.e. vertical, "Y" axis).
    """
    if n <= 0:
        yield (x0 + (xi + yi) / 2, y0 + (xj + yj) / 2)
    else:
        yield from hilbert(n - 1, x0 + xi/2        , y0 + xj/2        , -xi/2, xj/2, yi/2, yj/2)
        yield from hilbert(n - 1, x0 + xi/2 + yi/2 , y0 + xj/2  + yj/2, -xi/2, xj/2, yi/2, yj/2)
        yield from hilbert(n - 1, x0 + xi/2 + yi   , y0 + xj/2  + yj  ,  xi/2, xj/2, yi/2,-yj/2)
        yield from hilbert(n - 1, x0 + xi/2 + yi/2 , y0 + xj/2  + yj/2,  xi/2, xj/2, yi/2,-yj/2)


if __name__ == "__main__":
    import argparse, shutil, math, subprocess, os, sys

    # Prepare the command-line interface.

    parser = argparse.ArgumentParser(description="Generate Moore or Hilbert curves.")
    parser.add_argument("npoints", metavar="NPOINTS", type=int,
                        help="Desired number of points (must be power of 4).")
    parser.add_argument("--output", "-o", type=argparse.FileType("w"),
                        help="Output file (default to stdout).", default=sys.stdout)
    parser.add_argument("--type", "-t", metavar="TYPE", choices=["moore", "hilbert"],
                        default="hilbert",
                        help="Generate a curve of the specified type. (choices: hilbert, moore)")
    parser.add_argument("--gnuplot", "-g", nargs="?", const="dumb", default=None, metavar="TERM",
                        help="Display the curve using GNUplot. "
                        "The optional argument indicates the GNUplot terminal type, "
                        "defaults to 'dumb' (ASCII art).")
    parser.add_argument("--no-labels", action="store_true",
                        help="Do not print the point labels.")
    parser.add_argument("--fit", nargs=4, metavar="C", type=float,
                        help="Orient/size the curve according to the specified unit vector "
                        "coordinates. The first pair of values sets the X vector; the second "
                        "pair sets the Y vector. The default defines a square that gives all "
                        "points positive coordinates at distance 1 from each other. "
                        "For example use N 0 0 M to fit in a rectangle of size NxM oriented from "
                        "the bottom left to the top right.")
    parser.add_argument("--offset", nargs=2, metavar="C", type=float,
                        help="Translate the curve to the specified position. The default "
                        "tries to position a corner of the curve at coordinates (0,0).")
    args = parser.parse_args()

    # Check and extract arguments.
    n = math.log(args.npoints, 4)
    sq = math.sqrt(args.npoints)
    if n != int(n):
        parser.error("number of points is not a power of 4.")

    fit = args.fit
    if fit is None:
        fit = [sq, 0., 0., sq]

    offset = args.offset
    if offset is None:
        if fit[1] != 0 or fit[2] != 0:
            offset = [0, 0]
        else:
            offset = [-fit[0]/(2*sq), -fit[3]/(2*sq)]

    if args.type == "moore":
        fn = moore
    if args.type == "hilbert":
        fn = hilbert

    # Generate the curve points.
    l = fn(n, *(offset + fit))

    # Display the curve.

    if args.gnuplot is None:
        for lb, (x,y) in enumerate(l):
            if args.no_labels:
                print(x,y, file=args.output)
            else:
                print(x, y, lb, file=args.output)
    else:
        l = list(l)

        tsize = shutil.get_terminal_size()
        cmd = os.getenv("GNUPLOT", "gnuplot")
        proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=args.output, shell=True, universal_newlines=True)

        if args.gnuplot == "dumb":
            print("set term dumb %s %s" % (tsize.columns-2, tsize.lines-2), file=proc.stdin)
        else:
            print("set term %s" % args.gnuplot, file=proc.stdin)

        also_labels = ", '-' with labels"
        if args.no_labels:
            also_labels = ""
        print("set offsets graph 0.1,0.1,0.1,0.1\nset tics out scale 0.5\nset nokey\nplot '-' with lines%s" % also_labels, file=proc.stdin),

        # Data for the curve
        for (x,y) in l:
            print(x, y, file=proc.stdin)
        print("e", file=proc.stdin)

        # Data for the labels
        if not args.no_labels:
            for lb, (x,y) in enumerate(l):
                print(x, y, lb, file=proc.stdin)
            print("e", file=proc.stdin)

        # Done, finish.
        print("quit", file=proc.stdin)
        sys.exit(proc.wait())
