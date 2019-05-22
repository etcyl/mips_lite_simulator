#!/usr/bin/env python
# https://www.eg.bucknell.edu/~csci320/mips_web/

from mips_stage import stage
import sys

# Debugger mode list representing the program
prog_lst = [0xFFFFFFFF, # First program instruction
            0x00853000] # Second program instruction

# Number of stages in the MIPS Lite ISA
num_stages = 5

def r_type(op, rs, rt, rd):
    # R-type according to opcode:
    # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
    #   opcode      rs	    rt	    rd	   Un-use
    #    6b         5b	    5b	    5b	    11b

    # ADD
    if op == 0b000000:

        R[rd] = R[rs] + R[rt]
        print('ADD R' + str(rd) + ',' + ' R' + str(rs) + ', R' + str(rt))

    # SUB
    elif op == 0b000010:

        R[rd] = R[rs] - R[rt]
        print('SUB R' + str(rd) + ',' - ' R' + str(rs) + ', R' + str(rt))

    # MUL
    elif op == 0b000100:

        R[rd] = R[rs] * R[rt]
        print('MUL R' + str(rd) + ',' * ' R' + str(rs) + ', R' + str(rt))

    # OR
    elif op == 0b000110:

        R[rd] = R[rs] | R[rt]
        print('OR R' + str(rd) + ',' '|' ' R' + str(rs) + ', R' + str(rt))

    # AND
    elif op == 0b001000:

        R[rd] = R[rs] & R[rt]
        print('AND R' + str(rd) + ',' '&' ' R' + str(rs) + ', R' + str(rt))

    # XOR
    elif op == 0b001010:

        R[rd] = R[rs] ^ R[rt]
        print('XOR R' + str(rd) + ',' '^' ' R' + str(rs) + ', R' + str(rt))

    else:
        print('r_type opcode error: default case used instead')


def i_type(op, rs, rt, rd):
    # I-type according to opcode:
    # ADDI: 000001, SUBI: 000011, MULI: 000101, ORI: 000111, ANDI: 001001, XORI: 001011
    # LDW: 001100, STW: 001101
    # I- TYPE
    #   opcode      rs	    rt	    imm
    #    6b         5b	    5b	    16b
    # ADDI
    if op == 0b000001:
        R[rd] = int(R[rs]) + int(R[rt])
        print('ADDI R' + str(rd) + ',' '+' ' R' + str(rs) + ', R' + str(rt))
    # SUBI
    elif op == 0b000011:
        R[rd] = int(R[rs]) - int(R[rt])
        print('SUBI R' + str(rd) + ',' '-' ' R' + str(rs) + ', R' + str(rt))
    # MULI
    elif op == 0b000101:
        R[rd] = int(R[rs]) * int(R[rt])
        print('MULI R' + str(rd) + ',' '*' ' R' + str(rs) + ', R' + str(rt))
    # ORI
    elif op == 0b000111:
        R[rd] = int(R[rs]) | int(R[rt])
        print('ORI R' + str(rd) + ',' '|' ' R' + str(rs) + ', R' + str(rt))
    # ANDI
    elif op == 0b001001:
        R[rd] = int(R[rs]) & int(R[rt])
        print('ANDI R' + str(rd) + ',' '&' ' R' + str(rs) + ', R' + str(rt))
    # XORI
    elif op == 0b001011:
        R[rd] = int(R[rs]) ^ int(R[rt])
        print('XORI R' + str(rd) + ',' '^' ' R' + str(rs) + ', R' + str(rt))
    # Default exception case
    else:
        print('I_type opcode error: default case used instead')


def decode(instruction):
    # shift right to the right 5+5+5+11=26 opcode
    opcode = instruction >> 26

    # R-type according to opcode:
    # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
    if opcode == 0b000000 or opcode == 0b000010 or opcode == 0b000100 or \
            opcode == 0b00100 or opcode == 0b001010:
        # getting rs 5b by masking and shifting

        print('opcode =' + bin(opcode))
        # 5+5+11=21 to the rght
        rs = (instruction >> 21) & 0b00000011111
        # print(bin(rs))

        # 5+11=16 to the right
        rt = (instruction >> 16) & 0b0000000000011111
        # print(bin(rt))

        # 11
        rd = (instruction >> 11) & 0b000000000000000011111
        # print(bin(rd))
        
        _type = "R-type"

        return (opcode, rs, rt, rd, _type)
    else:
        return (1, 1, 1, 1, "ERROR")

