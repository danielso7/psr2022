# ---------------------------------------------------------
# TP1 - Typing Test
# Daniel Sousa Oliveira nº 89208
# PSR, October 2022.
# ---------------------------------------------------------

from colorama import *
from time import *
from pprint import *
from collections import *
import argparse
import readchar
import random
import string
import signal


"""Define namedtuple that contains requested key, received key and the time passed between the two"""
Input = namedtuple('Input', ['requested' , 'received' , 'duration'])

def readyToStart():
    """Function that requests any key to be pressed by the user in order to start the test.
    If the space bar is pressed, the test stops.
    """

    print(Style.BRIGHT + Fore.CYAN + 'PSR 2022 Typing test: ' +  
    '\nPress any key to start the test' +  Style.RESET_ALL)

    key = readchar.readkey()

    if key == " ":     
        print(Style.BRIGHT + Fore.RED + '\nTest was stopped' + Style.RESET_ALL)                 
        sleep(1)                                                                                
        return False
    else:
        print(Style.BRIGHT + Fore.GREEN +'Test was started' + Style.RESET_ALL)
        sleep(1)
        return True

def updateStats(test_stats, requested, received, duration):
    """Updates test statistics while the test is running

    Appends new input, adds one to the number of types (inputs), and in case of matching keys, adds one to the
    number of hits. Also, it calculates the new average duration, the average duration when the key is correct (hit)
    and the average duration when the key is incorrect (miss). Accuracy is also calculated at the end.

    Parameters
    ----------
    test_stats : dict
        Dictionary containing test statistics
    requested : str
        Random key requested to the user
    received : str
        Actual key pressed by the user
    duration : float
        Ellapsed time between the requested key by the program and the key pressed by the user
    """

    new_input = Input(requested, received, duration)              
    test_stats['inputs'].append(new_input)
    test_stats['number_of_types'] += 1

    if received == requested:
        test_stats['number_of_hits'] += 1
        test_stats['type_hit_average_duration'] = (test_stats['type_hit_average_duration']
        *(test_stats['number_of_hits'] - 1) + duration) / test_stats['number_of_hits']

        print(Style.BRIGHT + Fore.GREEN + 'Correct key' + Style.RESET_ALL)

    else:
        test_stats['type_miss_average_duration'] = (test_stats['type_miss_average_duration']
        *((test_stats['number_of_types'] - test_stats['number_of_hits'] - 1)) 
        + duration) / (test_stats['number_of_types'] - test_stats['number_of_hits'])
        
        print(Style.BRIGHT + Fore.RED + 'Incorrect key' + Style.RESET_ALL)
    
    test_stats['type_average_duration'] = ((test_stats['number_of_types']-1)*test_stats['type_average_duration']
    + duration) / test_stats['number_of_types']

    test_stats['accuracy'] = test_stats['number_of_hits'] / test_stats['number_of_types']

def inputReceiver(test_stats):
    """Function to handle reading keys when pressed by the user

    If the space bar is pressed the test is stopped. Function generates one key, waits for user input and calculates
    the ellapsed time between the two. Calls statistics update function at the end.

    Parameters
    ----------
    test_stats : dict
        Dictionary containing test statistics

    Returns
    -------
    bool
        True flag is used to stop the program when space bar is pressed
    """
  
    random_key = random.choice(string.ascii_lowercase)        
    
    initial_time = time()                      
    print(Style.BRIGHT + Fore.YELLOW + "Press '" + random_key + "' key" + Style.RESET_ALL)
    
    key = readchar.readkey()
    if key==' ':
        print(Style.BRIGHT + Fore.RED + 'Test was stopped' + Style.RESET_ALL)
        return True
    
    final_time = time()
    duration = final_time - initial_time
    updateStats(test_stats, random_key, key, duration)

    return False


def timeout_handler(num,frame):
    """Timeout exception handler

    Raises
    ------
    Exception
        Exception generated when the time of the test is over
    """
    raise Exception("TIME_OVER")

