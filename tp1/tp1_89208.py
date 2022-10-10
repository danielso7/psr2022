# ---------------------------------------------------------
# TP1 - Typing Test
# Daniel Sousa Oliveira nº 89208
# ALexandre Pereira Pinto nº 98401
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

Input = namedtuple('Input', ['requested' , 'received' , 'duration'])

def readyToStart():

    print(Style.BRIGHT + Fore.CYAN + 'PSR 2022 Typing test: ' +  '\nPress any key to start the test' +  Style.RESET_ALL)
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

    new_input = Input(requested, received, duration)              
    test_stats['inputs'].append(new_input)
    test_stats['number_of_types'] += 1

    if received == requested:
        test_stats['number_of_hits'] += 1
        test_stats['type_hit_average_duration'] = (test_stats['type_hit_average_duration']*(test_stats['number_of_hits'] - 1) + duration) / test_stats['number_of_hits']
        print(Style.BRIGHT + Fore.GREEN + 'Correct key' + Style.RESET_ALL)

    else:
        test_stats['type_miss_average_duration'] = (test_stats['type_miss_average_duration']*((test_stats['number_of_types'] - test_stats['number_of_hits'] - 1)) + duration) / (test_stats['number_of_types'] - test_stats['number_of_hits'])
        print(Style.BRIGHT + Fore.RED + 'Incorrect key' + Style.RESET_ALL)
    
    test_stats['type_average_duration'] = ((test_stats['number_of_types']-1)*test_stats['type_average_duration'] + duration) / test_stats['number_of_types']
    test_stats['accuracy'] = test_stats['number_of_hits'] / test_stats['number_of_types']

def inputReceiver(test_stats):
  
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


def timeout_handler(num, stack):
    raise Exception("TIME_OVER")

def modeTimer(max_number, test_stats):
    
    test_stats['test_start'] = ctime()
    signal.signal(signal.SIGALRM, timeout_handler)
    start_test_time = time()
    signal.alarm(max_number)

    try:
        while True:
            if inputReceiver(test_stats):
                break
    except Exception:
        print('Time is up!')
    finally:
        test_stats['test_end'] = ctime()
        test_stats['test_duration']= time()- start_test_time

    return test_stats

def modeInputs(max_number, test_stats):
    
    test_stats['test_start'] = ctime()
    start_test_time = time()

    for i in range(max_number):
        if inputReceiver(test_stats):
            break

    test_stats['test_end'] = ctime()
    test_stats['test_duration'] = time()- start_test_time
    
    return test_stats


def main():

    parser = argparse.ArgumentParser(description='TP1 PSR 2022 - Typing Test')
    parser.add_argument('-utm', '--use_time_mode', action='store_true', help='Max number of secs for time mode or maximum number of inputs for number of inputs mode.')
    parser.add_argument('-mv', '--max_value', type=int, help='Max number of seconds for time mode or maximum number of inputs for number of inputs mode.')
    args = vars(parser.parse_args())

    max_value = args['max_value']    
    if not args['max_value']:
        max_value = 25

    time_mode = args['use_time_mode']    
    if not args['use_time_mode']:
        time_mode = True  

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
            print(Style.BRIGHT + Fore.YELLOW + 'Time mode is active. Test will run up to ' + str(max_value) + ' seconds' + Style.RESET_ALL)
            test_stats = modeTimer(max_value, test_stats)
        else:
            print(Style.BRIGHT + Fore.YELLOW + 'Time mode is inactive. Test will continue until it receives ' + str(max_value) + ' inputs' + Style.RESET_ALL)
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