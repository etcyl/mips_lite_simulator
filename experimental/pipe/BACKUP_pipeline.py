memory_trace= "/Users/mattf/Desktop/trace.txt"
from mips_stage import stage

class simulator():
    def __init__(self):
        # R for register
        self.R = [0] * 31
        self.pipeline = [0]*5
        for i in range(len(self.pipeline)):
            self.pipeline[i] = stage()
            if i == 0:
                self.pipeline[0].set_current_action("IF")
            elif i == 1:
                self.pipeline[i].set_current_action("ID")
            elif i == 2:
                self.pipeline[i].set_current_action("EX")
            elif i == 3:
                self.pipeline[i].set_current_action("MEM")
            elif i == 4:
                self.pipeline[i].set_current_action("WB")
            print(self.pipeline[i].get_current_action())
        self.show_instruction=True

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
        f = open(memory_trace)
        self.lines = f.readlines()
        self.len_file=len(self.lines)
        self.lines.extend(self.memory_extend)
        self.PC = 0
        clock_cycle = 1
        while(self.PC<self.len_file or self.stop==1):
            if clock_cycle == 1:
                self.IF(self.pipeline[0])
            elif clock_cycle == 2:
                self.ID(self.pipeline[1])
                self.IF(self.pipeline[0])
            elif clock_cycle == 3:
                self.EXE(self.pipeline[2])
                self.ID(self.pipeline[1])
                self.IF(self.pipeline[0])
                if self.pipeline[1].get_rs() == self.pipeline[2].get_rd() or self.pipeline[1].get_rt() == self.pipeline[2].get_rd():
                    self.pipeline[1].set_stall()
            elif clock_cycle == 4:
                self.MEM(self.pipeline[3])
                if self.pipeline[1].is_stalled() == 0:
                    self.EXE(self.pipeline[2])
                    self.ID(self.pipeline[1])
                    self.IF(self.pipeline[0])
            elif clock_cycle >= 5:
                self.WB(self.pipeline[4])
                self.MEM(self.pipeline[3])
                self.EXE(self.pipeline[2])
                self.ID(self.pipeline[1])
                self.IF(self.pipeline[0])
                if self.pipeline[1].get_rs() == self.pipeline[2].get_rd() or self.pipeline[1].get_rt() == self.pipeline[2].get_rd():
                    self.pipeline[1].set_stall()
                    self.pipeline[1].set_stall()
            self.reset_inst()
            clock_cycle += 1

        # Final register state:
        print('\nFinal register state')
        print('Program counter: ' + str((self.PC-1)*4))
        for i in range(1,13):
            print('R'+str(i)+': '+str(self.R[i]))


        print('\nInstruction counts')
        print('Total number of instruction: '+str(self.arithmetic_inst+self.logical_inst+self.memory_inst+self.control_transfer_inst*2))
        print('Arithmetic instructions: '+str(self.arithmetic_inst))
        print('Logical instructions: ' + str(self.logical_inst))
        print('Memory access instructions: '+ str(self.memory_inst))
        print('Control transfer instructions: ' + str(self.control_transfer_inst*2))

    def IF(self, stage):
        self.inst=self.lines[self.PC]
        stage.set_instruction(self.inst)
        self.PC += 1

    def ID(self, stage):
        self.inst = int(str(self.inst), 16)
        # shift right to the right 5+5+5+11=26 opcode
        self.opcode = self.inst >> 26
        stage.set_opcode(self.opcode)

        # R-type according to opcode:
        # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
        if self.opcode == 0b000000 or self.opcode == 0b000010 or self.opcode == 0b000100 or \
                self.opcode == 0b000110 or self.opcode == 0b001000 or self.opcode == 0b001010:

            stage.set_type('r_type')
            stage.set_type(self.type)
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
                
            stage.set_name_op(self.name_op)
            self.decode_r_type(stage)




        # I-type according to opcode:
        # ADDI: 000001, SUBI: 000011, MULI: 000101, ORI: 000111, ANDI: 001001, XORI: 001011
        # LDW: 001100, STW: 001101
        # store type in to object

        elif self.opcode == 0b000001 or self.opcode == 0b000011 or self.opcode == 0b000101 or \
                self.opcode == 0b000111 or self.opcode == 0b001001 or self.opcode == 0b001011 or \
                self.opcode == 0b001100 or self.opcode == 0b001101:

            stage.set_type('i_type')

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

            stage.set_name_op(self.name_op)
            self.decode_i_type(stage)


            # CONTROL FLOW self.inst
            # BZ: 001110, BEQ: 001111, JR: 010000, HALT: 010001
            # SPECIAL CASE BZ, JR, HALT does not use all the field in I format
        elif self.opcode == 0b001110 or self.opcode == 0b001111 or self.opcode == 0b010000 or self.opcode == 0b0100001:
            stage.set_type('control_flow')

            if self.opcode == 0b001110:
                self.name_op = 'bz'

                # 5+5+11
                self.rs = (self.inst >> 21) & 0b00000011111
                # 21
                self.x = (self.inst) & 0b00000000000111111111111111111111
                stage.set_x(self.x)
                stage.set_rs(self.rs)

            elif self.opcode == 0b001111:
                self.name_op = 'beq'

                # 5+5+11
                self.rs = (self.inst >> 21) & 0b00000011111

                # 5+11=16 to the right
                self.rt = (self.inst >> 16) & 0b0000000000011111
                # print(bin(rt))

                self.x = (self.inst) & 0b00000001111111111111111
                # print(bin(rd))
                stage.set_x(self.x)
                stage.set_rs(self.rs)
                stage.set_rt(self.rt)
            elif self.opcode == 0b010000:
                self.name_op = 'jr'
                # 5+5+11
                self.rs = (self.inst >> 21) & 0b00000011111
                stage.set_rs(self.rs)

            elif self.opcode == 0b010001:
                self.name_op = 'halt'

            else:
                print('decode error !')
            
            stage.set_name_op(self.name_op)

    def decode_r_type(self, stage):
        # getting rs 5b by masking and shifting
        # 5+5+11=21 to the rght
        self.rs = (self.inst >> 21) & 0b00000011111
        stage.set_rs(self.rs)
        # print(bin(rs))

        # 5+11=16 to the right
        self.rt = (self.inst >> 16) & 0b0000000000011111
        # print(bin(rt))
        stage.set_rt(self.rt)
        # 11
        self.rd = (self.inst >> 11) & 0b000000000000000011111
        # print(bin(rd))
        stage.set_rd(self.rd)

    def decode_i_type(self, stage):
        # 5+5+11=21 to the right
        self.rs = (self.inst >> 21) & 0b00000011111
        # print(bin(self.rs))
        stage.set_rs(self.rs)

        # 5+11=16 to the right
        self.rt = (self.inst >> 16) & 0b0000000000011111
        # print(bin(self.rt))
        stage.set_rt(self.rt)

        # sign imm converter
        imm = (self.inst) & 0b00000001111111111111111
        sign = imm >> 15

        if sign == 0b1:
            self.imm = BitArray(bin=bin(imm)).int
        else:
            self.imm = imm

        stage.set_immediate(self.imm)

    # EXE
    def EXE(self, stage):
        if stage.get_type() == 'r_type':
            self.exe_r_type(stage)
        elif stage.get_type() == 'i_type':
            self.exe_i_type(stage)
        elif stage.type() == 'control_flow':
            self.exe_control_flow(stage)

    def exe_control_flow(self, stage):
        if stage.get_name_op() == 'bz':
            if self.show_instruction:
                print('BZ' + ' R' + str(stage.get_rs()) + ', ' + str(stage.get_x()))
            if self.R[stage.get_rs()] == 0:
                self.PC = stage.get_x() + self.PC - 1
                self.control_transfer_inst += 1

        elif stage.get_name_op() == 'beq':
            if self.show_instruction:
                print('BEQ' + ' R' + str(stage.get_rs()) + ', ' + ' R' + str(stage.get_rt()) + ', ' + str(stage.get_x()))
            if self.R[stage.get_rs()] == self.R[stage.get_rt()]:
                self.PC = stage.get_x() + self.PC - 1
                self.control_transfer_inst += 1

        elif stage.get_name_op() == 'jr':
            self.control_transfer_inst += 1
            if self.show_instruction:
                print('JR' + ' R' + str(stage.get_rs()))
            self.PC = int(self.R[stage.get_rs()] / 4)

        elif stage.get_name_op() == 'halt':
            stage.set_stop()
            if self.show_instruction:
                print('HALT')

            self.control_transfer_inst += 1

    def exe_r_type(self, stage):
        # R-type according to opcode:
        # ADD: 000000, SUB: 000010, MUL: 000100, OR: 000110, AND: 001000, XOR: 001010
        #   opcode      rs	    rt	    rd	   Un-use
        #    6b         5b	    5b	    5b	    11b
        # ADD
        if stage.get_name_op() == 'add':
            stage.set_ALU_result(self.R[stage.get_rs()] + self.R[stage.get_rt()])
            #self.R[stage.get_rd()]= self.R[stage.get_rs()] + self.R[stage.get_rt()]
            if self.show_instruction:
                print('ADD R' + str(stage.get_rd()) + ',' + ' R' + str(stage.get_rs()) + ', R' + str(stage.get_rt()))
            self.arithmetic_inst += 1

        # SUB
        elif stage.get_name_op() == 'sub':
            stage.set_ALU_result(self.R[stage.get_rs()] - self.R[stage.get_rt()])
            #self.R[stage.get_rd()] = self.R[stage.get_rs()] - self.R[stage.get_rt()]
            if self.show_instruction:
                print('SUB R' + str(stage.get_rd()) + ',' + ' R' + str(stage.get_rs()) + ', R' + str(stage.get_rt()))
            self.arithmetic_inst += 1
            
        # MUL
        elif stage.get_name_op() == 'mul':
            stage.set_ALU_result(self.R[stage.get_rs()] * self.R[stage.get_rt()])
            #self.R[stage.get_rd()] = self.R[stage.get_rs()] * self.R[stage.get_rt()]
            if self.show_instruction:
                print('MUL R' + str(stage.get_rd()) + ',' * ' R' + str(stage.get_rs()) + ', R' + str(stage.get_rt()))
            self.arithmetic_inst += 1
       
        # OR
        elif stage.get_name_op() == 'or':
            stage.set_ALU_result(self.R[stage.get_rs()] | self.R[stage.get_rt()])
            #self.R[stage.get_rd()] = self.R[stage.get_rs()] | self.R[stage.get_rt()]
            if self.show_instruction:
                print('OR R' + str(stage.get_rd()) + ',' '|' ' R' + str(stage.get_rs()) + ', R' + str(stage.get_rt()))
            self.logical_inst += 1
        
        # AND
        elif stage.get_name_op() == 'and':
            stage.set_ALU_result(self.R[stage.get_rs()] & self.R[stage.get_rt()])
            #self.R[stage.get_rd()] = self.R[stage.get_rs()] & self.R[stage.get_rt()]
            if self.show_instruction:
                print('AND R' + str(stage.get_rd()) + ',' '&' ' R' + str(stage.get_rs()) + ', R' + str(stage.get_rt()))
            self.logical_inst += 1
        
        # XOR
        elif stage.get_name_op() == 'xor':
            stage.set_ALU_result(self.R[stage.get_rs()] ^ self.R[stage.get_rt()])
            #self.R[stage.get_rd()] = self.R[stage.get_rs()] ^ self.R[stage.get_rt()]
            if self.show_instruction:
                print('XOR R' + str(stage.get_rd()) + ',' '^' ' R' + str(stage.get_rs()) + ', R' + str(stage.get_rt()))
            self.logical_inst += 1
        else:
            print('exe r_type error')

        # EXE i_type

    def exe_i_type(self, stage):
        # I-type according to opcode:
        # ADDI: 000001, SUBI: 000011, MULI: 000101, ORI: 000111, ANDI: 001001, XORI: 001011
        # LDW: 001100, STW: 001101
        # I- TYPE
        #   opcode      rs	    rt	    imm
        #    6b         5b	    5b	    16b
        # ADDI
        rt = stage.get_rt()
        rs = stage.get_rs()
        imm = stage.get_imm()
        if stage.get_name_op() == 'addi':
            stage.set_ALU_result(self.R[rs] + imm)
            #self.R[rt] = self.R[rs] + imm
            if self.show_instruction:
                print('ADDI R' + str(rt) + ', R' + str(rs) + ', ' + str(imm))
            self.arithmetic_inst += 1
        # SUBI
        elif stage.get_name_op() == 'subi':
            stage.set_ALU_result(self.R[rs] - imm)
            #self.R[rt] = self.R[rs] - imm
            if self.show_instruction:
                print('SUBI R' + str(rt) + ', R' + str(rs) + ', ' + str(imm))
            self.arithmetic_inst += 1
        # MULI
        elif stage.get_name_op() == 'muli':
            stage.set_ALU_result(self.R[rs] * imm)
            #self.R[rt] = self.R[rs] * imm
            if self.show_instruction:
                print('MULI R' + str(rt) + ', R' + str(rs) + ', ' + str(imm))
            self.arithmetic_inst += 1
        # ORI
        elif stage.get_name_op() == 'ori':
            stage.set_ALU_result(self.R[rs] | imm)
            #self.R[rt] = self.R[rs] | imm
            if self.show_instruction:
                print('ORI R' + str(rt) + ', R' + str(rs) + ', ' + str(imm))
            self.logical_inst += 1
        # ANDI
        elif stage.get_name_op() == 'andi':
            stage.set_ALU_result(self.R[rs] & imm)
            #self.R[rt] = self.R[rs] & imm
            if self.show_instruction:
                print('ANDI R' + str(rt) + ', R' + str(rs) + ', ' + str(imm))
            self.logical_inst += 1
        # XORI
        elif stage.get_name_op() == 'xori':
            stage.set_ALU_result(int(self.R[rs]) ^ imm)
            #self.R[rt] = int(self.R[rs]) ^ imm
            if self.show_instruction:
                print('XORI R' + str(rt) + ', R' + str(rs) + ', ' + str(imm))
            self.logical_inst += 1

        # LDW
        elif stage.get_name_op() == 'ldw':
            # load value of addressing store in self.R[self.rs] + imm is the base into self.R[self.rt]
            stage.set_ALU_result(int(((self.R[rs] + imm)/4), 16))
            #self.R[rt] = int(self.lines[int((self.R[rs] + imm)/4)],16)
            if self.show_instruction:
                print('LDW ' + 'R' + str(rt) + ', R' + str(rs) + ', ' + str(imm))
            self.memory_inst += 1
        # STW
        elif stage.get_name_op() == 'stw':
            stage.set_ALU_result(int((self.R[rs] + imm)/4))
            #self.lines[int((self.R[rs] + imm)/4)] = self.R[rt]
            if self.show_instruction:
                print('STW ' + 'R' + str(rt) + ', R' + str(rs) + ', ' + str(imm))
            else:
                print('Address: ' + str(imm) + ', Contents: ' + str(self.R[rt]))
            self.memory_inst += 1
        else:
            print('error exe')

    def MEM(self, stage):
        if stage.get_name_op() == 'ldw':
            # load value of addressing store in self.R[self.rs] + imm is the base into self.R[self.rt]
            stage.set_MEM_result(int(self.lines[stage.get_ALU_result()]))
            #self.R[stage.get_rt()] = int(self.lines[int((self.R[stage.get_rs()] + stage.get_imm())/4)],16)
            if self.show_instruction:
                print('LDW ' + 'R' + str(stage.get_rt()) + ', R' + str(stage.get_rs()) + ', ' + str(stage.get_imm()))
            self.memory_inst += 1
        # STW
        elif stage.get_name_op() == 'stw':
            self.lines[stage.get_ALU_result()] = self.R[stage.get_rt()]
            if self.show_instruction:
                print('STW ' + 'R' + str(stage.get_rt()) + ', R' + str(stage.get_rs()) + ', ' + str(stage.get_imm()))
            else:
                print('Address: ' + str(stage.get_imm()) + ', Contents: ' + str(self.R[stage.get_rt()]))
            self.memory_inst += 1
        else:
            pass#print('error exe') # Pass on Arithmetic and Logic instructions since no Memory stage action is required

    def WB(self, stage):
        if stage.get_name_op() == 'stw': # No action necessary for Store instructions during the Writeback stage
            pass
        else:
            if stage.get_name_op() == 'ldw':
                 self.R[stage.get_rt()] = stage.get_MEM_result()
            elif stage.get_type == 'r-type':
                self.R[stage.get_rd()] = stage.get_ALU_result()
            else:
                self.R[stage.get_rt()] = stage.get_ALU_result()
