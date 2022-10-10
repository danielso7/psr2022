# --------------------------------------------------
# Python script to print prime numbers
# Daniel Sousa Oliveira
# PSR, October 2022.
# --------------------------------------------------

from colorama import *
from my_functions import *
import argparse

parser = argparse.ArgumentParser()          
parser.add_argument('--maximum_number', type=int, required=False,
                    help='The maximum number until which we check if numbers are prime')
args = vars(parser.parse_args())

maximum_number = args['maximum_number']     # maximum number to test.
if not args['maximum_number']:
    maximum_number = 100                    # define default value

def main():

    print("Starting to compute prime numbers up to " + str(maximum_number))

    for i in range(0, maximum_number+1):
        if isPrime(i):
            print(Style.BRIGHT + Fore.RED + 'Number ' + str(i) + ' is prime.' + Style.RESET_ALL)
        else:
            print('Number ' + str(i) + ' is not prime.')

if __name__ == "__main__":
    main()