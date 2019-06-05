
# https://stackoverflow.com/questions/42397772/converting-binary-representation-to-signed-64-bit-integer-in-python

#
# >>> from bitstring import BitArray
# >>> s = '1000010101010111010101010101010101010101010101010111010101010101'
# >>> BitArray(bin=s).int
# -8838501918699063979

from bitstring import BitArray


class Simulator:
    def __init__(self):
        self.memory_trace = ''
        # R for register
        self.R = [0] * 31

        self.show_instruction= True

        #memory extend
        self.memory_extend = [0]*1000

        self.PC =0
        self.stop=0
        self.clock_cycle=0
        self.arithmetic_inst = 0
        self.logical_inst = 0
        self.memory_inst=0
        self.control_transfer_inst=0


        self.lines=0
        self.len_file=0


        self.stall=0
        self.branch_taken=0


        #each instruction
        self.opcode=0
        self.name_op=''
        self.inst =0
        self.type=''
        self.rs=0
        self.rd=0
        self.rt=0
        self.imm=0
        self.x=0
        


    def reset_inst(self):
        # each instruction
        self.opcode = 0
        self.inst=0
        self.name_op = ''
        self.type = ''
        self.rs = 0
        self.rd = 0
        self.rt = 0
        self.imm = 0
        self.x = 0

    def simulation(self):
        f = open(self.memory_trace)
        self.lines = f.readlines()
        self.len_file=len(self.lines)
        self.lines.extend(self.memory_extend)
        self.PC=0
        while(self.PC<self.len_file and self.stop != 1):
            self.IF()
            #if int(self.inst,16)==0:
            #    break
            self.ID()
            self.EXE()
            self.reset_inst()

        # Final register state:
        print('\nFinal register state')
        print('Program counter: ' + str((self.PC-1)*4))
        for i in range(0,31):
            print('R'+str(i)+': '+str(self.R[i]))


        print('\nInstruction counts')
        print('Total number of instruction: '+str(self.arithmetic_inst+self.logical_inst+self.memory_inst+self.control_transfer_inst))
        print('Arithmetic instructions: '+str(self.arithmetic_inst))
        print('Logical instructions: ' + str(self.logical_inst))
        print('Memory access instructions: '+ str(self.memory_inst))
        print('Control transfer instructions: ' + str(self.control_transfer_inst))




    def IF(self):
        self.inst=self.lines[self.PC]
        self.PC += 1

    def ID(self):
        self.inst = int(str(self.inst), 16)
        # shift right to the right 5+5+5+11=26 opcode
        self.opcode = self.inst >> 26

        # R-type according to opcode:
        # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
        if self.opcode == 0b000000 or self.opcode == 0b000010 or self.opcode == 0b000100 or \
                self.opcode == 0b000110 or self.opcode == 0b001000 or self.opcode == 0b001010:

            self.type='r_type'
            # store type in to object

            if self.opcode == 0b000000:
                self.name_op = 'add'

            elif self.opcode == 0b000010:
                self.name_op = 'sub'

            elif self.opcode == 0b000100:
                self.name_op = 'mul'

            elif self.opcode == 0b000110:
                self.name_op = 'or'

            elif self.opcode == 0b001000:
                self.name_op = 'and'

            elif self.opcode == 0b001010:
                self.name_op = 'xor'
                

            self.decode_r_type()




        # I-type according to opcode:
        # ADDI: 000001, SUBI: 000011, MULI: 000101, ORI: 000111, ANDI: 001001, XORI: 001011
        # LDW: 001100, STW: 001101
        # store type in to object

        elif self.opcode == 0b000001 or self.opcode == 0b000011 or self.opcode == 0b000101 or \
                self.opcode == 0b000111 or self.opcode == 0b001001 or self.opcode == 0b001011 or \
                self.opcode == 0b001100 or self.opcode == 0b001101:

            self.type = 'i_type'

            if self.opcode == 0b000001:
                self.name_op = 'addi'

            elif self.opcode == 0b000011:
                self.name_op = 'subi'

            elif self.opcode == 0b000101:
                self.name_op = 'muli'

            elif self.opcode == 0b000111:
                self.name_op = 'ori'

            elif self.opcode == 0b001001:
                self.name_op = 'andi'

            elif self.opcode == 0b001011:
                self.name_op = 'xori'

            elif self.opcode == 0b001100:
                self.name_op = 'ldw'

            elif self.opcode == 0b001101:
                self.name_op = 'stw'

            else:
                print('decode error !')

            self.decode_i_type()


            # CONTROL FLOW self.inst
            # BZ: 001110, BEQ: 001111, JR: 010000, HALT: 010001
            # SPECIAL CASE BZ, JR, HALT does not use all the field in I format
        elif self.opcode == 0b001110 or self.opcode == 0b001111 or self.opcode == 0b010000 or self.opcode == 0b010001:
            self.type = 'control_flow'

            if self.opcode == 0b001110:
                self.name_op = 'bz'

                # 5+5+11
                self.rs = (self.inst >> 21) & 0b00000011111
                # 21
                self.x = (self.inst) & 0b00000000000111111111111111111111

            elif self.opcode == 0b001111:
                self.name_op = 'beq'

                # 5+5+11
                self.rs = (self.inst >> 21) & 0b00000011111

                # 5+11=16 to the right
                self.rt = (self.inst >> 16) & 0b0000000000011111
                # print(bin(rt))

                self.x = (self.inst) & 0b00000001111111111111111
                # print(bin(rd))

            elif self.opcode == 0b010000:
                self.name_op = 'jr'
                # 5+5+11
                self.rs = (self.inst >> 21) & 0b00000011111

            elif self.opcode == 0b010001:
                self.name_op = 'halt'

            else:
                print('decode error !')
            


    def decode_r_type(self):
        # getting rs 5b by masking and shifting
        # 5+5+11=21 to the rght
        self.rs = (self.inst >> 21) & 0b00000011111

        # print(bin(rs))

        # 5+11=16 to the right
        self.rt = (self.inst >> 16) & 0b0000000000011111
        # print(bin(rt))

        # 11
        self.rd = (self.inst >> 11) & 0b000000000000000011111
        # print(bin(rd))

    def decode_i_type(self):
        # 5+5+11=21 to the right
        self.rs = (self.inst >> 21) & 0b00000011111
        # print(bin(self.rs))

        # 5+11=16 to the right
        self.rt = (self.inst >> 16) & 0b0000000000011111
        # print(bin(self.rt))

        # sign imm converter
        imm = (self.inst) & 0b00000001111111111111111
        sign = imm >> 15

        if sign == 0b1:
            self.imm = BitArray(bin=bin(imm)).int
        else:
            self.imm = imm

    # EXE
    def EXE(self):
        if self.type == 'r_type':
            self.exe_r_type()
        elif self.type == 'i_type':
            self.exe_i_type()
        elif self.type == 'control_flow':
            self.exe_control_flow()

    def exe_control_flow(self):
        # sign imm converter

        sign = self.x >> 15

        if sign == 0b1:
            self.x = BitArray(bin=bin(self.x)).int
        else:
            pass

        if self.name_op == 'bz':
            self.control_transfer_inst += 1
            if self.show_instruction:
                print('BZ' + ' R' + str(self.rs) + ', ' + str(self.x))
            if self.R[self.rs] == 0:
                self.PC = self.x + self.PC - 1
                self.stall += 2

        elif self.name_op == 'beq':
            self.control_transfer_inst += 1
            if self.show_instruction:
                print('BEQ' + ' R' + str(self.rs) + ', ' + ' R' + str(self.rt) + ', ' + str(self.x))
            if self.R[self.rs] == self.R[self.rt]:
                self.PC = self.x + self.PC - 1
                self.stall += 2


        elif self.name_op == 'jr':
            self.control_transfer_inst += 1
            self.stall += 2
            if self.show_instruction:
                print('JR' + ' R' + str(self.rs))
            self.PC = int(self.R[self.rs] / 4)

        elif self.name_op == 'halt':
            self.control_transfer_inst += 1
            self.stop = 1
            if self.show_instruction:
                print('HALT')



    def exe_r_type(self):
        # R-type according to opcode:
        # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
        #   opcode      rs	    rt	    rd	   Un-use
        #    6b         5b	    5b	    5b	    11b
        # ADD
        if self.name_op == 'add':
            self.R[self.rd]= self.R[self.rs] + self.R[self.rt]
            if self.show_instruction:
                print('ADD R' + str(self.rd) + ',' + ' R' + str(self.rs) + ', R' + str(self.rt))
            self.arithmetic_inst += 1



        # SUB
        elif self.name_op == 'sub':
            self.R[self.rd] = self.R[self.rs] - self.R[self.rt]
            if self.show_instruction:
                print('SUB R' + str(self.rd) + ',' + ' R' + str(self.rs) + ', R' + str(self.rt))
            self.arithmetic_inst += 1
            
        # MUL
        elif self.name_op == 'mul':
            self.R[self.rd] = self.R[self.rs] * self.R[self.rt]
            if self.show_instruction:
                print('MUL R' + str(self.rd) + ',' + ' R' + str(self.rs) + ', R' + str(self.rt))
            self.arithmetic_inst += 1
        # OR
        elif self.name_op == 'or':
            self.R[self.rd] = self.R[self.rs] | self.R[self.rt]
            if self.show_instruction:
                print('OR R' + str(self.rd) + ',' + ' R' + str(self.rs) + ', R' + str(self.rt))
            self.logical_inst += 1
        # AND
        elif self.name_op == 'and':
            self.R[self.rd] = self.R[self.rs] & self.R[self.rt]
            if self.show_instruction:
                print('AND R' + str(self.rd) + ',' '&' ' R' + str(self.rs) + ', R' + str(self.rt))
            self.logical_inst += 1
        # XOR
        elif self.name_op == 'xor':
            self.R[self.rd] = self.R[self.rs] ^ self.R[self.rt]
            if self.show_instruction:
                print('XOR R' + str(self.rd) + ',' '^' ' R' + str(self.rs) + ', R' + str(self.rt))
            self.logical_inst += 1
        else:
            print('exe r_type error')

        # EXE i_type

    def exe_i_type(self):
        # I-type according to opcode:
        # ADDI: 000001, SUBI: 000011, MULI: 000101, ORI: 000111, ANDI: 001001, XORI: 001011
        # LDW: 001100, STW: 001101
        # I- TYPE
        #   opcode      rs	    rt	    imm
        #    6b         5b	    5b	    16b
        # ADDI
        rt = self.rt
        rs = self.rs
        imm = self.imm
        if self.name_op == 'addi':
            self.R[self.rt] = self.R[self.rs] + self.imm
            if self.show_instruction:
                print('ADDI R' + str(self.rt) + ', R' + str(self.rs) + ', ' + str(self.imm))
            self.arithmetic_inst += 1
        # SUBI
        elif self.name_op == 'subi':
            self.R[self.rt] = self.R[self.rs] - self.imm
            if self.show_instruction:
                print('SUBI R' + str(self.rt) + ', R' + str(self.rs) + ', ' + str(self.imm))
            self.arithmetic_inst += 1
        # MULI
        elif self.name_op == 'muli':
            self.R[self.rt] = self.R[self.rs] * self.imm
            if self.show_instruction:
                print('MULI R' + str(self.rt) + ', R' + str(self.rs) + ', ' + str(self.imm))
            self.arithmetic_inst += 1
        # ORI
        elif self.name_op == 'ori':
            self.R[self.rt] = self.R[self.rs] | self.imm
            if self.show_instruction:
                print('ORI R' + str(self.rt) + ', R' + str(self.rs) + ', ' + str(self.imm))
            self.logical_inst += 1
        # ANDI
        elif self.name_op == 'andi':
            self.R[self.rt] = self.R[self.rs] & self.imm
            if self.show_instruction:
                print('ANDI R' + str(self.rt) + ', R' + str(self.rs) + ', ' + str(self.imm))
            self.logical_inst += 1
        # XORI
        elif self.name_op == 'xori':
            self.R[self.rt] = int(self.R[self.rs]) ^ self.imm
            if self.show_instruction:
                print('XORI R' + str(self.rt) + ', R' + str(self.rs) + ', ' + str(self.imm))
            self.logical_inst += 1

        # LDW
        elif self.name_op == 'ldw':
            # load value of addressing store in self.R[self.rs] + imm is the base into self.R[self.rt]
            self.R[self.rt] = int(self.lines[int((self.R[self.rs] + imm)/4)],16)
            if self.show_instruction:
                print('LDW ' + 'R' + str(self.rt) + ', R' + str(self.rs) + ', ' + str(self.imm))
            self.memory_inst += 1
        # STW
        elif self.name_op == 'stw':
            self.lines[int((self.R[self.rs] + self.imm)/4)] = self.R[self.rt]
            if self.show_instruction:
                print('STW ' + 'R' + str(self.rt) + ', R' + str(self.rs) + ', ' + str(self.imm))
            else:
                print('Address: ' + str(self.imm) + ', Contents: ' + str(self.R[self.rt]))
            self.memory_inst += 1
        else:
            print('error exe')



        



