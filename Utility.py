import time
import psutil
from pandas import read_csv


t0 = 0

def start_time():
    global t0
    t0 = time.process_time()


def stop_time(returnTime=False):
    global t0
    if not returnTime:
        print("The process took: " , time.process_time() - t0 ,"seconds")
    else: return str(time.process_time() - t0)

def printRamUsage():
    print("Occupazione attuale ram: ", psutil.virtual_memory().percent)
    print("Ram libera: ", str(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total))

def loadData():
    print("##### Loading data #####")
    start_time()
    data = read_csv("imdb-actors-actresses-movies.tsv", delimiter="\t", header=None)
    stop_time()
    print("#########################")
    return data