# gradcafe_paranoid

# -----------------------------------------------------------------------------

from colorama import init, deinit
from bs4 import BeautifulSoup
from termcolor import colored
import itertools
import threading
import requests
import urllib
import time
import sys

# -----------------------------------------------------------------------------

# Parameters

N = 10
UNIV_LIST = []
BASE_URL = "http://thegradcafe.com/survey/index.php?q="

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

# Query a link
def getResponse(query):
    print(yellow("Fetching details ..."))
    sys.stdout.flush()
    startLoadingAnimation()
    response = requests.get(query)
    stopLoadingAnimation()
    print(green("\nDone."))
    return response.content

# -----------------------------------------------------------------------------

# Main body

params = '|'.join("\"{0}\"".format(item) for item in UNIV_LIST)
query = BASE_URL + urllib.quote_plus("(" + params + ")")
response = getResponse(query);


# -----------------------------------------------------------------------------

# Remove colorama -- For Windows
deinit()