def simulator(ist):
    global PC
    for PC in range(0, len(ist)):
        # converted to hex then binary
        ist[PC] = int(ist[PC], 16)
        print(bin(ist[PC]))

        # R- TYPE
        #   opcode      rs	    rt	    rd	   Un-use
        #    6b         5b	    5b	    5b	    11b
        # I- TYPE
        #   opcode      rs	    rt	    imm
        #    6b         5b	    5b	    16b

        # shift right to the right 5+5+5+11=26 opcode
        opcode = ist[PC] >> 26

        # Decode go here

        # R-type according to opcode:
        # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
        if opcode == 0b000000 or opcode == 0b000010 or opcode == 0b000100 or \
                opcode == 0b00100 or opcode == 0b001010:
            # getting rs 5b by masking and shifting

            print('opcode =' + bin(opcode))
            # 5+5+11=21 to the rght
            rs = (ist[PC] >> 21) & 0b00000011111
            # print(bin(rs))

            # 5+11=16 to the right
            rt = (ist[PC] >> 16) & 0b0000000000011111
            # print(bin(rt))

            # 11
            rd = (ist[PC] >> 11) & 0b000000000000000011111
            # print(bin(rd))

            r_type(opcode, rs, rt, rd)

        # I-type according to opcode:
        # ADDI: 000001, SUBI: 000011, MULI: 000101, ORI: 000111, ANDI: 001001, XORI: 001011
        # LDW: 001100, STW: 001101

        # CONTROL FLOW INSTRUCTION
        # BZ: 001110, BEQ: 001111, JR: 010000, HALT: 010001
        # SPECIAL CASE BZ, JR, HALT does not use all the field in I format

def is_r_type(opcode, ist, PC):
    if opcode == 0b000000 or opcode == 0b000010 or opcode == 0b000100 or \
            opcode == 0b00100 or opcode == 0b001010:
        # getting rs 5b by masking and shifting

        print('opcode =' + bin(opcode))
        # 5+5+11=21 to the rght
        rs = (ist[PC] >> 21) & 0b00000011111
        # print(bin(rs))

        # 5+11=16 to the right
        rt = (ist[PC] >> 16) & 0b0000000000011111
        # print(bin(rt))

        # 11
        rd = (ist[PC] >> 11) & 0b000000000000000011111
        # print(bin(rd))

        return (rs, rt, rd)
    else:
        return -1

def debug_functional(ist):
    global PC
    PC = 0

    for PC in range(0, len(ist)):
        # converted to hex then binary
        ist[PC] = int(ist[PC])
        print(bin(ist[PC]))

        # R- TYPE
        #   opcode      rs	    rt	    rd	   Un-use
        #    6b         5b	    5b	    5b	    11b
        # I- TYPE
        #   opcode      rs	    rt	    imm
        #    6b         5b	    5b	    16b

        # shift right to the right 5+5+5+11=26 opcode
        opcode = ist[PC] >> 26

        # Decode go here

        # R-type according to opcode:
        # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
        if opcode == 0b000000 or opcode == 0b000010 or opcode == 0b000100 or \
                opcode == 0b00100 or opcode == 0b001010:
            # getting rs 5b by masking and shifting

            print('opcode =' + bin(opcode))
            # 5+5+11=21 to the rght
            rs = (ist[PC] >> 21) & 0b00000011111
            # print(bin(rs))

            # 5+11=16 to the right
            rt = (ist[PC] >> 16) & 0b0000000000011111
            # print(bin(rt))

            # 11
            rd = (ist[PC] >> 11) & 0b000000000000000011111
            # print(bin(rd))

            r_type(opcode, rs, rt, rd)

        # I-type according to opcode:
        # ADDI: 000001, SUBI: 000011, MULI: 000101, ORI: 000111, ANDI: 001001, XORI: 001011
        # LDW: 001100, STW: 001101

        # CONTROL FLOW INSTRUCTION
        # BZ: 001110, BEQ: 001111, JR: 010000, HALT: 010001
        # SPECIAL CASE BZ, JR, HALT does not use all the field in I format

def memory_trace_reader(filename):
    return 

