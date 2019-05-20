from entry import entry
from bitstring import BitArray



memory_file='memory.txt'

PC_global=0
stall=00

# R for register
R = [0] * 31


memory=[100000000000]

arithmetic_inst=0
logical_inst=0

def do_stage(entry_list,i):
    if entry_list[i].stage==1:
        IF(entry_list,i)
    elif entry_list[i].stage==2:
        ID(entry_list,i)
    elif entry_list[i].stage==3:
        EXE(entry_list,i)
    elif entry_list[i].stage==4:
        pass
    elif entry_list[i].stage == 5:
        entry_list[i].reset()






def check_stage(entry_list,i):
    if entry_list[i].stage == 0 and entry_list[i].line >= 0:
        entry_list[i].stage =1
        do_stage(entry_list,i)
    elif entry_list[i].stage == 1:
        entry_list[i].stage = 2
        do_stage(entry_list, i)
    elif entry_list[i].stage == 2:
        entry_list[i].stage = 3
        do_stage(entry_list, i)
    elif entry_list[i].stage == 3:
        entry_list[i].stage = 4
        do_stage(entry_list, i)
    elif entry_list[i].stage == 4:
        entry_list[i].stage = 5
        do_stage(entry_list, i)







def IF(entry_list,i):
    f=open(memory_file)
    lines=f.readlines()
    entry_list[i].inst=lines[entry_list[i].line]





# ID passing entry_list[i].inst
def ID(entry_list,i):
    entry_list[i].inst = int(entry_list[i].inst,16)
    #print(bin(entry_list[i].inst))

    # shift right to the right 5+5+5+11=26 opcode
    entry_list[i].opcode = entry_list[i].inst >> 26
    opcode = entry_list[i].opcode




    # R-type according to opcode:
    # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
    if opcode == 0b000000 or opcode == 0b000010 or opcode == 0b000100 or \
            opcode == 0b000110 or opcode==0b001000 or opcode == 0b001010:
        # store type in to object
        entry_list[i].type='r_type'
        decode_r_type(entry_list,i)

        if opcode == 0b000000:
            entry_list[i].name_op='add'

        elif opcode == 0b000010:
            entry_list[i].name_op='sub'

        elif opcode == 0b000100:
            entry_list[i].name_op='mul'

        elif opcode == 0b000110:
            entry_list[i].name_op='or'

        elif opcode == 0b001000:
            entry_list[i].name_op='and'

        elif opcode == 0b001010:
            entry_list[i].name_op='xor'

        decode_i_type(entry_list, i)








    # I-type according to opcode:
    # ADDI: 000001, SUBI: 000011, MULI: 000101, ORI: 000111, ANDI: 001001, XORI: 001011
    # LDW: 001100, STW: 001101
    # store type in to object

    elif opcode == 0b000001 or opcode == 0b000011 or opcode == 0b000101 or \
            opcode == 0b000111 or opcode == 0b001001 or opcode == 0b001011 or \
            opcode == 0b001100 or opcode == 0b001101 :

        entry_list[i].type = 'i_type'

        if opcode == 0b000001:
            entry_list[i].name_op = 'addi'

        elif opcode == 0b000011:
            entry_list[i].name_op = 'subi'

        elif opcode == 0b000101:
            entry_list[i].name_op = 'muli'

        elif opcode == 0b000111:
            entry_list[i].name_op = 'ori'

        elif opcode == 0b001001:
            entry_list[i].name_op = 'andi'

        elif opcode == 0b001011:
            entry_list[i].name_op = 'xori'

        elif opcode == 0b001100:
            entry_list[i].name_op = 'ldw'

        elif opcode == 0b001101:
            entry_list[i].name_op = 'stw'

        else:
            print('decode error !')


        decode_i_type(entry_list,i)

        # CONTROL FLOW entry_list[i].inst
        # BZ: 001110, BEQ: 001111, JR: 010000, HALT: 010001
        # SPECIAL CASE BZ, JR, HALT does not use all the field in I format
    elif opcode == 0b001110 or  opcode == 0b001111 or opcode == 0b010000 or opcode== 0b0100001:
        entry_list[i].type = 'control_flow'

        if opcode == 0b001110:
            entry_list[i].name_op ='bz'

            # 5+5+11
            entry_list[i].rs = (entry_list[i].inst >> 21) & 0b00000011111
            # 21
            entry_list[i].x = (entry_list[i].inst) & 0b00000000000111111111111111111111

        elif opcode ==0b001111:
            entry_list[i].name_op ='beq'

            # 5+5+11
            entry_list[i].rs = (entry_list[i].inst >> 21) & 0b00000011111

            # 5+11=16 to the right
            entry_list[i].rt = (entry_list[i].inst >> 16) & 0b0000000000011111
            # print(bin(rt))

            entry_list[i].x = (entry_list[i].inst) & 0b00000001111111111111111
            # print(bin(rd))

        elif opcode == 0b010000:
            entry[i].name_op = 'jr'
            # 5+5+11
            entry_list[i].rs = (entry_list[i].inst >> 21) & 0b00000011111

        elif opcode == 0b010001:
            entry[i].name_op = 'halt'



        else:
            print('decode error !')




