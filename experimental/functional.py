#!/usr/bin/env python

from mips_stage import stage
from bitstring import Bits
from bitstring import BitArray
import sys

arithmetic_inst = 0
PC = 0
IR = 0
jump_flag =0
halt = 0
arithmetic_inst = 0
registers = [0]*15
total_instructions = 0
logical_inst = 0
mem_inst = 0
cntrl_inst = 0
counter = 0

def functional(filename):
    global arithmetic_inst
    global registers
    global total_instructions
    global logical_inst
    global mem_inst
    global cntrl_inst
    global halt
    global PC
    global IR
    global jump_flag
    global counter
    #memory_trace = []
    mem_extend = [0]*1000
    
    def print_instruction_counts():
        print 'Total number of instructions: ', arithmetic_inst + logical_inst + mem_inst + cntrl_inst, '\n'
        print 'Arithmetic instructions: ', arithmetic_inst, '\n'
        print 'Logical instructions: ', logical_inst, '\n'
        print 'Memory access instructions: ', mem_inst, '\n'
        print 'Control transfer instructions: ', cntrl_inst, '\n'
        return

    def decode(inst):
        inst = int(str(inst), 16)
        opcode = inst >> 26
        print 'inst and opcode are: ', inst, opcode, '\n'
        if opcode == 0b000000 or opcode == 0b000010 or opcode == 0b000100 or \
                opcode == 0b000110 or opcode == 0b001000 or opcode == 0b001010:
            rs = (inst >> 21 ) & 0b00000011111
            rt = (inst >> 16 ) & 0b0000000000011111
            rd = (inst >> 11) & 0b000000000000000011111
            _type = "R-type"
            return (opcode, rs, rt, rd, _type) 
        elif opcode == 0b000001 or opcode == 0b000011 or opcode == 0b000101 or \
                opcode == 0b000111 or opcode == 0b001001 or opcode == 0b001011 or \
                opcode == 0b001100 or opcode == 0b001101 or opcode == 0b001110 or \
                opcode == 0b001111 or opcode == 0b010000 or opcode == 0b010001:
            rs = (inst >> 21) & 0b00000011111
            rt = (inst >> 16) & 0b0000000000011111
            immediate = (inst) & 0b00000001111111111111111
            sign = immediate >> 15
            if sign == 0b1:
                immediate = BitArray(bin=bin(immediate).int)
            _type = "I-type"
            return (opcode, rs, rt, immediate, _type)

    def execute_action(memory_trace, s):
        global arithmetic_inst
        global logical_inst
        global mem_inst
        global cntrl_inst
        global total_instructions
        global registers
        global counter
        global jump_flag
        global halt
        print 's.get_opcode() is: ', s.get_opcode(), '\n'        
        if s.get_opcode() == 0b000000:# ADD
            arithmetic_inst += 1
            print 'type of rd: ', type(s.get_rd()), '\n'
            rd = s.get_rd()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'rs + rt = ', rs + rt, '\n'
            registers[rd] = registers[rs] + registers[rt]
            return
        elif s.get_opcode() == 0b000010:# SUB
            arithmetic_inst += 1
            rd = s.get_rd()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'rs - rt = ', rs - rt, '\n'
            registers[rd] = registers[rs] - registers[rt]
            return
        elif s.get_opcode() == 0b000100:# MUL
            arithmetic_inst += 1
            rd = s.get_rd()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'rs * rt = ', rs * rt, '\n'
            registers[rd] = registers[rs] * registers[rt]
            return
        elif s.get_opcode() == 0b000110:# OR
            logical_inst += 1
            rd = s.get_rd()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'rt OR rs = ', rs | rs, '\n'
            registers[rd] = registers[rs] | registers[rt]
            return 
        elif s.get_opcode()  == 0b001000:# AND 
            logical_inst += 1
            rd = s.get_rd()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'rt AND rs = ', rt & rs, '\n'
            registers[rd] = registers[rs] & registers[rt]
            return
        elif s.get_opcode()  == 0b001010:# XOR
            logical_inst += 1
            rd = s.get_rd()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'rt XOR rs = ', rt ^ rs, '\n'
            registers[rd] = registers[rs] ^ registers[rt]
            return
        elif s.get_opcode() == 0b000001: # ADDI
            arithmetic_inst += 1
            imm = s.get_immediate()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'rs + imm = ', rs + imm, '\n'
            registers[rt] = registers[rs] + imm
            return
        elif s.get_opcode() == 0b000011: # SUBI
            imm = s.get_immediate()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'rs - imm = ', registers[rs] - imm, '\n'
            registers[rt] = rs - imm
            arithmetic_inst += 1
            return
        elif s.get_opcode() == 0b000101: # MULI
            arithmetic_inst += 1
            imm = s.get_immediate()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'rs * imm = ', rs * imm, '\n'
            registers[rt] = registers[rs] * imm
            return
        elif s.get_opcode() == 0b000111: # ORI
            logical_inst += 1
            imm = s.get_immediate()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'rs OR imm = ', rs | imm, '\n'
            registers[rt] = registers[rs] | imm
            return
        elif s.get_opcode() == 0b001001: # ANDI
            logical_inst += 1
            imm = s.get_immediate()
            rs = s.get_rs()
            rt = s.get_rt()
            registers[rt] = registers[rs] & imm
            return
        elif s.get_opcode() == 0b001011: # XORI
            logical_inst += 1
            imm = s.get_immediate()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'rs XOR imm = ', rs ^ imm, '\n'
            registers[rt] = int(registers[rs]) ^ imm
            return
        elif s.get_opcode() == 0b001100: # LDW
            mem_inst += 1
            imm = s.get_immediate()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'LDW \n'
            print 'rt: ', rt, '\n'
            print int((imm + registers[rs])/4)
            #registers[rt] = int(memory_trace[int((imm + registers[rs])/4)], 16)
            registers[rt] = int(memory_trace[int((registers[rs] + imm)/4)],16)
            return
        elif s.get_opcode() == 0b001101: # STW
            mem_inst += 1
            imm = s.get_immediate()
            rs = s.get_rs()
            rt = s.get_rt()
            print 'STW \n'
            print int((registers[rs] + imm)/4)
            print rt
            memory_trace[int((registers[rs] + imm)/4)] = registers[rt]
            return
        elif s.get_opcode() == 0b001110: # BZ
            cntrl_inst += 1
            imm = s.get_immediate()
            rs = s.get_rs()
            rt = s.get_rt()
            if registers[rs] == 0:
                counter = counter + imm - 1
                jump_flag = 1
            else:
                pass
            return
        elif s.get_opcode() == 0b001111: # BEQ
            cntrl_inst += 1
            imm = s.get_immediate()
            rs = s.get_rs()
            rt = s.get_rt()
            if registers[rs] == registers[rt]:
                counter = counter + (imm) - 1
                jump_flag = 1
            else:
                pass
            return
        elif s.get_opcode() == 0b010000: # JR
            cntrl_inst += 1
            imm = s.get_immediate()
            rs = s.get_rs()
            rt = s.get_rt()
            counter = int(registers[rs]/4)
            jump_flag = 1
            return
        elif s.get_opcode() == 0b010001: # HALT
            cntrl_inst += 1
            return

        print 'Error during execute_action() func, opcode did not match with known values\n'        
        return

    s = stage()
    file_ptr = open(filename, 'r')
    memory_trace = file_ptr.readlines()
    #memory_trace.extend(mem_extend)
    #print counter
    while not halt: # Grab a line from the memory trace
        print counter
        instruction = memory_trace[counter]
        counter += 1
        IR = instruction
        if (instruction, 16) == 0:
            break
        (opcode, rs, rt, rd, _type) = decode(instruction)
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
        execute_action(memory_trace, s)
        (instruction, opcode, rs, rt, rd, _type) = (0, 0, 0, 0, 0, '') 
        PC += 4 
        if counter == 1024:
            halt = 1
 
    print_instruction_counts()
    print 'Program Counter: ', str((counter- 1)*4), '\n'
    for i in range(len(registers)):
        print 'R' + str(i) + ':', registers[i], '\n'
    return

fn = "/Users/mattf/Desktop/trace.txt"
functional(fn)
