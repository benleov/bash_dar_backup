#!/usr/bin/python
import os

import io
import string

#######################Python Backup Script#########################################
##
##This script allows you to backup selective directories using dar. 
##It has a couple of handy features:

##
##1) It will ignore any directory containing a file called ".nobackup".(configurable) 
##2) Any directories put into the ignore list will be ignored recursively.
##3) It will write these to DVD / CD, and prompt to enter next disk.
##4) It dar files once burnt to disk.
##
##Source: http://programminglinuxblog.blogspot.com/ 
##License: GPLv3. See http://www.gnu.org/licenses/gpl.html 
####################################################################################

# All directories off ROOT_PATH are by included by default unless they are put in the
# exclude or ignore lists.

# IGNORE_FILENAME if a file with this file name is found dar will not backup anything 
# in the directory its contained in. It is NOT recursive, thus subdirectories will be 
# considered for backup.

IGNORE_FILENAME=".nobackup"

# Saves the executed dar command in this file:

COMMAND_FILE = "command"

# Saves the output of the dar command in this file

COMMAND_OUTPUT = "output";

# BACK_SAVE_LOC is where the dar file will be saved. WARNING: this directory should 
# be an ignored directory or in a sub directory of one of these directories.

BACK_SAVE_LOC="/root/backups/"

# the name of the dar file(s) that will be created

BACKUP_FILENAME="full"

# The root directory to backup from

ROOT_PATH = "/"

# exclude is a list of directories to exclude from backup. 
# WARNING: these directories must be RELATIVE to ROOT_PATH.

exclude = []

# NOTE: all subdirectories of these directories are ignored (i.e a recursive ignore)

# Example Ignore:
# ignore = ["bin", "dev","initrd","lib","media","proc","tmp", "vmlinuz","boot","etc", 
#            "mnt","root","srv","cdrom","lost+found","opt","sbin","sys","var"]

ignore.append(BACK_SAVE_LOC)      # ( WARNING: dont modify )

stack = []   # stack for directories to include   ( WARNING: dont modify )

# recursive method that sets up stack and exclude lists with the appropriate directories.
def get_backup_directories(rootDir):

    for name in os.listdir(rootDir):
        path = os.path.join(rootDir, name)

        if os.path.isdir(path):  # if current file is a dir

            ignoreDir = False

            for ig in ignore:  # check if its in ignore list
                if path.startswith(ROOT_PATH + ig):

                    ignoreDir = True
                    break

            if not ignoreDir:

                stack.append(path)
                get_backup_directories(path)
            else:

               exclude.append(path)
 else:
     shortpath = os.path.basename(path)

  
     if shortpath == IGNORE_FILENAME: # remove directory if ignore file present
                stack.pop()

                
  exclude.append(path.replace(IGNORE_FILENAME,"")) # remove filename 
    

get_backup_directories(ROOT_PATH)

# explicitly included directories also includes sub-directories; this removes any sub-directories
# of already included directories

print "normalising include stack"

i = len(stack)

while i != 0:
    i = i - 1

    
    x = len(stack)
    while x != 0:

        x = x - 1
        if stack[i].startswith(stack[x]) and not stack[i] == stack[x]:

            del stack[i]
            break

for i in stack: 
    print "normalised: " + i

print "making exclude paths relative"

i = len(exclude)

while i != 0:
    i = i - 1

    curr = exclude[i]
    curr = curr.replace(ROOT_PATH,"",1)

    curr = curr.replace(" ","\ ")       # delimit space characters
    exclude[i] = curr

# same for include paths

print "making include paths relative"

i = len(stack)

while i != 0:
    i = i - 1

    curr = stack[i]    
    curr = curr.replace(ROOT_PATH,"",1) 
    curr = curr.replace(" ","\ ")  # delmit space characters

    stack[i] = curr

# NOTE: -v verbose,-c filename, -s size, -z gzip  compression, set root folder, ignore All files
baseCmd = "dar -v -c "+ BACK_SAVE_LOC + BACKUP_FILENAME + " -s 4000M -z -R " + ROOT_PATH +" -P . "

# include directories
for i in stack:
    baseCmd += "-g " + i + " "

# exclude directories
for i in exclude:
   baseCmd += "-P " + i + " " 


print "executing command: " + baseCmd

os.system("echo "  + baseCmd + " > " + COMMAND_FILE) # save to file

output = os.system(baseCmd + " > " + COMMAND_OUTPUT)    # also save to file

# write each file to cd

files = os.listdir(".")

# remove all non-dar files

i = len(files)
while i != 0:

        i = i - 1
        if not files[i].endswith(".dar"):

                del files[i]
 
print "you will need " + str(len(files)) + " disks. Starting burning process..."

for curr in files:
 x = raw_input('Please insert a CD/DVD. Press any key to continue.')

 output = os.system("growisofs -Z /dev/dvd -R -J " + BACK_SAVE_LOC + curr) 
 os.system("eject")

# cleanup

os.system("rm *.dar")


