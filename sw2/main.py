import sys

#note: mapping input list to gates is not required, delete if you want later

#defining node, gate and circuit objects  ========================================================================
class Node :
    def __init__(self, index, name, if_input, if_output) -> None:
        self.nodeIndex = index
        self.nodeName = name #str
        self.is_input = if_input
        self.is_output = if_output
        self.gate = 0 # gate outputting to this node
        self.outGates = [] # gates to which output of this gate is going
        self.inputs = []  #list of nodes giving input to the gate associated with this node
        self.inDelay = 0 #for part A
        self.reqDelay = 0 #for Part B
        
    def displayNode(self):
        print(self.nodeIndex, self.nodeName, self.is_input, self.is_output, self.gate, self.inputs, self.gate, self.outGates, self.inDelay, self.reqDelay)
        
class Gate :
    def __init__(self, index, type, inputs, output) -> None:
        self.gateIndex = index
        self.gateType = type #string
        self.gateDelay = [0, 0, 0] #delay at time of output
        self.area = [0, 0, 0] #possible areas
        self.usedImpl = 0 #for part 2 0/1/2
        self.inputs = inputs #list of nodes giving input to this gate
        self.output = output #Node taking output (str)
            
    def displayGate(self):
        print (self.gateIndex, self.gateType, self.gateDelay, self.area, self.inputs, self.output)
    
class Circuit:
    
    def __init__(self) -> None:
        self.gateCount = 0 
        self.nodeCount = 0
                
        #dictionary of all node objects, accessed by their names as keys
        self.nodes = {}
        
        #lists of input/output node objects
        self.inputNodesList = [] 
        self.outputNodesList = []
        
        #useful stuff, don't mess around with these
        self.gates= [] #list containing all gate OBJECTS
        self.gateTypeDict = {} #dictionary of all gate types and corresponding gate indices
        
        self.outputTrees = {} #contains all output trees accessed by corresponding output node
        self.outputPathDelays = ()
        
    def nodeInserter(self,arr, if_input, if_output) : #helper function
        for name in arr :
            self.nodeCount += 1
            index = self.nodeCount
            self.nodes[name] = Node(index, name, if_input, if_output)
            if (if_input == True) :
                self.nodes[name].gate = 0
                self.inputNodesList.append(self.nodes[name])
            elif (if_output == True) :
                self.outputNodesList.append(self.nodes[name])
            
    def resetCircuit(self):
        for nodeName in self.nodes:
            self.nodes[nodeName].inDelay = 0
        for gate in self.gates:
            gate.usedImpl = 0
    
    def displayCircuit(self) :
        print(self.nodeCount, self.gateCount)
        for i in self.nodes:
            self.nodes[i].displayNode()
        for j in range(len(self.gates)) :
            self.gates[j].displayGate()
            
#reading inputs and updating created objects ============================================================

def generateValidLinesList(filename) -> list:
    validLines = [] #storing valid input lines
    Lines = filename.readlines() # stores each line of circuit file as a string in a list Lines
    for currLine in Lines :
        i = 0
        while (currLine[i] == ' ') : #find first character after any spaces
            i += 1
        if currLine[i] not in ['/', '\n'] : #then it is a valid line
            validLines.insert(len(validLines), currLine) #checked, works, basically push_back(currLine)
    return validLines

def readCircuitFile(circuit, filename) :
    validLines = generateValidLinesList(filename)    
    for currLine in validLines :
        wordsInLine = currLine.split() #list of all words in current line
        if (wordsInLine[0]=='PRIMARY_INPUTS'):
            circuit.nodeInserter(wordsInLine[1:], True, False) #inserts all nodes in current line into the nodes List
        elif (wordsInLine[0]=='PRIMARY_OUTPUTS'):
            circuit.nodeInserter(wordsInLine[1:], False, True)
        elif (wordsInLine[0]=='INTERNAL_SIGNALS'):
            circuit.nodeInserter(wordsInLine[1:], False, False)
        elif (wordsInLine[0]=='DFF'): #then the input and output ports of DFF must have already been included in above three conditions, change to input/output node as applicable
            inDFF = wordsInLine[1]
            outDFF = wordsInLine[2]
            if ((circuit.nodes[inDFF] not in circuit.outputNodesList)) : #treat inDFF as output node
                circuit.outputNodesList.append(circuit.nodes[inDFF])
                circuit.nodes[inDFF].is_output = True
            if ((circuit.nodes[outDFF] not in circuit.inputNodesList)) : #treat inDFF as input node
                circuit.inputNodesList.append(circuit.nodes[outDFF])
                circuit.nodes[outDFF].is_input = True
        else : #gates input now
            circuit.gateCount += 1
            index = circuit.gateCount
            gateType = wordsInLine[0]
            inputList = wordsInLine[1:-1] #all except last node are inputs to this particular gate
            output = wordsInLine[len(wordsInLine)-1] #node to which this gate outputs to
            circuit.gates.append(Gate(index, gateType, inputList, output))
            #assuming each internal or output node is associated as an output of a gate 
            #map each int/output node to the corresponding gate outputting to it
            circuit.nodes[output].gate = index
            circuit.nodes[output].inputs = inputList
            #map each node inputting to this gate with the gate
            for nodeName in inputList:
                if(circuit.nodes[nodeName].is_output == False):
                    circuit.nodes[nodeName].outGates.append(index)
                else :
                    raise Exception('An output node cannot serve as input or internal signal')  #RECTIFY THIS!  
            try : # inserting each gate type into the dict (initialization)
                circuit.gateTypeDict[gateType].append(index)
            except KeyError:
                circuit.gateTypeDict[gateType] = [index]
    
