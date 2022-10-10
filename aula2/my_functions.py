# --------------------------------------------------
# Python script to print prime numbers
# Daniel Sousa Oliveira
# PSR, October 2022.
# --------------------------------------------------
import math

def isPrime(value):
    """
    Checks whether the number value is prime.
    :param value: the number to test.
    :return: True or False
    """

    for div in range(2,(int)(math.sqrt(value))+1):
        rem = value % div
        if rem == 0:
            print("Calculated dividers of " + str(value) + " are " +
            str(list(range(2,div+1))))
            return False

    return True