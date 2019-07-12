#!/usr/bin/env python
import argparse

import SimpleITK as sitk


parser = argparse.ArgumentParser()
parser.add_argument('input')
parser.add_argument('output')
args = parser.parse_args()

sitk.WriteImage(sitk.ReadImage(args.input), args.output)
