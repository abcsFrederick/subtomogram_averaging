#!/usr/bin/env python


def add_arguments(parser, filename):
    with open(filename) as template:
        lines = template.readlines()

    help_ = []
    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.startswith('#'):
            help_.append(line[1:].strip())
            continue

        argument, default = [value.strip() for value in line.split('=')]
        parser.add_argument('--' + argument, default=default, help='\n'.join(help_))
        help_ = []

    return parser


def output_arguments(args):
    for key, value in vars(args).items():
        if key == 'template':
            continue
        print('%s = %s' % (key, value))


if __name__ == '__main__':
    import argparse
    import sys


    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-t', '--template', required=True)
    args, argv = parser.parse_known_args()
    if not args.template:
        parser.print_usage()
        sys.exit(2)

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-t', '--template')
    parser.add_argument('--output-unused-arguments', action='store_true')
    parser = add_arguments(parser, args.template)
    args, argv = parser.parse_known_args()
    if args.output_unused_arguments:
        print(' '.join(argv), file=sys.stderr)

    del args.template
    del args.output_unused_arguments

    output_arguments(args)
