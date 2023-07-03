"""
Assembly Parser is a class that reads an assembly language command, parses it, 
and provides convenient access to the command’s components (fields and symbols)
"""

class AssemblyParser:
    
    def __init__(self, filename):
        '''
        Opens the input file/stream and gets ready to parse it
        '''
        self.file = open(filename)
        self.prevPosition = self.file.tell()
        self.currPosition = -1

    def hasMoreCommands(self):
        '''
        Check if there are more commands in the input.
        return bool
        '''
        res = self.prevPosition != self.currPosition
        # TODO: decide whether to close the file once the end of the file is reached
        if not res:
            self.file.close()
        return res
    
    def advance(self):
        '''
        Reads the next command from the input and makes it the current
        command. Should be called only if hasMoreCommands() is true.
        Initially there is no current command.
        '''
        if self.hasMoreCommands():
            line = self.file.readline()
            # assign curr command position to the previous position
            if self.currPosition != -1:
                self.prevPosition = self.currPosition

            # assign the new command position to the current position
            self.currPosition = self.file.tell()
            
            # update the currentCommand
            self.currentCommand = line.strip()

    def commandType(self) -> str:
        '''
        Returns the type of the current command:
        A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        C_COMMAND for dest=comp;jump
        L_COMMAND for (Xxx) where Xxx is a symbol.
        '''

        firstChar = ""
        if self.currentCommand:
            firstChar = self.currentCommand[0]

        # current line is either comment or an empty line
        if not firstChar or firstChar == "/":
            return ""
        
        if firstChar == "@":
            return "A_COMMAND"
        elif firstChar == "(":
            return "L_COMMAND"
        else:
            return "C_COMMAND"

    def symbol(self) -> str:
        '''
        Returns the symbol or decimal Xxx of the current command
        @Xxx or (Xxx). Should be called only when commandType() is
        A_COMMAND or L_COMMAND.
        '''
        if self.commandType() == "A_COMMAND":
            return self.currentCommand[1:]

        elif self.commandType() == "L_COMMAND":
            return self.currentCommand[1:-1]

    def dest(self) -> str:
        '''
        Returns the dest mnemonic in the current C-command (8 possibilities). 
        Should be called only when commandType() is C_COMMAND.
        '''

        destination = self.currentCommand.split("=")[0]
        if destination == self.currentCommand:
            return "null"
        return destination
    
    def comp(self) -> str:
        '''
        Returns the comp mnemonic in the current C-command (28 possibilities).
        Should be called only when commandType() is C_COMMAND
        '''
        if ";" in self.currentCommand:
            compVal = self.currentCommand.split(";")[0]
        elif "=" in self.currentCommand:
            compVal = self.currentCommand.split('=')[-1]
        return compVal
    
    def jump(self) -> str:
        '''
        Returns the jump mnemonic in the current C-command (8 possibilities). 
        Should be called only when commandType() is C_COMMAND.
        '''
        jumpCond = self.currentCommand.split(";")[-1].strip()
        if jumpCond == self.currentCommand:
            return "null"
        return jumpCond
    
    def getCommand(self):
        return self.currentCommand