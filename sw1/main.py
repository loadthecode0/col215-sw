#defining node, gate and circuit objects  ========================================================================
class Node :
    def __init__(self, index, name, if_input, if_output) -> None:
        self.nodeIndex = index
        self.nodeName = name
        self.is_input = if_input
        self.is_output = if_output
        self.gate = 0 # gate outputting to this node
        self.outGates = []
        self.inputs = [] 
        self.inDelay = 0 #for part A
        self.reqDelay = 0 #for Part B
        
    def displayNode(self):
        print(self.nodeIndex, self.nodeName, self.is_input, self.is_output, self.gate, self.outGates, self.inDelay, self.inputs, self.reqDelay)
        
class Gate :
    def __init__(self, index, type, inputs, output) -> None:
        self.gateIndex = index
        self.gateType = type
        self.gateDelay = 0 #delay at time of output
        self.inputs = inputs #list of nodes giving input
        self.output = output #Node taking output
            
    def displayGate(self):
        print (self.gateIndex, self.gateType, self.gateDelay, self.inputs, self.output)
    
class Circuit:
    
    def __init__(self) -> None:
        
        self.gateCount = 0 
        self.nodeCount = 0
                
        #dictionary of node objects, accessed by their names
        self.nodes = {}
        
        #lists of node objects
        self.inputNodesList = [] 
        self.outputNodesList = []
        
        #useful stuff, don't mess around with these
        self.gates= [] #list containing all gate OBJECTS
        self.gateTypeDict = {}
        
    def nodeInserter(self,arr, if_input, if_output) :
        for z in range(len(arr)) :
            self.nodeCount += 1
            index = self.nodeCount
            name = arr[z]
            self.nodes[name] = Node(index, name, if_input, if_output)
            if (if_input == True) :
                self.nodes[name].gate = 0
                self.inputNodesList.append(self.nodes[name])
            elif (if_output == True) :
                self.outputNodesList.append(self.nodes[name])
            
    def displayCircuit(self) :
        for i in self.nodes:
            self.nodes[i].displayNode()
        for j in range(len(self.gates)) :
            self.gates[j].displayGate()
            

#reading inputs and updating created objects ============================================================

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
        if (wordsInLine[0]=='PRIMARY_INPUTS' ):
            circuit.inputNodesDelays = dict.fromkeys(wordsInLine[1:], 0)
            circuit.nodeInserter(wordsInLine[1:], True, False) #inserts all nodes in current line
        elif (wordsInLine[0]=='PRIMARY_OUTPUTS'):
            circuit.outputNodesDelays = dict.fromkeys(wordsInLine[1:], 0)
            circuit.nodeInserter(wordsInLine[1:], False, True)
            
        elif (wordsInLine[0]=='INTERNAL_SIGNALS'):
            circuit.intNodesDelays = dict.fromkeys(wordsInLine[1:], 0)
            circuit.nodeInserter(wordsInLine[1:], False, False)
        else :
            circuit.gateCount += 1
            index = circuit.gateCount
            type = wordsInLine[0]
            inputList = wordsInLine[1:(len(wordsInLine)-1)]
            output = wordsInLine[len(wordsInLine)-1] #node to which this gate outputs to
            circuit.gates.append(Gate(index, type, inputList, output))
            #assuming each internal or output node is associated as an output of a gate 
            #map each int/output node to the corresponding gate outputting to it
            circuit.nodes[output].gate = index
            #map each node inputting to this gate with the gate
            for nodeName in inputList:
                if(circuit.nodes[nodeName].is_output == False):
                    circuit.nodes[nodeName].outGates.append(index)
            # circuit.gates[index-1].displayGate()    
            try :
                circuit.gateTypeDict[type].append(index)
            except KeyError:
                circuit.gateTypeDict[type] = []
                circuit.gateTypeDict[type].append(index)
    
    #specifying input side nodes for each node
    for i in circuit.nodes :
        if(circuit.nodes[i].is_input == False):
            gateNo = circuit.nodes[i].gate #list gates(s) outputting to this node
            circuit.nodes[i].inputs = circuit.gates[gateNo].inputs
            
    #specifying input side nodes for each node
    for i in circuit.nodes :
        if(circuit.nodes[i].is_output == False):
            gateNo = circuit.nodes[i].gate #list gates(s) outputting to this node
            circuit.nodes[i].inputs = circuit.gates[gateNo].inputs
    
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
                gate = circuit.gates[gateIndices[z]]
                gate.gateDelay = delay
                # gate.displayGate()
        except KeyError:
            pass
        
