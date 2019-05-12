#!/usr/bin/env python

import sys


# PC for program counter
PC = 0

# R for register
R=[0]*31




def r_type(op,rs,rt,rd):
    pass
    # R- TYPE
    #   opcode      rs	    rt	    rd	   Un-use
    #    6b         5b	    5b	    5b	    11b

def i_type(op,rs,rt,imm):
    pass
    # I- TYPE
    #   opcode      rs	    rt	    imm
    #    6b         5b	    5b	    16b


def simulator(ist):
    global PC
    for PC in range(0,len(ist)):
        #converted to hex then binary
        ist[PC]=int(ist[PC],16)
        print(bin(ist[PC]))

        # shift right to get opcode
        opcode = ist[PC]>>16

        # Decode go here

        # R-type according to opcode:
        # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
        if opcode == 0b000000 or opcode == 0b000010 or opcode == 000100  or\
            opcode == 0b00100 or opcode == 0b001010:

                #getting rs 5b by masking and shifting
                rs=ist[PC] & 0b000000000011111000000000

                r_type(opccode,)



        # I-type according to opcode:
        # ADDI: 000001, SUBI: 000011, MULI: 000101, ORI: 000111, ANDI: 001001, XORI: 001011
        # LDW: 001100, STW: 001101

        #CONTROL FLOW INSTRUCTION
        # BZ: 001110, BEQ: 001111, JR: 010000, HALT: 010001
        # SPECIAL CASE BZ, JR, HALT does not use all the field in I format








def main():

    #try:
    # Read Memory trace by lines
    with open(sys.argv[1], 'r') as my_file:
        # read line by line
        ist = my_file.read().splitlines()

    print("""MIPS simulation Enter option (1-3):\n
    1) Functional simulator only\n
    2) Functional simulator + Timing simulator assuming no pipeline forwarding\n
    3) Functional simulator + Timing simulator with pipeline forwarding\n""")

    option = input('Enter Number:')

    if int(option) ==1:
        simulator(ist)

    # except :
    #     print('Check filename again!')


if __name__ == '__main__':
    main()
