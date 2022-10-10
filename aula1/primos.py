# --------------------------------------------------
# Python script to print prime numbers
# Daniel Sousa Oliveira
# PSR, October 2022.
# --------------------------------------------------

from colorama import *

maximum_number = 50

def isPrime(value):

    for div in range(2,value):
        rem = value % div
        if rem == 0:
            print("Calculated dividers of " + str(value) + " are " +
            str(list(range(2,div+1))))
            return False

    return True
    

def main():

    print("Starting to compute prime numbers up to " + str(maximum_number))

    for i in range(1, maximum_number+1):
        if isPrime(i):
            print(Style.BRIGHT + Fore.RED + 'Number ' + str(i) + ' is prime.' + Style.RESET_ALL)
        else:
            print('Number ' + str(i) + ' is not prime.')

if __name__ == "__main__":
    main()

# count prime numbers smaller than maximum_number that contain number "3"
# python3 primos.py | grep "is prime" | grep "3" | wc -l

# create shebang line
# chmod u+x primos.py
# ls -la primos.py
# ./primos.py
