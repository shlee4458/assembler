#!/usr/bin/env python
from assemblyParser import *
from assemblyCode import *
import argparse

DEBUG_MODE = False

def main():

    # parse filename as an argument
    argParser = argparse.ArgumentParser(description = "Process a file")
    argParser.add_argument('filename', type=str, help="Path to the file")
    args = argParser.parse_args()
    filename = args.filename

    # Load the file to the assembly parser
    parser = AssemblyParser(filename)

    with open('Prog.hack', "w") as output:
        line = 1
        
        # loop over each line of the file and write to the file the binary representation
        while parser.hasMoreCommands():
            # read the next line
            parser.advance()

            # print the current line and command
            print(f"current line: {line}, current command: {parser.getCommand()}")

            # if the current line is empty, continue
            type = parser.commandType()
            if not type:
                continue
        
            # write based on the type
            if type == "C_COMMAND":
                print("C was called")
                dest, comp, jump = parser.dest(), parser.comp(), parser.jump()
                a = "1" if ";" in parser.getCommand() else "0"
                res = "111" + a + compBin(comp) + destBin(dest) + jumpBin(jump) + "\n"
                if DEBUG_MODE:
                    print(compBin(comp))
                    print(destBin(dest))
                    print(jumpBin(jump))
                print(f"C_COMMAND was written: {res}")
                output.write(res)
            
            elif type == "A_COMMAND" or type == "L_COMMAND":
                symbol = parser.symbol()
                # TODO: translate symbol to decimal
                res = (("0" * 16) + bin(int(symbol))[2:])[-16:] + "\n"
                print(f"A_COMMAND/L_COMMAND was written: {res}")
                output.write(res)
            line += 1

if __name__ == "__main__":
    main()