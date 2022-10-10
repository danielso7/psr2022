# ---------------------------------------------------------
# Python script to print print and read chars from keyboard
# Daniel Sousa Oliveira
# PSR, October 2022.
# ---------------------------------------------------------

from curses.ascii import *
import readchar

def printAllCharsUpTo(stop_char):
    """
    Prints all chars up to one given char
    :param stop_char: the final char to print
    """

    chars = []
    for number in range(32,ord(stop_char)):
        chars.append(chr(number))

    print("Characters up to '" + stop_char + "' : " + str(", ".join(chars)))

def readAllUpTo(stop_char):
    """
    Reads all characters inserted in the keyboard
    :param stop_char: Program interruption key
    """
    
    while True:

        key = readchar.readkey()

        if key == stop_char:
            break

        print("Key pressed : " + key)


def main():
    key = readchar.readkey()
    printAllCharsUpTo(key)
    readAllUpTo('X')

    

if __name__ == '__main__':
    main()