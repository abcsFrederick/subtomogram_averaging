#!/usr/bin/env python

from PIL import Image, ImageFont, ImageDraw

import numpy as np


def label(label='', x=0, y=0, font=None):
    if font is None:
        font = ImageFont.load_default()
    image = Image.new('1', font.getsize('label'))
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), label, fill=1, font=font)
    del draw

    indices = np.array((-1, 1))*np.transpose(np.where(np.array(image))) + np.array((x, y))
    yield from map(tuple, indices)


def model(labels, width, height, depth):
    yield from [
        'imod 1',
        'object 0 %d 0' % len(labels),
        'color 0 0 1 0',
        'scattered',
        'symbol square',
        'symsize 1',
    ]
    h = max(p[0] for _, p in labels)
    for i, (label_, (x, y)) in enumerate(labels):
        coordinates = list(label(label_, (h + 1 - x)*height, y*width))
        yield 'contour %d 0 %d' % (i, len(coordinates)*depth)
        for z in range(depth):
            for y_, x_ in coordinates:
                yield '%d %d %d' % (x_, y_, z)
            coordinates.reverse()


if __name__ == '__main__':
    import argparse
    import csv
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('width', type=int, default=1)
    parser.add_argument('height', type=int, default=1)
    parser.add_argument('depth', type=int, default=1)
    parser.add_argument('file', nargs='?', default='-')

    args = parser.parse_args()

    if args.file == '-':
        file = sys.stdin
    else:
        file = open(args.file)
    labels = [(label, (int(r), int(c))) for label, r, c in csv.reader(file)]

    for line in model(labels, args.width, args.height, args.depth):
        print(line)
