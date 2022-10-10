# ---------------------------------------------------------
# Python script to measure execution time
# Daniel Sousa Oliveira
# PSR, October 2022.
# ---------------------------------------------------------

from time import *
import math

def calculateExecutionTime():
    """
    Calculates ellapsed time during cycle execution
    """

    initial_time = time()

    for i in range(0,50000001):
        math.sqrt(i)

    final_time = time()- initial_time
    print("Ellapsed time is " + str(final_time) + " seconds")



def main():
    print("The current date is " + ctime())
    calculateExecutionTime()


if __name__ == '__main__':
    main()