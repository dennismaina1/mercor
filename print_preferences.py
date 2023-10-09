import time
import sys
from colorama import Fore, Style 

#print in red
def print_red(text,delay=0.05):
    for char in text: 
        sys.stdout.write(Fore.RED + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_green(text,delay=0.05):
    for char in text:
        sys.stdout.write(Fore.GREEN + char + Style.RESET_ALL) 
        sys.stdout.flush() 
        time.sleep(delay)
    print()
