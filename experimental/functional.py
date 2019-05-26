#!/usr/bin/env python
# https://www.eg.bucknell.edu/~csci320/mips_web/

from mips_stage import stage
import sys

def functional(filename):
    # Total number of instructions and a breakdown of instruction frequencies for the following instruction types:
    # Arithmetic, Logical, Memory Access, Control Transfer
    total_instructions = 0
    arithmetic_inst = 0  # Number of arithmetic instructions
    logical_inst = 0
    mem_inst = 0
    cntrl_inst = 0
 
    def memory_trace_reader(filename):
        f_ptr = open(filename, 'r')
        mem = f_ptr.read().splitlines()
        for i in range(len(mem)):
            mem[i] = int(mem[i], 16)
            mem[i] = bin(mem[i])
        return mem
    
    def print_instruction_counts():
        print 'Total number of instructions: ', total_instructions, '\n'
        print 'Arithmetic instructions: ', arithmetic_inst, '\n'
        print 'Logical instructions: ', logical_inst, '\n'
        print 'Memory access instructions: ', mem_inst, '\n'
        print 'Control transfer instructions: ', cntrl_inst, '\n'
        return
    
    def execute_action(stage):
        return

    def memory_action(stage):
        return
    
    def writeback(stage):
        return    

    global PC
    global IR
    PC = 0 # Set the Program Counter and Instruction Register to 0
    IR = 0
    registers = [0]*15 # List of 16 general purposes registers  
    counter = 0
    halt = 0
    s = stage()
    memory_trace = memory_trace_reader(filename)
    #print("Memory trace:", memory_trace, "\n")
    while not halt: # Grab a line from the memory trace
        instruction = memory_trace[counter]
        IR = instruction
        print 'Instruction is: ', instruction, '\n'        
        counter += 1
        PC += 4 
        halt = 1
 
    print_instruction_counts()
    print 'Program Counter: ', PC, '\n' 
    for i in range(len(registers)):
        print 'R' + str(i) + ':', registers[i], '\n'
    return

fn = "/Users/mattf/Desktop/renamed/input1.txt"
functional(fn)
