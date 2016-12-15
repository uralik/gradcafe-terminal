# gradcafe-terminal

# -----------------------------------------------------------------------------

from datetime import datetime
from dateutil.parser import parse
from dateutil.relativedelta import *
from tabulate import tabulate
from colorama import init, deinit
from bs4 import BeautifulSoup
from termcolor import colored
import itertools
import threading
import argparse
import requests
import urllib
import time
import sys
import re

# -----------------------------------------------------------------------------

# Parameters

DAYS_TO_FETCH = 10 # Fetch results from the past "N" days
UNIV_LIST = ["University of California San Diego", "UC San Diego", "UCSD"]
BASE_URL = "http://thegradcafe.com/survey/index.php?q="
URL_SUFFIX = "&t=a&o=&pp=250"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) "
                         "AppleWebKit/602.3.12 (KHTML, like Gecko) Version"
                         "/10.0.2 Safari/602.3.12"}

# Truncation lengths (number of characters to display table properly) for:
# (0) Univ. name; (1) Program; (2) Decision, Date; (3) Date Added; (4) Notes;
TRUNCATION_LENGTHS = [30, 40, 35, 11, 35]

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
clearString = " " * 80

def loadingAnimation():
    for currentPrint in itertools.cycle(loadingStrings):
        if not isAnimationRunning:
            sys.stdout.write("\r" + clearString)
            sys.stdout.write("\r")
            sys.stdout.flush()
            break
        
        sys.stdout.write("\r" + currentPrint + yellow(" Fetching details ..."))
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

def header(printStr):
    return colored(printStr, "blue", attrs=["bold"])

def green(printStr):
    return colored(printStr, "green")

def red(printStr):
    return colored(printStr, "red")
    
def yellow(printStr):
    return colored(printStr, "yellow")

# -----------------------------------------------------------------------------

# Command-line argument related code

description = "gradcafe-terminal"
parser = argparse.ArgumentParser(description = description)
parser.add_argument("-d", "--days", type = int,
                    help = "Maximum number of past days (from today) " 
                           "for which to fetch results. " 
                           "The default value is 7 days (1 week). " 
                           "Irrespective of the value chosen, a maximum of 250 "
                           "results can be displayed.")

args = parser.parse_args()
if args.days is not None:
    if args.days >= 1:
        DAYS_TO_FETCH = args.days
    else:
        print(red("Illegal value for number of days."))
        print("Parameter \"--days\" should be a positive integer.")
        sys.exit()

# -----------------------------------------------------------------------------

# Query a link
def getResponse(query):
    sys.stdout.flush()
    startLoadingAnimation()
    response = requests.get(query, headers = HEADERS)
    stopLoadingAnimation()
    return response.content

# -----------------------------------------------------------------------------

# Truncate strings
def truncate(strParam, length):
    if len(strParam) > length:
        return strParam[:length - 4] + " ..."
    else:
        return strParam

# -----------------------------------------------------------------------------

# Main body

params = '|'.join("\"{0}\"".format(item) for item in UNIV_LIST)
query = BASE_URL + urllib.quote_plus("(" + params + ")") + URL_SUFFIX
response = getResponse(query);
soup = BeautifulSoup(response, "html.parser")
dataList = soup.find_all("tr")
tableList = [[tdItem.get_text().encode('ascii', 'ignore')
                                            for tdItem in item.find_all("td")] 
                                                    for item in dataList]

if len(tableList) < 2:
    print(red("No records found.\n"))

else:
    pattern = re.compile('[\W_]+')
    parenPattern = re.compile('\([^)]*\)')
    filteredTableList = [[truncate(pattern.sub(' ', 
                                    parenPattern.sub('', item[0])).strip(), 
                                                        TRUNCATION_LENGTHS[0]), 
                          truncate(pattern.sub(' ', item[1]).strip(), 
                                                        TRUNCATION_LENGTHS[1]), 
                          truncate(pattern.sub(' ', item[2]).strip(), 
                                                        TRUNCATION_LENGTHS[2]), 
                          truncate(pattern.sub(' ', item[4]).strip(), 
                                                        TRUNCATION_LENGTHS[3]), 
                          truncate(pattern.sub(' ', item[5]).strip(), 
                                                        TRUNCATION_LENGTHS[4])] 
                            for item in tableList[1:] 
                                if (datetime.now() + 
                                    relativedelta(days = -1 * DAYS_TO_FETCH) 
                                                            <= parse(item[4]))]
    
    for ii in range(len(filteredTableList)):
        if "accepted" in filteredTableList[ii][2].lower():
            for jj in range(len(filteredTableList[ii])):
                filteredTableList[ii][jj] = green(filteredTableList[ii][jj])
        elif "rejected" in filteredTableList[ii][2].lower():
            for jj in range(len(filteredTableList[ii])):
                filteredTableList[ii][jj] = red(filteredTableList[ii][jj])
            
    
    print(tabulate(filteredTableList, 
                   headers = [header(tableList[0][0]), header(tableList[0][1]), 
                              header(tableList[0][2]), header(tableList[0][4]), 
                              header(tableList[0][5])], 
                   tablefmt="fancy_grid"))

# -----------------------------------------------------------------------------

# Remove colorama -- For Windows
deinit()
