#!/usr/bin/env python
import csv
from itertools import starmap

import numpy as np

import SimpleITK as sitk


def coordinates(volume_filename):
    volume = sitk.ReadImage(volume_filename)
    return volume.GetOrigin(), volume.GetSpacing(), volume.GetDirection()


def parse_fcsv(fcsv_filename):
    with open(fcsv_filename) as fcsv_file:
        reader = csv.reader(fcsv_file)
        for row in reader:
            if not row or row[0].startswith('#'):
                continue
            id = row[0]
            x, y, z = row[1:4]
            ow, ox, oy, oz = row[4:8]
            vis, sel, lock = row[8:11]
            label, desc = row[11:13]
            associated_node_id = row[13]
            yield tuple(map(float, (x, y, z))) + (fcsv_filename, label)


def _offset_scale(coordinate, origin, spacing, direction):
    return (coordinate - direction*origin)/spacing


def offset_scale(origin, spacing, direction):
    def transform(coordinate):
        arguments = zip(coordinate, origin, spacing, direction)
        return tuple(starmap(_offset_scale, arguments))
    return transform


def markup2point(markup):
    return '%f %f %f # %s %s' % markup


def _fcsv2points(fcsv_filename, transform=None):
    for markup in parse_fcsv(fcsv_filename):
        coordinate = markup[:3]
        if transform:
            coordinate = transform(coordinate)
        yield markup2point(coordinate + markup[3:]) + '\n'


def fcsv2points(volume_filename, fcsv_filenames, output_filename):
    #origin, spacing, direction = coordinates(volume_filename)

    #transform = offset_scale(origin, spacing, direction)

    volume = sitk.ReadImage(volume_filename)
    direction = np.array(volume.GetDirection()).reshape((3, 3))

    def transform(coordinate):
        coordinate = np.matmul(direction, coordinate)
        return volume.TransformPhysicalPointToContinuousIndex(coordinate)

    with open(output_filename, 'w') as output_file:
        for fcsv_filename in fcsv_filenames:
            output_file.writelines(_fcsv2points(fcsv_filename, transform))


if __name__ == '__main__':
    import argparse
    import sys


    parser = argparse.ArgumentParser()
    parser.add_argument('volume')
    parser.add_argument('fiducials', nargs='*')
    parser.add_argument('points')
    parser.add_argument('--output-volume-filename', action='store_true')

    args = parser.parse_args()

    fcsv2points(args.volume, args.fiducials, args.points)
    if args.output_volume_filename:
        print(args.volume, file=sys.stderr)
