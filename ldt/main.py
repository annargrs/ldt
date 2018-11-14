"""Welcome to ldt.

This is the entry point of the ldt application.
"""

import argparse


def _experiment(args):
    pass


def main():
    """Launch the ldt application."""
    parser = argparse.ArgumentParser(prog='ldt')
    subparsers = parser.add_subparsers()
    parser_xp = subparsers.add_parser(
        'experiment', formatter_class=argparse.RawTextHelpFormatter,
        help='Run experiments according to the setup specified in the input '
             'YAML config file')
    parser_xp.set_defaults(func=_experiment)
    parser_xp.add_argument('--with',
                           help='A YAML config file to specify the '
                                'experimental setup')
    args = parser.parse_args()
    args.func(args)
