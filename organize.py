import os
import shutil
from PIL import Image
import webbrowser
from binaryornot.check import is_binary
import re

NAME = os.name

def get_ext(path):
    return (os.path.splitext(path)[1][1:])

def join_path(path1, path2):
    #some extra work to do if the first path is a drive
    pattern = r"^[A-Za-z]+:$"
    if (re.match(pattern,path1) is not None):
        path1+="\\"
    return os.path.join(path1, path2)

def open_file(path):
    extension = get_ext(path)
    if (extension == 'png' or extension == 'jpg'):
        image = Image.open(path)
        image.show()
    elif (extension == 'pdf'):
        webbrowser.open_new(path)
    else:
        # check for binary file
        if (not is_binary(path)):

            if (NAME == 'nt'):
                command_string = "notepad.exe " + path
            
            else:
                command_string = "vim " + path
            
            os.system(command_string)
        
        else:

            print('Unable to open binary file')
    
class directory_db:
    dir_list = []

    def __init__(self):
        pass


    def add_dir(self,item):
        found = False
        if (len(self.dir_list) == 0):
            self.dir_list.append([item,1])
            return 0
        if self.dir_list[0][0] == item:
            self.dir_list[0][1]+=1
            return 1
        for i in range(1,len(self.dir_list)):
            if (self.dir_list[i][0] == item):
                found = True
                target = self.dir_list[i][1]
                if (self.dir_list[i-1][1] > self.dir_list[i][1]):
                    self.dir_list[i][1]+=1
                else:
                    swap_location = -1
                    found_swap = False
                    for j in range(i-1,-1,-1):
                        if self.dir_list[j][1] > target:
                            swap_location = j+1
                            found_swap = True
                            break
                    if (not found_swap):
                        swap_location = 0

                    temp = self.dir_list[swap_location]
                    self.dir_list[swap_location] = self.dir_list[i]
                    self.dir_list[i] = temp
                    self.dir_list[swap_location][1]+=1


        if (not found):
            self.dir_list.append([item,1])
        
        return 2

    def get_directories(self, n):
        ret = []
        for i in range(min(n,len(self.dir_list))):
            ret.append(self.dir_list[i][0])
        
        return ret
    
    def get_length(self):
        return len(self.dir_list)

saved_directories = directory_db()

def clean_directory(path):
    global saved_directories

    os.chdir(path)

    cont = input(f"Cleaning {path}. Continue (y), move the whole directory (m), or skip (s)? ")
    if (cont.lower() != 'y' and cont.lower() != 'm'):
        return 0
    
    if (cont.lower() == 'm'):
        valid = False
        new_directory = input("Enter a new directory\n")
        while (not valid):
            if (os.path.isdir(new_directory) and os.path.isabs(new_directory)):
                saved_directories.add_dir(new_directory)
                valid = True
                shutil.move(path,join_path(new_directory,path))

            else:
                new_directory = input("Not a valid directory. Path must be absolute. Enter a new directory\n")

    subdirectories = []
    #use correct pathnames so that os module is happy
    for obj in os.listdir():
        if (os.path.isdir(join_path(path,obj))):
            subdirectories.append(join_path(path,obj))
        else:
            print(f"\n\nMoving {obj}")

            opened_file = input("Open the file (o), skip (s), or move (anything else)? ")
            if (opened_file.lower() == 'o'):
                open_file(join_path(path,obj))
                opened_file = input("Skip (s) or move (anything else)? ")
            if (opened_file.lower() == 's'):
                continue

            move_to = ""

            n = 8
            # dynamic choice range
            print('')
            dir_list = saved_directories.get_directories(n)
            for i in range(min(len(dir_list),n)):
                print(f"{i+1}. {dir_list[i]}")
            question = ''
            if (len(dir_list) == 0):
                question = 'Enter n for a new directory, or enter d to delete? '
            else:
                question = f"Enter number 1-{min(len(dir_list),n)} for a saved directory, enter n for a new directory, or press d to delete? "
            choice = input(question)
            valid_choice = False
            skip = False
            while (not valid_choice):
                if (choice.isdigit() and int(choice) >= 1 and int(choice) <= min(n,8)):
                    valid_choice = True
                    move_to = saved_directories.get_directories(n)[int(choice)-1]
                    saved_directories.add_dir(move_to)
                elif (choice == 'd'):
                    os.remove(join_path(path,obj))
                    valid_choice = True
                    skip = True
                elif (choice == 'n'):
                    valid = False
                    new_directory = input("Enter a new directory (absolute path)\n")
                    while (not valid):
                        if (os.path.isdir(new_directory) and os.path.isabs(new_directory)):
                            saved_directories.add_dir(new_directory)
                            move_to = new_directory
                            valid = True
                            valid_choice = True

                        else:
                            new_directory = input("Not a valid directory. Path must be absolute. Enter a new directory\n")
                else:
                    choice = input(question)
            if (skip):
                continue
            shutil.move(join_path(path,obj), join_path(move_to,obj))
    
    for dir in subdirectories:
        clean_directory(dir)
    
    return 1

if __name__ == '__main__':
    root = input("Which (absolute) path do you want to clean?\n")
    while (not (os.path.isdir(root) and os.path.isabs(root))):
        root = input("Invalid path. Use an absolute path. Which path do you want to clean?\n")

    clean_directory(root)
                

