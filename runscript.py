#!/usr/bin/env python
import subprocess
import os

EXCLUDE = []

def main():

    # get the path of the folder to iterate and find the name of the file
    dirPath = os.path.join(os.getcwd(), "test")

    # iterate over the files in the path
    for filename in os.listdir(dirPath):
        
        # get the filenames that has the extension of the .asm
        if (".asm" in filename) and (filename not in EXCLUDE):
            argument = "./test/" + filename
            command = ["./main.py", argument]
            subprocess.run(command)

if __name__ == "__main__":
    main()