def pipeline(memory_trace):
    # Total number of instructions and a breakdown of instruction frequencies for the following instruction types:
    # Arithmetic, Logical, Memory Access, Control Transfer
    total_instructions = 0
    arithmetic_inst = 0  # Number of arithmetic instructions
    arithmetic_freq = 0
    logical_inst = 0
    logical_freq = 0
    mem_inst = 0
    mem_freq = 0
    cntrl_inst = 0
    cntrl_freq = 0
 
    def memory_trace_reader(filename):
        f_ptr = open(filename, 'r')
        mem = f_ptr.read().splitlines()
        for i in range(len(mem)):
            mem[i] = int(mem[i], 16)
            mem[i] = bin(mem[i])
        return mem
    
    def print_frequencies():
        print("Frequency of arithmetic instruction:\n", arithmetic_freq)
        print("Frequency of logical instruction:\n", logical_freq)
        print("Frequency of memory instruction:\n", mem_freq)
        print("Frequency of control instruction:\n", cntrl_freq)
        return
    
    def set_frequencies():
        if arithmetic_inst >= 1 and total_instructions >= 1:
            arithmetic_freq = float(arithmetic_inst) / float(total_instructions)
        elif arithmetic_inst == 0:
            pass
        else:
            print('error setting arithmetic freq: total_instructions == 0')
            return

        if logical_inst >= 1:
            logical_freq = float(logical_inst) / float(total_instructions)

        if mem_inst >= 1:
            mem_freq = float(mem_inst) / float(total_instructions)

        if cntrl_inst >= 1:
            cntrl_freq = float(cntrl_inst) / float(total_instructions)

        print('Frequencies of different instructions calculated...')
        print_frequencies()
        return
    
    def execute_action(stage):
        return

    def memory_action(stage):
        return
    
    def writeback(stage):
        return    

    """
    The MIPS pipelined execution is as follows:
        Clock
        Cycle   1   2   3   4   5   6   7   --> Time
        I_j     IF  ID  EX  MEM WB
        I_j+1       IF  ID  EX  MEM WB
        I_j+2           IF  ID  EX  MEM WB
    Here, the pipeline is abstracted as a list in Python of length equal to the number of stages.
    Since the MIPS Lite pipeline has 5 stages this means the pipeline list contains 5 elements.
    """
    global PC
    global IR
    PC = 0 # Set the Program Counter to 0
    counter = 0
    halt = 0
    init = 1
    s = stage()
    pipe = [s]*num_stages
    print("Memory trace:", memory_trace, "\n")
    print("Stage class:" ,s, "\n")
    print("Pipeline:", pipe, "\n")
    while not halt: # Grab a line from the memory trace
        instruction = bin(memory_trace[counter])
        print("Instruction is:", instruction)
        # Update the pipeline
        for i in range(len(pipe)):
            if(init): # This will only be true if it's the very first instruction
                init = 0
                pipe[0].set_current_action("IF")
                pipe[0].set_instruction(instruction)
                IR = instruction
                PC += 4
                counter += 1
            else:
                if pipe[i].get_current_action() == "IF":
                    pipe[i].set_current_action("ID")
                    pipe[i].get_instruction()
                    instruction_format = decode(instruction)
                    if instruction_format[-1] == "R-type":
                        (opcode, rs, rt, rd, _type) = instruction_format
                        pipe[i].set_opcode(opcode)
                        pipe[i].set_rs(rs)
                        pipe[i].set_rt(rt)
                        pipe[i].set_rd(rd)
                        pipe[i].set_type(_type)
                    elif instruction_format[-1] == "I-type":
                        (opcode, rs, rt, immediate, _type) = instruction_format
                        pipe[i].set_opcode(opcode)
                        pipe[i].set_rs(rs)
                        pipe[i].set_rt(rt)
                        pipe[i].set_immediate(immediate)
                        pipe[i].set_type(_type)
                    else:
                        print("ERROR decoding")
                elif pipe[i].get_current_action() == "ID":
                    pipe[i].set_current_action("EX")
                    # Perform the ALU operation, either a memory reference, a register to register action, 
                    # register to immediate action, or branch
                    execute_action(pipe[i])
                elif pipe[i].get_current_action() == "EX":
                    pipe[i].set_current_action("MEM")
                    memory_action(pipe[i])
                elif pipe[i].get_current_action() == "MEM":
                    pipe[i].set_curent_action("WB")
                    writeback(pipe[i])
                elif pipe[i].get_current_action() == "NOOP":
                    pass
                else:
                    print("ERROR looping over pipeline, invalid stage state detected")
                
    print("Memory trace finished...\n")
    set_frequencies() 
    return pipe
    
def main():
    # Read Memory trace by lines
    print("""MIPS simulation Enter option (1-4):\n
    1) Functional simulator only\n
    2) Functional simulator + Timing simulator assuming no pipeline forwarding\n
    3) Functional simulator + Timing simulator with pipeline forwarding\n
    4) Functional simulator debug mode (list of instructions)\n""") # Pass a list of instructions to test

    option = input('Enter Number:')

    if int(option) == 1:
        with open(sys.argv[1], 'r') as my_file:
            # read line by line
            print("Functional simulator selected ...\n")
            ist = my_file.read().splitlines()
            simulator(ist)
    elif int(option) == 2:
        print("Functional simulator + Timing simulator assuming no pipeline forwarding selected...\n")
        p = pipeline(prog_lst)
        return p
    elif int(option) == 3:
        print("Functional simulator + Timing simulator with pipeline forwarding selected...\n")
    elif int(option) == 4:
        debug_functional(prog_lst)

if __name__ == '__main__':
    _p = main()
    print(_p)
    for i in range(len(_p)): # Print the stages of the pipeline
        print("Stage #", i, "currently performing:", _p[i].get_current_action())
