from curses.ascii import *
import readchar

def countNumbersUpTo(stop_char):
    """
    Counts all keys inserted and divides them into numbers or others
    :param stop_char: Program interruption key
    """

    total_numbers = 0
    total_others = 0
    inputs = []

    while True:
        key = readchar.readkey()
        print("Key pressed : " + key)

        if key == stop_char:
            break

        inputs.append(key)

    total_numbers = [input for input in inputs if input.isnumeric()]
    total_others = [input for input in inputs if not input.isnumeric()]
    total_numbers.sort()

    print('You entered ' + str(len(total_numbers)) + ' numbers.')
    print('You entered ' + str(total_numbers))

    print('You entered ' + str(len(total_others)) + ' others.')
    print('You entered ' + str(total_others))

    others_dict = {}
    counter = 0
    for input in inputs:
        if not input.isnumeric():
            others_dict[counter] = input
        counter += 1

    print('Other Inputs Dictionary ' + str(others_dict))


def main():
    countNumbersUpTo('X')
    

if __name__ == '__main__':
    main()