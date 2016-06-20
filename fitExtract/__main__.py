from fitExtract import *
import argparse
import os


def main():
    """Main method that implements arguments and options"""
    parser = argparse.ArgumentParser(description='Extra data from .fit files')

    # Arguments and help
    parser.add_argument('-f', '--folder', nargs='*',
                        help='runs fitExtract.py in specified folder paths')
    parser.add_argument('-ls', '--lithiumsymmetric', action='store_true',
                        help='extracts R2 and R3 and assigns to RInt or RElec')
    parser.add_argument('-a', '--additional', nargs='*',
                        help='adds additional parameters to extract')
    parser.add_argument('-c', '--custom', nargs='*',
                        help='extracts custom parameters instead of default')

    # Options
    args = parser.parse_args()

    # Pick one of ls, c, or default
    assert not (args.lithiumsymmetric and args.custom), 'Pick one of -ls or -c'

    # Set params for specified case
    if args.lithiumsymmetric:
        params = ['R2', 'R3']
    elif args.custom:
        params = args.custom
    else:
        params = ['R2']

    # Add more params if -a used
    if args.additional:
        for arg in args.additional:
            params.append(arg)

    # Run in specified folders if -f used, else run in containing folder
    if args.folder:
        for path in args.folder:
            try:
                run(params, args.lithiumsymmetric, correctPath(path))
            except AssertionError:
                print('ERROR: ' + path + ' does not contain any .fit files. Skiping...')
    else:
        try:
            run(params, args.lithiumsymmetric, correctPath(os.getcwd()))
        except AssertionError:
            print('ERROR: current directory does not contain any .fit files. Exiting...')


if __name__ == '__main__':
    main()
