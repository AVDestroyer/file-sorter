import os
import shutil
from PIL import Image
import webbrowser

def openF(path):
    if (path[-4:] == '.png' or path[-4:] == '.jpg'):
        image = Image.open(path)
        image.show()
    elif (path[-4:] == '.pdf'):
        webbrowser.open_new(path)
    else:
        osCommandStirng = "notepad.exe " + path
        os.system(osCommandStirng)
    

class directoryDB:
    dirlist = []

    def __init__(self):
        pass


    def addDir(self,item):
        found = False
        if (len(self.dirlist) == 0):
            self.dirlist.append([item,1])
            #print(self.dirlist)
            return 0
        if self.dirlist[0][0] == item:
            self.dirlist[0][1]+=1
            #print(self.dirlist)
            return 1
        for i in range(1,len(self.dirlist)):
            if (self.dirlist[i][0] == item):
                found = True
                target = self.dirlist[i][1]
                if (self.dirlist[i-1][1] > self.dirlist[i][1]):
                    self.dirlist[i][1]+=1
                else:
                    swapLocation = -1
                    foundSwap = False
                    for j in range(i-1,-1,-1):
                        if self.dirlist[j][1] > target:
                            swapLocation = j+1
                            foundSwap = True
                            break
                    if (not foundSwap):
                        swapLocation = 0

                    temp = self.dirlist[swapLocation]
                    self.dirlist[swapLocation] = self.dirlist[i]
                    self.dirlist[i] = temp
                    self.dirlist[swapLocation][1]+=1


        if (not found):
            self.dirlist.append([item,1])
        

        #print(self.dirlist)

        return 2

    
    def getDirectories(self, n):
        ret = []
        for i in range(min(n,len(self.dirlist))):
            ret.append(self.dirlist[i][0])
        
        return ret
    
    def getLength(self):
        return len(self.dirlist)

savedDirectories = directoryDB()

def cleanDirectory(path):
    global savedDirectories

    os.chdir(path)
    if (path[-1] != '/'):
        path+='/'
    cont = input(f"Cleaning {path}. Continue (y), move the whole directory (m), or skip (s)? ")
    if (cont.lower() != 'y' and cont.lower() != 'm'):
        return 0
    
    if (cont.lower() == 'm'):
        valid = False
        newDirectory = input("Enter a new directory\n")
        while (not valid):
            if (os.path.isdir(newDirectory) and os.path.isabs(newDirectory)):
                if newDirectory[-1] != '/':
                    newDirectory += '/'
                savedDirectories.addDir(newDirectory)
                valid = True
                shutil.move(path,newDirectory + path)

            else:
                newDirectory = input("Not a valid directory. Path must be absolute. Enter a new directory\n")

    subdirectories = []
    #use correct pathnames so that os module is happy
    for obj in os.listdir():
        if (os.path.isdir(path + obj + '/')):
            subdirectories.append(path + obj + '/')
        else:
            print(f"\n\nMoving {obj}")

            openFile = input("Open the file (o), skip (s), or move (anything else)? ")
            if (openFile.lower() == 'o'):
                openF(path + obj)
                openFile = input("Skip (s) or move (anything else)? ")
            if (openFile.lower() == 's'):
                continue

            moveTo = ""

            n = 8
            # dynamic choice range
            print('')
            dirList = savedDirectories.getDirectories(n)
            for i in range(min(len(dirList),n)):
                print(f"{i+1}. {dirList[i]}")
            question = ''
            if (len(dirList) == 0):
                question = 'Enter n for a new directory, or enter d to delete '
            else:
                question = f"Enter number 1-{min(len(dirList),n)} for a saved directory, enter n for a new directory, or press d to delete "
            choice = input(question)
            validChoice = False
            skip = False
            while (not validChoice):
                if (choice.isdigit() and int(choice) >= 1 and int(choice) <= min(n,8)):
                    validChoice = True
                    moveTo = savedDirectories.getDirectories(n)[int(choice)-1]
                    savedDirectories.addDir(moveTo)
                elif (choice == 'd'):
                    os.remove(path + obj)
                    validChoice = True
                    skip = True
                elif (choice == 'n'):
                    valid = False
                    newDirectory = input("Enter a new directory\n")
                    while (not valid):
                        if (os.path.isdir(newDirectory) and os.path.isabs(newDirectory)):
                            if newDirectory[-1] != '/':
                                newDirectory += '/'
                            savedDirectories.addDir(newDirectory)
                            moveTo = newDirectory
                            valid = True
                            validChoice = True

                        else:
                            newDirectory = input("Not a valid directory. Path must be absolute. Enter a new directory\n")
                else:
                    choice = input(question)
            if (skip):
                continue
            shutil.move(path + obj, moveTo + obj)
    
    for dir in subdirectories:
        cleanDirectory(dir)
    
    return 1

#if __name__ == 'test':
root = input("Which path do you want to clean?\n")
while (not (os.path.isdir(root) and os.path.isabs(root))):
    root = input("Invalid path. Use an absolute path. Which path do you want to clean?\n")
if (root[-1] != '/'):
    root += '/'
cleanDirectory(root)
                

