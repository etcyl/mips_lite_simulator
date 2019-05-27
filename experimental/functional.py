#!/usr/bin/env python

from mips_stage import stage
from bitstring import Bits
from bitstring import BitArray
import sys

arithmetic_inst = 0
total_instructions = 0
logical_inst = 0
mem_inst = 0
cntrl_inst = 0

def functional(filename):
    
    def memory_trace_reader(filename):
        f_ptr = open(filename, 'r')
        mem = f_ptr.read().splitlines()
        for i in range(len(mem)):
            #mem[i] = int(mem[i], 16)
            #mem[i] = bin(mem[i])
            val = BitArray('0' + 'x' + str(mem[i]))
            mem[i] = val
            #mem[i] = int(mem[i], 10)
            #mem[i] = val.int
            #print 'mem' + str(i) + ': ', mem[i], '\n'
        return mem
    
    def print_instruction_counts():
        print 'Total number of instructions: ', total_instructions, '\n'
        print 'Arithmetic instructions: ', arithmetic_inst, '\n'
        print 'Logical instructions: ', logical_inst, '\n'
        print 'Memory access instructions: ', mem_inst, '\n'
        print 'Control transfer instructions: ', cntrl_inst, '\n'
        return

    def decode(instruction):
        print 'original instruction is: ', instruction, '\n' #bin(instruction), '\n'
        #instruction = int(instruction, 2)
        instruction = instruction.bin
        #print 'instruction is: ', instruction, '\n'
        opcode = Bits(bin=instruction[:6]) # Get the final 6 bits of the instruction
        print 'opcode: ', opcode, '\n'
        if opcode == BitArray('0x00') or opcode == BitArray('0x02') or opcode == BitArray('0x04') or \
           opcode == BitArray('0x06') or opcode == BitArray('0x08') or opcode == BitArray('0x0A'):
            rs = Bits(bin=instruction[6:11]) #(instruction >> 21) & 0b00000011111
            rt = Bits(bin=instruction[12:17]) #(instruction >> 16) & 0b0000000000011111
            rd = Bits(bin=instruction[18:23])#(instruction >> 11) & 0b000000000000000011111
            _type = "R-type"
            print 'True'
            return (opcode, rs, rt, rd, _type)

        if opcode == BitArray('0x01') or opcode == BitArray('0x03') or opcode == BitArray('0x05') or \
           opcode == BitArray('0x07') or opcode == BitArray('0x09') or opcode == BitArray('0x0B') or \
           opcode == BitArray('0x0C') or BitArray('0x0D') or BitArray('0x0E') :
            rs = Bits(bin=instruction[6:11])#(instruction >> 21) & 0b00000011111
            rt = Bits(bin=instruction[12:17])#(instruction >> 16) & 0b0000000000011111 
            immediate = Bits(bin=instruction[18:-1])#(instruction << 16)
            #immediate = #immediate >> 16
            _type = "I-type"
            return (opcode, rs, rt, immediate, _type)

        else:
            print 'Error decoding', '\n'
            return (-1, -1, -1, -1, "INVALID")    

    def execute_action(s):
        global arithmetic_inst
        global logical_inst
        global mem_inst
        global cntrl_inst
        global total_instructions
        total_instructions += 1
        print 's.get_opcode() is: ', s.get_opcode(), '\n'        
        if s.get_opcode() == '0b000000':#BitArray('0x00'): # ADD
            arithmetic_inst += 1
            return
        elif s.get_opcode() == '0b000010':#BitArray('0x02'): # SUB
            arithmetic_inst += 1 
            return
        elif s.get_opcode() == '0b000100':#BitArray('0x04'): # MUL
            arithmetic_inst += 1
            return
        elif s.get_opcode() == '0b000110':#BitArray('0x06'): # OR
            logical_inst += 1
            return 
        elif s.get_opcode()  == '0b001000':#BitArray('0x08'): # AND 
            logical_inst += 1
            return
        elif s.get_opcode()  == '0b001010':#BitArray('0x0A'): # XOR
            logical_inst += 1
            return
        elif s.get_opcode() == '0b000001': # ADDI
            arithmetic_inst += 1
            return
        elif s.get_opcode() == '0b000011': # SUBI
            arithmetic_inst += 1
            return
        elif s.get_opcode() == '0b000101': # MULI
            arithmetic_inst += 1
            return
        elif s.get_opcode() == '0b000111': # ORI
            logical_inst += 1
            return
        elif s.get_opcode() == '0b001001': # ANDI
            logical_inst += 1
            return
        elif s.get_opcode() == '0b001011': # XORI
            logical_inst += 1
            return
        elif s.get_opcode() == '0b001100': # LDW
            mem_inst += 1
            return
        elif s.get_opcode() == '0b001101': # STW
            mem_inst += 1
            return
        elif s.get_opcode() == '0b001110': # BZ
            cntrl_inst += 1
            return
        elif s.get_opcode() == '0b001111': # BEQ
            cntrl_inst += 1
            return
        elif s.get_opcode() == '0b010000': # JR
            cntrl_inst += 1
            return
        elif s.get_opcode() == '0b010001': # HALT
            cntrl_inst += 1
            return

        print 'Error during execute_action() func, opcode did not match with known values\n'        
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
        (opcode, rs, rt, rd, _type) = decode(instruction)
        print 'opcode type is: ', opcode, '\n'
        #print 'opcode is: ', opcode, 'rs is: ', rs, 'rd is: ', rd, 'type is: ', _type, '\n' 
        if opcode == 0b010001:
            halt = 1
            break
        if _type == "R-type":
            s.set_opcode(opcode)
            s.set_rs(rs)
            s.set_rt(rt)
            s.set_rd(rd)
            s.set_type(_type)
        elif _type == "I-type":
            s.set_opcode(opcode)
            s.set_rs(rs)
            s.set_rt(rt)
            s.set_immediate(rd)
            s.set_type(_type)   
        execute_action(s)
        memory_action(s)
        writeback(s)   
        counter += 1
        if counter == 30:
            halt = 1 
        PC += 4 
 
    print_instruction_counts()
    print 'Program Counter: ', PC, '\n' 
    for i in range(len(registers)):
        print 'R' + str(i) + ':', registers[i], '\n'
    return

fn = "/Users/mattf/Desktop/trace.txt"
functional(fn)
