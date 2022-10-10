# --------------------------------------------------
# Python script to calculate perfect numbers
# Daniel Sousa Oliveira
# PSR, October 2022.
# --------------------------------------------------

maximum_number = 100  # maximum number to test.


def getDividers(value):
    """
    Return a list of dividers for the number value
    :param value: the number to test
    :return divider_list: a list of dividers.
    """
    divider_list = [1]

    for div in range(2,value):
        rem = value % div
        if rem == 0:
            divider_list.append(div)

    return divider_list


def isPerfect(value):
    """
    Checks whether the number value is perfect.
    :param value: the number to test.
    :return: True or False
    """
    dividers = getDividers(value)
    if sum(dividers) == value:
        return True
    return False


def main():
    print("Starting to compute perfect numbers up to " + str(maximum_number))

    for i in range(1, maximum_number+1):
        if isPerfect(i):
            print('Number ' + str(i) + ' is perfect.')


if __name__ == "__main__":
    main()