def decode_r_type(entry_list,i):
    # getting rs 5b by masking and shifting
    # 5+5+11=21 to the rght
    entry_list[i].rs = (entry_list[i].inst >> 21) & 0b00000011111

    #print(bin(rs))

    # 5+11=16 to the right
    entry_list[i].rt = (entry_list[i].inst >> 16) & 0b0000000000011111
    #print(bin(rt))

    # 11
    entry_list[i].rd = (entry_list[i].inst >> 11) & 0b000000000000000011111
    #print(bin(rd))


def decode_i_type(entry_list,i):
    # 5+5+11=21 to the rght
    entry_list[i].rs = (entry_list[i].inst >> 21) & 0b00000011111
    #print(bin(entry_list[i].rs))

    # 5+11=16 to the right
    entry_list[i].rt = (entry_list[i].inst >> 16) & 0b0000000000011111
    #print(bin(entry_list[i].rt))


    #sign imm converter
    imm=(entry_list[i].inst) & 0b00000001111111111111111

    entry_list[i].imm = BitArray(bin=bin(imm)).int
    #print(entry_list[i].imm)
    #print(bin(entry_list[i].imm))


# EXE
def EXE(entry_list,i):
    if entry_list[i].type=='r_type':
        exe_r_type(entry_list,i)
    elif entry_list[i].type=='i_type':
        exe_i_type(entry_list,i)
    elif entry_list[i].type=='control_flow':
        exe_control_flow(entry_list,i)

def exe_control_flow(entry_list,i):
    global PC_global
    rt=entry_list[i].rt
    rs=entry_list[i].rs
    x=entry_list[i].x

    if  entry_list[i].name_op == 'bz':
        print('BZ' + ' R'+ str(rt)+ ', '+str(x))
        if R[rs] == 0:
            entry[i].branch_taken= 1
            PC_global=x

    elif entry_list[i].name_op == 'beq':
        print('BEQ' + ' R' + str(rs) + ', ' + ' R' + str(rt) + ', ' + str(x))
        if R[rs] == R[rt]:
            entry_list[i].branch_taken = 1
            PC_global=x
    elif entry_list[i].name_op == 'jr':
        print('JR' + ' R' + str(rs) )
        entry_list[i].branch_taken = 1
        PC_global=R[rs]
    elif entry_list[i].name_op =='halt':
        entry_list[i].stop=1





