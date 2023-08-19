import numpy as np
import os

def readInputs(filename):
    open(filename,"r")

#read circuit file

# close all files at the end!

def main():
    
    print("Hello")
    
    #all input files
    circuitFile = readInputs("circuit.txt") #universal : circuit structure
    delays = readInputs("gate_delays.txt") #universal : gate delay values for each gate
    reqDelays = readInputs("required_delays.txt") # input for part B
    
    #all output files
    outputDelays = open("output_delays.txt","w+") # output for part A
    inputDelays = open("input_delays.txt","w+") # output for part B
    
if __name__ == "__main__":
    main()