import time
import itertools
import _thread
import os
import sys
from random import randint

path = input("\t\t\t\t\t\tEnter the path.\n\t\t\t\t\t\t")
f = open(path+"\log", "w+")
f.close()

done = False
print("\n\n")

def animate():                                                       #Animation of loading
    for c in itertools.cycle(["|", "/", "--", "\\"]):
        if done:
            break
        sys.stdout.write("\r\t\t\t\t\tMaking a queue " + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.flush()

def countFiles():      
    noOffiles = 0                                 #Will count the no of files present in the folder
    folder = os.listdir(path)
    for files in folder:
        if files.endswith(".mp3"):
            noOffiles += 1
    return noOffiles

def Check(gen_no):                                      #Check if the no is already there
    log = open(path+"\log", "r+")
    while True:
        line = log.readline()
        pos = line.find(",")
        if not line:
            log.close()
            return True
        elif str(gen_no) == line[:pos]:
            log.close()
            return False

def GenerateList():                                         #Generates the playing queue
        while True:
            na = int(countFiles())
            if na == 0:
                input("No mp3 files found\nClosing script now!")
                return False
            count = 0
            while True:                                                                                  
                i = randint(0,na)
                if count == na:
                    return True
                if Check(i):
                    log = open(path+"\log", "a")
                    log.write(str(i)+",\n")
                    log.close()
                    count += 1

def Play():                                                         #Plays song by reading them from the queue
    log = open(path+"\log", "r+")
    while True:
        no = log.readline()
        if not no:
            log.close()
            os.remove(path+"\log")
            input("Done Playing!!")
            return False
            break
        else:
            pos = no.find(",")
            i = 0
            for files in os.listdir(path):
                if files.endswith(".mp3"):
                    if str(i) == no[:pos]:
                        print("\n\t\t\tYou will listen to  "+files)
                        os.startfile(path+"\\"+files)
                        break
                    else:
                        i += 1
        user = input("\n\t\t\tPress any key to play next and exit to exit the script ")
        if user == "exit":
            log.close()
            os.remove(path+"\log")
            return 0

countFiles()
_thread.start_new_thread(animate, ())
if GenerateList() == True:
    done = True
    input("\n\n\t\t\t\t\t    Press any key to start")
    Play()
    print("\t\t\t\t")
    os.system("TASKKILL /F /IM Music.UI.exe")
input("\t\t\tThanks for using the script! Hope you liked it!")