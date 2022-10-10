# ---------------------------------------------------------
# Python script to handle complex numbers
# Daniel Sousa Oliveira
# PSR, October 2022.
# ---------------------------------------------------------

def addComplex(x,y):
    """
    Addition of two complex numbers
    :param x,y: Two complex numbers passed as tuples
    :returns  : Final result of the operation
    """

    return (x[0]+y[0],x[1]+y[1])

 

def multiplyComplex(x,y):
    """
    Multiplication of two complex numbers
    :param x,y: Two complex numbers passed as tuples
    :returns  : Final result of the operation
    """
    z = complex(x[0],x[1])*complex(y[0],y[1])

    return (int(z.real),int(z.imag))
    

def printComplex(x):
    """
    Prints complex numbers in format (a + bi)
    :param x: Complex number passed as a tuple
    """

    print(str(x[0]) + " + " + str(x[1]) + "i")
    
def main():

    # Define two complex numbers as tuples of size two
    c1 = (5, 3)
    c2 = (-2, 7)

    # Test add
    printComplex(addComplex(c1, c2))

    # Test multiply
    printComplex(multiplyComplex(c1, c2))
 


if __name__ == '__main__':
    main()