def readGateDelayFile (circuit, filename) :
    validLines = generateValidLinesList(filename)    
    for currLine in validLines :
        wordsInLine = currLine.split()
        gateType = wordsInLine[1]
        try:
            implIndex = ord(wordsInLine[0][len(gateType) + 1]) - 48
            delay = wordsInLine[2]
            area = wordsInLine[3]
            gateIndices = circuit.gateTypeDict[gateType] #fetches list of indices of gates of this type
            for index in gateIndices :
                circuit.gates[index].gateDelay[implIndex - 1] = float(delay)
                circuit.gates[index].area[implIndex - 1] = float(area)
        except KeyError:
            print(f'{gateType} Gate not present in circuit')
            
    #sort now
    for gate in circuit.gates :
        gate.gateDelay.sort()
        gate.area.sort(reverse = True)
        
# def readReqDelayFile (circuit, filename) :
#     validLines = generateValidLinesList(filename)                
#     for currLine in validLines :
#         wordsInLine = currLine.split()
#         try:
#             circuit.nodes[wordsInLine[0]].reqDelay = wordsInLine[1]
#         except KeyError:
#             print('Node not present in circuit')
        
#calculation for part A =====================================================================
def calcDelayNode(circuit, node) -> float :#recursive function to calculate delays
    maxDelay = 0
    gate = circuit.gates[node.gate]
    gateDelay = gate.gateDelay[gate.usedImpl]
    if(node.is_input == True):
        return 0
    if(node.inDelay != 0): #has been calculated earlier, my DP measure
        return node.inDelay
    for otherNodeName in node.inputs:
        otherNode = circuit.nodes[otherNodeName]
        maxDelay = max(maxDelay, calcDelayNode(circuit, otherNode))
    node.inDelay = maxDelay + float(gateDelay)
    return (node.inDelay)
        
def calcLongestDelay(circuit, filename):
    circuit.resetCircuit()
    try:
        for outNode in circuit.outputNodesList :
            calcDelayNode(circuit, outNode)
    except Exception as e:
        filename.write(str(e) + '\n')
        raise Exception from e
    longestDelay = 0
    for x in circuit.outputNodesList: #x is an output node object
        longestDelay = max(longestDelay, x.inDelay)
    return longestDelay
        
#calculation for part B =======================================================================================
def DFSUtil(gateNo, circuit):
        
    print(gateNo, end=' ')
    for nodeName in circuit.gates[gateNo].inputs:
        if circuit.nodes[nodeName].is_input == False:
            DFSUtil(circuit.nodes[nodeName].gate, circuit)

# The function to do DFS traversal. It uses
# recursive DFSUtil()
def constructOutputTrees(circuit):
    
    for outNode in circuit.outputNodesList :
        DFSUtil(outNode.gate, circuit)
        print("\n")

    
    
        
# def calcB(circuit, filename):
#     try:
#         for outNode in circuit.inputNodesList :
#             calcOutDelayNode(circuit, outNode)
#     except Exception as e:
#         filename.write(str(e) + '\n')
#         raise Exception from e

#writing outputs==========================================================            
def writeLongestDelayFile(circuit, filename):
    longestDelay = calcLongestDelay(circuit, filename)
    if (int(longestDelay) == longestDelay):
            longestDelay = int(longestDelay)
    filename.write(str(longestDelay) + "\n")
        
def writeInputDelayFile(circuit, filename) :
    for x in circuit.inputNodesList:
        delay = x.reqDelay
        if (int(delay) == delay):
            delay = int(delay)
        filename.write(f"{str(x.nodeName)} {str(delay)}" + "\n")

#main=======================================================================
def main():  
    C = Circuit() #declare circuit
    C.gates.append(Gate(0, 'dummy', 'dummy', 'dummy')) #dummy gate attached
    
    #all input files
    with open(sys.argv[2], 'r') as circuitFile: # input for part A
        readCircuitFile(C, circuitFile) #tested, works
    with open(sys.argv[3],'r') as delayFile: #universal : gate delay values for each gate
        readGateDelayFile (C, delayFile)
    # with open(sys.argv[4], 'r') as longestDelay: # input for part B
    #     readReqDelayFile (C, reqDelays)

    #all output files
    if sys.argv[1] == 'A' :
        with open("longest_delay.txt","a") as longestDelayFile:
            writeLongestDelayFile(C, longestDelayFile) # output for part A
    # elif sys.argv[1] == 'B':
    #     with open("input_delays.txt","a") as inputDelays:
    #         calcB(C, inputDelays)
    #         writeInputDelayFile(C, inputDelays)# output for part B
    
    C.displayCircuit()
    constructOutputTrees(C)
    
if __name__ == "__main__":
    main()