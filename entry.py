
class entry():
    def __init__(self):
        self.type =''
        self.name_op=''
        self.opcode = 0
        self.rd = 0
        self.rs = 0
        self.x=0
        self.rt = 0
        self.imm = 0
        self.stage = 0
        self.inst = 0

        # feeding PC to this line
        self.line=-1

        # brach.taken
        # 0  is not taken
        # 1 is taken
        self.branch_taken = 0

        # stone done is already
        # stall 1 is done stalling
        # stall 0 is not done stalling
        self.stall_done=0

        # stop the program
        self.stop=0

    def reset(self):
        self.type = ''
        self.name_op = ''
        self.opcode = 0
        self.rd = 0
        self.rs = 0
        self.x = 0
        self.rt = 0
        self.imm = 0
        self.stage = 0
        self.inst = 0


        # feeding PC to this line
        self.line=-1

        # brach.taken
        # 0  is not taken
        # 1 is taken
        self.branch_taken = 0

        # stone done is already
        # stall 1 is done stalling
        # stall 0 is not done stalling
        self.stall_done = 0

        # stop the program
        self.stop = 0
