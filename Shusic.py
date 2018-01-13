import time
import _thread
import os
import threading
from random import randint

class MyThread(threading.Thread):
    def __init__(self, pathToScan):
        threading.Thread.__init__(self)
        self.pathToScan = pathToScan
    def run(self):
        scanFiles(self.pathToScan)


done = False
print("\n\n")

masterPath = "E:\\"
dbpath = "C:\\Database\\"  #database path

def havePatience(keyWord):
    print("\t\t\t\tCreating "+keyWord+" ....")
    print("\t\t\t\tThis might take some time depending on your amount of files")

def giveLine(path, lineNO):
    #This reads the given line no from the given file
    file = open(path, "r")
    i = 0  #To keep count of lines
    while True:
        line = file.readline()
        if not line:
            file.close()
            return False
        elif lineNO == i:
            file.close()
            return line
        i += 1

#This is a function to see if the database contains song names or not.
#This should be called after the database has been created.
def checkValid():
    i = 0 #Variable to check it.
    op = open(dbpath+"SongList.db","r")
    while True:
        line = op.readline()
        if not line and i == 0:
            return False
        else:
            return True

def checkDB():
    flag = False
     #Check if Database folder is present
    for file in os.listdir("C:\\"):
        if file == "Database":
            flag = True
            break
    #If the Database Folder is not present,  make one
    if flag == False:
        os.mkdir("C:\\Database")
    #check if db file is present
    for files in os.listdir(dbpath):
        if files == "SongList.db":
            return True
    #Create a file to store songs names from the directory. Name it SongList.db
    mkFile = open(dbpath+"SongList.db","w+")
    mkFile.close()
    return False

def scanFiles(path):
    path += "\\"
    for file in os.listdir(path):
        #print("Checking in "+file)
        if file.endswith(".mp3"):
            #Write the name to db
            db = open(dbpath+"SongList.db", "a+")
            db.write(path+file+"\n")
            db.close()
        elif os.path.isdir(path+file) and file != "System Volume Information":
            thread = MyThread(path+file)
            thread.start()
            thread.join()

"""def animate():                                                       #Animation of loading
    for c in itertools.cycle(["|", "/", "--", "\\"]):
        if done:
            break
        sys.stdout.write("\r\t\t\t\t\tMaking a queue " + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.flush()"""


def countFiles():      
    noOffiles = 0                                 #Will count the no of files present in the file
    openDB = open(dbpath+"SongList.db","r")
    while True:
        line = openDB.readline()
        if not line:
            openDB.close()
            break
        noOffiles += 1
    return noOffiles

def Check(gen_no):                                      #Check if the no is already there
    log = open(dbpath+"log", "r+")
    while True:
        line = log.readline()
        pos = line.find(",")
        if not line:
            log.close()
            return True
        elif str(gen_no) == line[:pos]:
            log.close()
            return False

def GenerateList():
        #_thread.start_new_thread(animate, ())
        count = 0      #Variable to keep track of list range
        #Make the log file that will keep the songs numbers
        log = open(dbpath+"log", "w+")
        log.close()
        #Get the total number of Songs from db
        last = countFiles()
        while count != last:
            i = randint(0, last+1)
            if Check(i):
                openLog = open(dbpath+"log", "a+")
                openLog.write(str(i)+"\n")
                openLog.close()
                count  += 1
        done = True

def Play(song):
    rev = song[::-1]
    pos = rev.find("\\")
    name = rev[:pos]
    Name = name[::-1]
    print("\t\t\t\t  Playing "+Name)
    os.startfile(song[:-1])

def find(playType):                                 #Plays song by reading them from the queue acc to playType
    if playType == "Shuffle":                                                
        log = open(dbpath+"log", "r+")
        while True:
            no = log.readline()
            if not no:
                log.close()
                os.remove(dbpath+"\log")
                input("Done Playing!!")
                return False
                break
            else:
                song = giveLine(dbpath+"SongList.db", int(no))
                Play(song)
                #input("Press any key to play next!")
                user = input("\n\t\t\t\tPress any key to play next and exit to exit the script : ")
                print("\n")
                if user == "exit":
                    log.close()
                    os.remove(dbpath+"\log")
                    return 0
    else:
        i = 1
        while True:
            song = giveLine(dbpath+"SongList.db", i)
            if not song:
                print("Done Playing!\a")
                break
            Play(song)
            i += 1
            user = input("\n\t\t\t\tPress any key to play next and exit to exit the script :")
            print("\n")
            if user == "exit":
                log.close()
                os.remove(path+"\log")
                return 0
                

def main():
    #This will give the menu of the player
    print("\t\t\t\t=============================================================")
    print("\t\t\t\t|                          SHUSIC                           |")
    print("\t\t\t\t|                                               -deepjyoti30|")
    print("\t\t\t\t=============================================================\n\n")
    if checkDB():
        print("\t\t\t\tExisting Database of songs found.")
        prompt = input("\t\t\t\tDo you want to recreate the database? [Y,n]\n\t\t\t\t")
        if prompt == "Y":
            os.remove(dbpath+"SongList.db")
            havePatience("Database")
            scanFiles(masterPath)
    else:
        print("\t\t\t\tSong Database not found.")
        havePatience("Database")
        scanFiles(masterPath)
    if not(checkValid()):
        print("\t\t\t\tWe could not find any songs in your pc.")
        print("\t\t\t\tPlease add some and run Shusic again.")
        return False
    ch = ""
    while ch != "3":
        print("\n\t\t\t\t------------------------------------------------------------")
        print("\t\t\t\t 1. Shuffle")
        print("\t\t\t\t 2. Just Play")
        print("\t\t\t\t 3. Exit")
        print("\t\t\t\t------------------------------------------------------------")
        ch = input("\t\t\t\tEnter Your choice: ")
        print("\n")
        if ch == "1":
            havePatience("Playlist")
            GenerateList()
            input("\t\t\t\tPress Any key to continue!")
            if find("Shuffle") == 0:
                break
        elif ch == "2":
            if find("Play") == 0:
                break

main()
input("\t\t\t\tThanks for using the script! Hope you liked it!")
os.system("TASKKILL /F /IM Music.UI.exe")