def exe_r_type(entry_list, i):
    global arithmetic_inst, logical_inst
    # R-type according to opcode:
    # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
    #   opcode      rs	    rt	    rd	   Un-use
    #    6b         5b	    5b	    5b	    11b
    # ADD
    rd=entry_list[i].rd
    rs=entry_list[i].rs
    rt=entry_list[i].rt
    if entry_list[i].name_op == 'add':
        R[rd] = R[rs] + R[rt]
        print('ADD R' + str(rd)+ ',' + ' R' + str(rs) + ', R' + str(rt))
        arithmetic_inst += 1

    # SUB
    elif entry_list[i].name_op=='sub':
        R[rd] = R[rs] - R[rt]
        print('SUB R' + str(rd) + ',' - ' R' + str(rs) + ', R' + str(rt))
        arithmetic_inst += 1
    # MUL
    elif entry_list[i].name_op == 'mul':
        R[rd] = R[rs] * R[rt]
        print('MUL R' + str(rd) + ',' * ' R' + str(rs) + ', R' + str(rt))
        arithmetic_inst += 1
    # OR
    elif entry_list[i].name_op == 'or':
        R[rd] = R[rs] | R[rt]
        print('OR R' + str(rd) + ',' '|' ' R' + str(rs) + ', R' + str(rt))
        logical_inst += 1
    # AND
    elif entry_list[i].name_op == 'and':
        R[rd] = R[rs] & R[rt]
        print('AND R' + str(rd) + ',' '&' ' R' + str(rs) + ', R' + str(rt))
        logical_inst += 1
    # XOR
    elif entry_list[i].name_op == 'xor':
        R[rd] = R[rs] ^ R[rt]
        print('XOR R' + str(rd) + ',' '^' ' R' + str(rs) + ', R' + str(rt))
        logical_inst += 1
    else:
        print('exe r_type error')

    # EXE i_type
def exe_i_type(entry_list,i):
    global arithmetic_inst, logical_inst
    # I-type according to opcode:
    # ADDI: 000001, SUBI: 000011, MULI: 000101, ORI: 000111, ANDI: 001001, XORI: 001011
    # LDW: 001100, STW: 001101
    # I- TYPE
    #   opcode      rs	    rt	    imm
    #    6b         5b	    5b	    16b
    # ADDI
    rt=entry_list[i].rt
    rs=entry_list[i].rs
    imm=entry_list[i].imm
    if entry_list[i].name_op == 'addi':
        R[rt] = R[rs] + imm
        print('ADDI R' + str(rt) + ', R' + str(rs) +', '+ str(imm))
        arithmetic_inst += 1
    # SUBI
    elif entry_list[i].name_op == 'subi':
        R[rt] = R[rs] - imm
        print('SUBI R' + str(rt) + ', R' + str(rs) +', '+ str(imm))
        arithmetic_inst += 1
    # MULI
    elif entry_list[i].name_op == 'muli':
        R[rt] = R[rs] * imm
        print('MULI R' + str(rt) + ', R' + str(rs) +', '+ str(imm))
        arithmetic_inst += 1
    # ORI
    elif entry_list[i].name_op == 'ori':
        R[rt] = R[rs] | imm
        print('ORI R' + str(rt) + ', R' + str(rs) +', '+ str(imm))
        logical_inst += 1
    # ANDI
    elif entry_list[i].name_op == 'andi':
        R[rt] = R[rs] & imm
        print('ANDI R' + str(rt) + ', R' + str(rs) +', '+ str(imm))
        arithmetic_inst += 1
    # XORI
    elif entry_list[i].name_op == 'xori':
        R[rt] = int(R[rs]) ^ imm
        print('XORI R' + str(rt) + ', R' + str(rs) +', '+ str(imm))
        logical_inst += 1

    #LDW
    elif entry_list[i].name_op == 'ldw':
        # load value of addressing store in R[rs] + imm is the base into R[rt]
        print('LDW ' + 'R' + str(rt) + ', R' + str(rs) + ', ' + str(imm))
        R[rt] = memory[R[rs]+ imm]
        logical_inst += 1
    #LDW
    elif entry_list[i].name_op == 'stw':
        print('XORI ' + 'R' + str(rt) + ', R' + str(rs) + ', ' + str(imm))
        memory[R[rs]+imm]= R[rt]
        logical_inst += 1
    else:
        print('error exe')

def main():
    entry_list = [entry() for i in range(5)]
    entry_list = [entry() for i in range(5)]

    entry_list[1].reset()
    entry_list[1].line = 8

    PC_global=0
    while(PC_global!=100):
        if entry_list[1].stage==0:
            entry_list[1].line=PC_global
            check_stage(entry_list, 1)
            check_stage(entry_list, 1)
            check_stage(entry_list, 1)
            check_stage(entry_list, 1)
            check_stage(entry_list, 1)
        PC_global+=1



if __name__ == '__main__':
    main()
