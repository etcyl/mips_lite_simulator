#!/usr/bin/env python
# https://www.eg.bucknell.edu/~csci320/mips_web/

import sys


# PC for program counter
PC = 0

# R for register
R=[0]*31




def r_type(op,rs,rt,rd):
    # R-type according to opcode:
    # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
    #   opcode      rs	    rt	    rd	   Un-use
    #    6b         5b	    5b	    5b	    11b

    # ADD
    if op == 0b000000:

        R[rd] = R[rs] + R[rt]
        print('ADD R'+str(rd)+','+' R'+str(rs)+', R'+str(rt))
        
    # SUB    
    elif op == 0b000010:
        
        R[rd] = R[rs] - R[rt]
        print('SUB R'+str(rd)+','-' R'+str(rs)+', R'+str(rt))
        
    # MUL
    elif op == 0b000100:
        
        R[rd] = R[rs] * R[rt]
        print('MUL R'+str(rd)+','*' R'+str(rs)+', R'+str(rt))
        
    # OR
    elif op == 0b000110:
        
        R[rd] = R[rs] | R[rt]
        print('OR R'+str(rd)+','|' R'+str(rs)+', R'+str(rt))
        
    # AND
    elif op == 0b001000:
        
        R[rd] = R[rs] & R[rt]
        print('AND R'+str(rd)+','&' R'+str(rs)+', R'+str(rt))
        
     # XOR
    elif op == 0b001010:
        
        R[rd] = R[rs] ^ R[rt]
        print('XOR R'+str(rd)+','^' R'+str(rs)+', R'+str(rt))     
    
    else:
        print('r_type opcode error: default case used instead')
  
        

def i_type(op,rs,rt,imm):
    # I-type according to opcode:
    # ADDI: 000001, SUBI: 000011, MULI: 000101, ORI: 000111, ANDI: 001001, XORI: 001011
    # LDW: 001100, STW: 001101
    # I- TYPE
    #   opcode      rs	    rt	    imm
    #    6b         5b	    5b	    16b

    # ADDI
    if op == 0b000001:

        R[rd] = int(R[rs]) + int(R[rt])
        print('ADDI R'+str(rd)+','+' R'+str(rs)+', R'+str(rt))
        
    # SUBI    
    elif op == 0b000011:
        
        R[rd] = int(R[rs]) - int(R[rt])
        print('SUBI R'+str(rd)+','-' R'+str(rs)+', R'+str(rt))
        
    # MULI
    elif op == 0b000101:
        
        R[rd] = int(R[rs]) * int(R[rt])
        print('MULI R'+str(rd)+','*' R'+str(rs)+', R'+str(rt))
        
    # ORI
    elif op == 0b000111:
        
        R[rd] = int(R[rs]) | int(R[rt])
        print('ORI R'+str(rd)+','|' R'+str(rs)+', R'+str(rt))
        
    # ANDI
    elif op == 0b001001:
        
        R[rd] = int(R[rs]) & int(R[rt])
        print('ANDI R'+str(rd)+','&' R'+str(rs)+', R'+str(rt))
        
     # XORI
    elif op == 0b001011:
        
        R[rd] = R[rs] ^ R[rt]
        print('XORI R'+str(rd)+','^' R'+str(rs)+', R'+str(rt))     
    
    else:
        print('I_type opcode error: default case used instead')


def simulator(ist):
    global PC
    for PC in range(0,len(ist)):
        #converted to hex then binary
        ist[PC]=int(ist[PC],16)
        print(bin(ist[PC]))

        # R- TYPE
        #   opcode      rs	    rt	    rd	   Un-use
        #    6b         5b	    5b	    5b	    11b
        # I- TYPE
        #   opcode      rs	    rt	    imm
        #    6b         5b	    5b	    16b

        # shift right to the right 5+5+5+11=26 opcode
        opcode = ist[PC]>>26


        # Decode go here

        # R-type according to opcode:
        # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
        if opcode == 0b000000 or opcode == 0b000010 or opcode == 0b000100  or\
           opcode == 0b00100 or opcode == 0b001010:
            #getting rs 5b by masking and shifting

            print('opcode ='+bin(opcode))
            # 5+5+11=21 to the rght
            rs= (ist[PC]>>21) & 0b00000011111
            #print(bin(rs))

            # 5+11=16 to the right
            rt=(ist[PC]>>16) & 0b0000000000011111
            #print(bin(rt))

            # 11
            rd=(ist[PC]>>11) & 0b000000000000000011111
            #print(bin(rd))


            r_type(opcode,rs,rt,rd)





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
