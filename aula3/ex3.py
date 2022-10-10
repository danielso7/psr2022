# ---------------------------------------------------------
# Python script to handle complex numbers
# Daniel Sousa Oliveira
# PSR, October 2022.
# ---------------------------------------------------------

from collections import namedtuple

# Define Namedtuple to make complex numbers explicit
Complex = namedtuple('Complex', ['r', 'i'])


def addComplex(x,y):
    """
    Addition of two complex numbers
    :param x,y: Two complex numbers passed as tuples
    :returns  : Final result of the operation
    """

    return (x.r+y.r, x.i+y.i)

 

def multiplyComplex(x,y):
    """
    Multiplication of two complex numbers
    :param x,y: Two complex numbers passed as tuples
    :returns  : Final result of the operation
    """
    z = complex(x.r,x.i)*complex(y.r,y.i)

    return (int(z.real),int(z.imag))
    

def printComplex(x):
    """
    Prints complex numbers in format (a + bi)
    :param x: Complex number passed as a tuple
    """

    print(str(x[0]) + " + " + str(x[1]) + "i")
    
def main():

    # Define two complex numbers as tuples of size two
    c1 = Complex(5, 3)      # use order when not naming
    c2 = Complex(i=7, r=-2) # if items are names order is not relevant
    print('c1 = ' + str(c1)) # named tuple looks nice when printed

    # Test add
    printComplex(addComplex(c1, c2))

    # Test multiply
    printComplex(multiplyComplex(c1, c2))
 


if __name__ == '__main__':
    main()