def readReqDelayFile (circuit, filename) :
    
    validLines = [] #storing valid input lines
    Lines = filename.readlines() # stores each line of circuit file as a string in a list Lines
    
    for x in range(len(Lines)) :
        currLine = Lines[x]
        i = 0
        while (currLine[i] == ' ') : #find first character after any spaces
            i += 1
        if ((currLine[i] != '/') and (currLine[i] != '\n')) :
            validLines.insert(len(validLines), currLine) #checked, works
            
    for y in range(len(validLines)) : #read and map gates to corresponding gate delays
        wordsInLine = validLines[y].split() 
        try:
            circuit.nodes[wordsInLine[0]].reqDelay = wordsInLine[1]
        except KeyError:
            pass
        
#calculation for part A =====================================================================
def calcDelayNode(circuit, node) -> float :#recursive function to calculate delays
    maxDelay = 0
    gateDelay = circuit.gates[node.gate].gateDelay
    if(node.is_input == True):
        return 0
    for otherNodeName in node.inputs:
        otherNode = circuit.nodes[otherNodeName]
        maxDelay = max(maxDelay, calcDelayNode(circuit, otherNode))
    node.inDelay = maxDelay + float(gateDelay)
    return (node.inDelay)
        
def calcA(circuit):
    for outNode in circuit.outputNodesList :
        calcDelayNode(circuit, outNode)
        
#calculation for part B =======================================================================================
def calcOutDelayNode(circuit, node) -> float :
    reqDelay = float('inf')
    if(node.is_output == True):
        return node.reqDelay
    if(node.reqDelay != 0): #has been calculated earlier
        return node.reqDelay
    for outputGateNo in node.outGates:
        outNode = circuit.nodes[circuit.gates[outputGateNo].output]
        outputGateDelay = circuit.gates[outputGateNo].gateDelay
        reqDelay = min(reqDelay, float(calcOutDelayNode(circuit, outNode)) - float(outputGateDelay))
        if (reqDelay < 0) :
            raise Exception('Invalid set of required outputs')
    node.reqDelay = reqDelay
    return (node.reqDelay)
        
def calcB(circuit):
    for outNode in circuit.inputNodesList :
        calcOutDelayNode(circuit, outNode)

#writing outputs==========================================================            
def writeOutputDelayFile(circuit, filename) :
    for x in circuit.outputNodesList: #x is an output node object
        delay = x.inDelay
        if (int(delay) == delay):
            delay = int(delay)
        filename.write(str(x.nodeName) + " " + str(delay) + "\n" )
        
def writeInputDelayFile(circuit, filename) :
    for x in circuit.inputNodesList:
        delay = x.reqDelay
        if (int(delay) == delay):
            delay = int(delay)
        filename.write(str(x.nodeName) + " " + str(delay) + "\n" )

#main=======================================================================
def main():
    
    #all input files
    circuitFile = open('circuit.txt', 'r')
    delayFile = open("gate_delays.txt",'r') #universal : gate delay values for each gate
    reqDelays = open("required_delays.txt", 'r') # input for part B
    
    #all output files
    outputDelayFile = open("output_delays.txt","a") # output for part A
    inputDelays = open("input_delays.txt","a") # output for part B
    
    C = Circuit()
    C.gates.append(Gate(0, 'dummy', 'dummy', 'dummy')) #dummy gate attached

    readCircuitFile(C, circuitFile) #tested, works
    readGateDelayFile (C, delayFile)
    readReqDelayFile (C, reqDelays)
    calcA(C)
    calcB(C)
    C.displayCircuit()
    writeOutputDelayFile(C, outputDelayFile)
    writeInputDelayFile(C, inputDelays)
    
    circuitFile.close()
    delayFile.close()
    reqDelays.close()
    outputDelayFile.close()
    inputDelays.close()
    
if __name__ == "__main__":
    main()