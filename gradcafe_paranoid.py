# gradcafe_paranoid

from termcolor import colored
from colorama import init, deinit
import itertools
import threading
import time
import sys

# -----------------------------------------------------------------------------

# Animation related method and globals

isAnimationRunning = False
pauseTime = 0.07 # in seconds
loadingAnimationThread = None
loadingStrings = ["[=         ]", "[ =        ]", "[  =       ]", 
                  "[   =      ]", "[    =     ]", "[     =    ]", 
                  "[      =   ]", "[       =  ]", "[        = ]", 
                  "[         =]", "[        = ]", "[       =  ]", 
                  "[      =   ]", "[     =    ]", "[    =     ]", 
                  "[   =      ]", "[  =       ]", "[ =        ]"]
clearString = "[==========]"

def loadingAnimation():
    for currentPrint in itertools.cycle(loadingStrings):
        if not isAnimationRunning:
            sys.stdout.write("\r" + clearString)
            sys.stdout.flush()
            break
        
        sys.stdout.write("\r" + currentPrint)
        sys.stdout.flush()
        time.sleep(pauseTime)

def startLoadingAnimation():
    global isAnimationRunning, loadingAnimationThread
    isAnimationRunning = True
    loadingAnimationThread = threading.Thread(target = loadingAnimation)
    loadingAnimationThread.start()
    
def stopLoadingAnimation():
    global isAnimationRunning, loadingAnimationThread
    isAnimationRunning = False
    loadingAnimationThread.join()

# -----------------------------------------------------------------------------

# Initialize colorama -- For Windows
init()

# Methods for colors

def white(printStr):
    return colored(printStr, "white")

def green(printStr):
    return colored(printStr, "green")

def red(printStr):
    return colored(printStr, "red")
    
def yellow(printStr):
    return colored(printStr, "yellow")

# -----------------------------------------------------------------------------

# Main body

print(yellow("Fetching details ..."))
sys.stdout.flush()
startLoadingAnimation()



stopLoadingAnimation()
print(green("\nDone."))

# -----------------------------------------------------------------------------

# Remove colorama -- For Windows
deinit()
