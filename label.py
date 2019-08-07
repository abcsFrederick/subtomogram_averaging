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

    indices = np.transpose(np.where(np.array(image))) + np.array((x, y))
    yield from map(tuple, indices)


def model(labels, height, depth):
    yield from [
        'imod 1',
        'object 0 %d 0' % len(labels),
        'color 0 0 1 0',
        'scattered',
        'symbol square',
        'symsize 1',
    ]
    for i, (label_, (x, y)) in enumerate(labels):
        coordinates = list(label(label_, x, y))
        yield 'contour %d 0 %d' % (i, len(coordinates)*depth)
        for z in range(depth):
            for y_, x_ in coordinates:
                yield '%d %d %d' % (x_, height - y_, z)
            coordinates.reverse()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('nx', type=int)
    parser.add_argument('ny', type=int)
    parser.add_argument('width', type=int)
    parser.add_argument('height', type=int)
    parser.add_argument('depth', type=int, default=1)

    args = parser.parse_args()

    labels = []
    label_ = 1
    for i in range(args.ny):
        for j in range(args.nx):
            labels.append((str(label_), (i * args.height, j * args.width)))
            label_ += 1

    for line in model(labels, args.ny * args.height, args.depth):
        print(line)