def modeTimer(max_number, test_stats):
    """Run the test on timer mode

    Use signal package to create an alarm clock which will raise time out expection when the maximum time is reached.
    Meanwhile calls input handler in loop until the end of the test. Updates test stats at the end.

    Parameters
    ----------
    max_number : int
        Maximum number of seconds of the test
    test_stats : dict
        Dictionary containing test statistics

    Returns
    -------
    test_stats : dict
        Dictionary containing test statistics
    """
    
    test_stats['test_start'] = ctime()
    signal.signal(signal.SIGALRM, timeout_handler)
    start_test_time = time()
    signal.alarm(max_number)

    try:
        while True:
            if inputReceiver(test_stats):
                break
    except Exception:
        print(Style.BRIGHT + Fore.RED + 'Times is up !' + Style.RESET_ALL)
    finally:
        test_stats['test_end'] = ctime()
        test_stats['test_duration'] = time()- start_test_time

    return test_stats

def modeInputs(max_number, test_stats):
    """Run the test on the Inputs mode

    Calls input handler in loop until the maximum number of inputs is reached. Updates test stats at the end.

    Parameters
    ----------
    max_number : int
        Maximum number of inputs that the program will accept during the test
    test_stats : dict
        Dictionary containing test statistics

    Returns
    -------
    test_stats : dict
        Dictionary containing test statistics
    """
    
    test_stats['test_start'] = ctime()
    start_test_time = time()

    for i in range(max_number):
        if inputReceiver(test_stats):
            break

    test_stats['test_end'] = ctime()
    test_stats['test_duration'] = time()- start_test_time
    
    return test_stats


def main():
    """Main function

    Initializes argument parser to handle two types of usage. If there are arguments passed the usage is the following:
    usage: main.py [-h] [-utm] [-mv MAX_VALUE]
    If no arguments are provided, the program will still run with default values.
    Also initializes test statistics dictionary.
    Handles the starting mode of the test and prints the resultant statistics of the test.

    """

    parser = argparse.ArgumentParser(description='TP1 PSR 2022 - Typing Test')
    parser.add_argument('-utm', '--use_time_mode', action='store_true', 
    help='Max number of secs for time mode or maximum number of inputs for number of inputs mode.')
    parser.add_argument('-mv', '--max_value', type=int, 
    help='Max number of seconds for time mode or maximum number of inputs for number of inputs mode.')
    args = vars(parser.parse_args())

    max_value = args['max_value']    
    if not args['max_value']:
        max_value = 25

    time_mode = args['use_time_mode']    
    if not args['use_time_mode']:
        time_mode = False  

    test_stats = {

        'inputs':[],
        'number_of_hits':0,
        'number_of_types':0,
        'test_duration': 0,
        'test_end': '',
        'test_start': '',
        'type_average_duration': 0,
        'type_hit_average_duration': 0,
        'type_miss_average_duration': 0
    }

    if readyToStart():

        print(Style.BRIGHT + Fore.GREEN + 'Typing Test was Started !' + Style.RESET_ALL)

        if time_mode:
            print(Style.BRIGHT + Fore.YELLOW + 'Time mode is active. Test will run up to ' 
            + str(max_value) + ' seconds' + Style.RESET_ALL)

            test_stats = modeTimer(max_value, test_stats)
        else:
            print(Style.BRIGHT + Fore.YELLOW + 'Time mode is inactive. Test will continue until it receives ' 
            + str(max_value) + ' inputs' + Style.RESET_ALL)

            test_stats = modeInputs(max_value, test_stats)

        print(Style.BRIGHT + Fore.YELLOW + "End of typing test !" + Style.RESET_ALL)
        print(Style.BRIGHT + Fore.CYAN + 'Final statistics of the test:' + Style.RESET_ALL)    
        
        exclude_keys = ['inputs']
        final_stats = {k: test_stats[k] for k in set(list(test_stats.keys())) - set(exclude_keys)}
        pprint(final_stats)

    else:

        print(Style.BRIGHT + Fore.RED + 'Test was stopped' + Style.RESET_ALL)
    

if __name__ == "__main__":
    main()