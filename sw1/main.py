import numpy as np

def readInputs(filename) :
    open(filename,"r")
    
class Node :
    def __init__(self) -> None:
        self.inputs = []
        self.outputs = []
        self.inDelay = 0 #for part A
        self.reqDelay = 0 #for Part B
        
class Gate :
    def __init__(self, index, type, inputs, output) -> None:
        self.gateIndex = index
        self.gateType = type
        self.gateDelay = 0
        self.inputs = inputs #list of nodes giving input
        self.output = output
        
    def calculateGateOutputDelay(self, circuit) -> int:
        t = 0
        for x in range(len(self.inputs)):
            t = max(t, circuit.inputNode[self.input[x]])
            
    def displayGate(self):
        print (self.gateIndex, self.gateType, self.gateDelay, self.inputs, self.output)
    
class Circuit:
    
    def __init__(self) -> None:
        
        self.gateCount = 0 
        self.intNodes = {}
        self.inputNodes = {}
        self.outputNodes = {}
        
        
        self.gates= [] #list containing all gate OBJECTS
        self.gateTypeDict = {}
        # self.gateInputNodes=[]
        # self.gateOutputNodes=[]
        
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
            circuit.gateCount += 1
            index = circuit.gateCount
            type = wordsInLine[0]
            inputList = wordsInLine[1:(len(wordsInLine)-1)]
            output = wordsInLine[len(wordsInLine)-1]
            circuit.gates.append(Gate(index, type, inputList, output))
            # circuit.gates[index-1].displayGate()    
            try :
                circuit.gateTypeDict[type].append(index)
            except KeyError as error :
                circuit.gateTypeDict[type] = []
                circuit.gateTypeDict[type].append(index)
    print (circuit.inputNodes)
    print (circuit.outputNodes)
    print (circuit.intNodes)
    print (circuit.gateCount)
    print (circuit.gateTypeDict)
    
def readGateDelayFile (circuit, filename) :
    
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
        type = wordsInLine[0]
        try:
            delay = wordsInLine[1]
            gateIndices = circuit.gateTypeDict[type]
            for z in range(len(gateIndices)) :
                gate = circuit.gates[gateIndices[z] - 1]
                gate.gateDelay = delay
                gate.displayGate()
        except KeyError:
            pass
    
    
            
def writeOutputDelayFile(circuit, filename) :
    for x in circuit.outputNodes:
        filename.write(str(x) + " " + str(circuit.outputNodes[x]) + "\n" )
    
# close all files at the end!

def main(): # checked, works
    
    print("Hello")
    
    #all input files
    circuitFile = open('circuit.txt', 'r')
    delayFile = open("gate_delays.txt",'r') #universal : gate delay values for each gate
    reqDelays = open("required_delays.txt", 'r') # input for part B
    
    #all output files
    outputDelayFile = open("output_delays.txt","a") # output for part A
    inputDelays = open("input_delays.txt","a") # output for part B
    
    C = Circuit()
    # C.defineInputNode("A")
    # C.defineInputNode("B")
    # C.printInputNodes()

    readCircuitFile(C, circuitFile) #tested, works
    readGateDelayFile (C, delayFile)
    writeOutputDelayFile(C, outputDelayFile)
    
if __name__ == "__main__":
    main()