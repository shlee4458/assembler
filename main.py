#!/usr/bin/env python
from AssemblyParser import *
from AssemblyCode import *
from SymbolTable import *
import argparse
import os

DEBUG_MODE = False

def main():

    # parse filename as an argument
    argParser = argparse.ArgumentParser(description = "Process a file")
    argParser.add_argument('filename', type=str, help="Path to the file")
    args = argParser.parse_args()
    filename = args.filename

    # initiate symbol table
    symbolTable = SymbolTable()    

    # First Pass
    # In the first passing, keep the record of the ROM address in the symbol table
    # each time a pseudocommand is encountered. increment the address record by 1 
    # whenever a C_instruction or A_instruction is encountered.

    # Load the file to the AssymblyParser
    parser = AssemblyParser(filename)
    address = 0

    while parser.hasMoreCommands():
        parser.advance()

        type = parser.commandType()

        # if it is comment or an empty line
        if not type:
            continue
        
        # if it is a_command or c_command increase the line
        if type == "A_COMMAND" or type == "C_COMMAND":
            address += 1
            continue
            
        # if it is L command, store it to the symbol table
        symbol = parser.symbol()
        symbolTable.addEntry(symbol, address)

    # Second Pass
    # When A instruction is encountered, where @xxx is not a number but a symbol,
    # find in the symbolMap the number representation of the symbol
    # if not store the variable in the symbolmap where n is the next available RAM address
    parser = AssemblyParser(filename)
    destFileName = filename.split('/')[-1].split('.')[0]
    destFileName = destFileName + ".hack"
    destPath = os.path.join(os.getcwd(), "test", destFileName)
    symbolTable.setNextAddress()

    with open(destPath, "w") as output:
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
                res = "111" + compBin(comp) + destBin(dest) + jumpBin(jump) + "\n"
                if DEBUG_MODE:
                    print(compBin(comp))
                    print(destBin(dest))
                    print(jumpBin(jump))
                print(f"C_COMMAND was written: {res}")
                output.write(res)
            
            elif type == "A_COMMAND":
                symbol = parser.symbol()
                # add to the table if the symbol is not an int or not in the symbol table
                if not symbol.isnumeric() and not symbolTable.contains(symbol):
                    symbolTable.addEntry(symbol, symbolTable.getNextAddress())

                if symbolTable.contains(symbol):
                    symbol = symbolTable.GetAddress(symbol)

                res = (("0" * 16) + bin(int(symbol))[2:])[-16:] + "\n"
                print(f"A_COMMAND/L_COMMAND was written: {res}")
                output.write(res)
            line += 1



if __name__ == "__main__":
    main()