import numpy as np

def readInputs(filename) :
    open(filename,"r")
    
class Node :
    def __init__(self) -> None:
        self.inputs = []
        self.outputs = []
        self.inDelay = 0
        self.outDelay = 0

class Circuit:
    
    def __init__(self) -> None:
        self.intNodes = {}
        self.inputNodes = {}
        self.outputNodes = {}
        
        
        self.gates= {} #dictionary for storing delays
        self.gateInputNodes=[]
        self.gateOutputNodes=[]
        
    # def defineIntNode(self, data) :
    #     self.intNodes.insert(len(self.intNodes), data)
        
    # def defineInputNode(self, data) :
    #     self.inputNodes.insert(len(self.inputNodes), data)
    
    # def defineOutputNode(self, data) :
    #     self.outputNodes.insert(len(self.outputNodes),data)
        
    # def printInputNodes(self) :
    #     print(*self.inputNodes)
        
def readCircuitFile(circuit, filename) :
    validLines = [] #storing valid input lines
    Lines = filename.readlines() # stores each line of circuit file as a string in a list Lines
    
    for x in range(len(Lines)) :
        currLine = Lines[x]
        i = 0
        while (currLine[i] == ' ') : #find first character after any spaces
            i += 1
        if ((currLine[i] != '/') and (currLine[i] != '\n')) :
            validLines.insert(len(validLines), currLine) #checked, works
    
    for y in range(len(validLines)) :
        wordsInLine = validLines[y].split() 
        if (wordsInLine[0]=='PRIMARY_INPUTS'):
            circuit.inputNodes = dict.fromkeys(wordsInLine[1:], 0)
        elif (wordsInLine[0]=='PRIMARY_OUTPUTS'):
            circuit.outputNodes = dict.fromkeys(wordsInLine[1:], 0)
        elif (wordsInLine[0]=='INTERNAL_SIGNALS'):
            circuit.intNodes = dict.fromkeys(wordsInLine[1:], 0)
        else :
            circuit.gates[wordsInLine[0]] = [0, wordsInLine[1:(len(wordsInLine)-1)], wordsInLine[len(wordsInLine)-1]]
    print (circuit.inputNodes)
    print (circuit.outputNodes)
    print (circuit.intNodes)
    print (circuit.gates)
            
def writeOutputDelayFile(circuit, filename) :
    for x in range(len(circuit.outputNodes)):
        filename.write("Test \n")
    
# close all files at the end!

def main(): # checked, works
    
    print("Hello")
    
    #all input files
    circuitFile = open('circuit.txt', 'r')
    delays = open("gate_delays.txt",'r') #universal : gate delay values for each gate
    reqDelays = open("required_delays.txt", 'r') # input for part B
    
    #all output files
    outputDelays = open("output_delays.txt","a") # output for part A
    inputDelays = open("input_delays.txt","a") # output for part B
    
    C = Circuit()
    # C.defineInputNode("A")
    # C.defineInputNode("B")
    # C.printInputNodes()

    readCircuitFile(C, circuitFile) #tested, works
    writeOutputDelayFile(C, outputDelays)
    
if __name__ == "__main__":
    main()