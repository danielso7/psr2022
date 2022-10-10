# --------------------------------------------------
# Python script to calculate perfect numbers
# Daniel Sousa Oliveira
# PSR, October 2022.
# --------------------------------------------------

maximum_number = 100

def isPerfect(value):
    
    divider_list = [1]

    for div in range(2,value):
        rem = value % div
        if rem == 0:
            divider_list.append(div)

    if sum(divider_list) == value:
        return True
            
    return False

def main():
    print("Starting to compute perfect numbers up to " + str(maximum_number))

    for i in range(1, maximum_number+1):
        if isPerfect(i):
            print('Number ' + str(i) + ' is perfect.')


if __name__ == "__main__":
    main()