#!/usr/bin/env python

import sys


# PC for program counter
PC = 0

# R for register
R=[0]*31




def r-type(op,rs,rt,rd):

    # R- TYPE
    #   opcode      rs	    rt	    rd	   Un-use
    #    6b         5b	    5b	    5b	    5b 6b

def i-type(op,rs,rt,imm)

    # I- TYPE
    #   opcode      rs	    rt	    imm
    #    6b         5b	    5b	    16b


def simulator(ist):
    global PC
    for PC in range(0,len(ist)):
        #converted to int then binary

        print(bin(int(ist[PC])))


        # R-type according to opcode:
        # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010

        # I-type according to opcode:
        # ADDI: 000001, SUBI: 000011, MULI: 000101, ORI: 000111, ANDI: 001001, XORI: 001011
        # LDW: 001100, STW: 001101

        #CONTROL FLOW INSTRUCTION
        # BZ: 001110, BEQ: 001111, JR: 010000, HALT: 010001
        # SPECIAL CASE BZ, JR, HALT does not use all the field in I format





        # Decode go here


def main():

    try:
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

    except IOError:
        print('Check filename again!')


if __name__ == '__main__':
    main()