import os
from random import randint
path = input("Enter the path. Please add a \ after the address\n")
f = open(path+"\log", "w+")
f.close()

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
        print("Loading....")
        while True:
            na = int(countFiles())
            if na == 0:
                input("No mp3 files found\nClosing script now!")
                exit
            count = 0
            while True:                                                                                  
                i = randint(0,na)
                if count == na:
                    input("\nDone Loading! Press any key to Start!")
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
                if str(i) == no[:pos]:
                    print("\nYou will listen to  "+files)
                    os.startfile(path+files)
                    break
                if files.endswith(".mp3"):
                    i += 1
        user = input("\nPress any key to play next and exit to exit the script")
        if user == "exit":
            log.close()
            os.remove(path+"\log")
            print("\nPlease Close the music player!\n")
            input("Thanks for using the script! Hope you liked it!")
            sys.exit

countFiles()
GenerateList()
Play()