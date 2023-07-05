class SymbolTable:
    def __init__(self):
        '''
        Creates a new empty symbol table.
        '''
        self.symbolMap = {
            'SP':0, 'LCL':1, 'ARG':2, 'THIS': 3, 'THAT': 4,
            'R0': 0, 'R1':1, 'R2':2, 'R3':3, 'R4':4, 'R5':5,
            'R6':6, 'R7':7, 'R8':8, 'R9':9, 'R10':10, 'R11': 11,
            'R12':12, 'R13':13, 'R14':14, 'R15':15,
            'SCREEN': 16384, 'KBD': 24576
        }
        self.nextAddress = 16

    def addEntry(self, symbol: str, address: int):
        '''
        Adds the pair (symbol, address) to the table.
        '''
        if symbol not in self.symbolMap:
            self.nextAddress += 1
        self.symbolMap[symbol] = address

    def contains(self, symbol: str) -> bool:
        '''
        Returns if the symbol table contains the symbol.
        '''
        return symbol in self.symbolMap

    def GetAddress(self, symbol: str) -> int:
        '''
        Returns the address associated with the symbol.
        Only called if the symbolMap contains the entry.
        '''
        return self.symbolMap[symbol]
    
    def getNextAddress(self):
        return self.nextAddress

    def setNextAddress(self):
        self.nextAddress = 16