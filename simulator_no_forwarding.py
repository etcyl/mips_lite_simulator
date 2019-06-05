from simulator import Simulator

class Simulator_no_forwarding(Simulator):
    def __init__(self):
        Simulator.__init__(self)
        # dependent table
        self.dependent_table = [0]*2
        self.dependent_table[0] = -1
        self.dependent_table[1] = -1

    # Dependent table is FIFO
    # R2 go slot 0 then R2 come out slot 1: R2 -> [_, _]
    # Next inst R3->[R2_]
    # Next inst R4->[R3, R2]
    # Next inst R5->[R4, R3]->R2

    def update_dependent(self):
        if self.branch_taken == 1:
            self.dependent_table[0] = -1
            self.dependent_table[1] = -1
            return

        # evict the second slot
        self.dependent_table[1] = -1
        # first slot -> second slot
        if self.dependent_table[0] != -1:
            self.dependent_table[1] = self.dependent_table[0]
            # clean up first slot
            self.dependent_table[0] = -1

        # first slot
        if self.type == 'r_type':
            self.dependent_table[0] = self.rd
        elif self.type == 'i_type':
            if self.name_op != 'stw':
                self.dependent_table[0] = self.rt
            pass
        else:
            pass



    def check_depedent(self):
        if self.type == 'r_type':
            if self.rs == self.dependent_table[0] or self.rt == self.dependent_table[0]:
                self.stall += 2
                return
            elif self.rs == self.dependent_table[1] or self.rt == self.dependent_table[1]:
                self.stall += 1
                return
            else:
                pass
        elif self.type == 'i_type':
            # adding the stw stall rt and rs
            if self.name_op == 'stw':
                if self.rs == self.dependent_table[0] or self.rt == self.dependent_table[0]:
                    self.stall += 2
                    return
                elif self.rs == self.dependent_table[1] or self.rt == self.dependent_table[1]:
                    self.stall += 1
                    return
                
            if self.rs == self.dependent_table[0]:
                self.stall += 2
                return
            elif self.rs == self.dependent_table[1]:
                self.stall += 1
                return
        elif self.type =='control_flow':
            # BZ
            if self.name_op == 'beq':
                if self.rs == self.dependent_table[0] or self.rt == self.dependent_table[0]:
                    self.stall += 2
                    return
                elif self.rs == self.dependent_table[1] or self.rt == self.dependent_table[1]:
                    self.stall += 1
                    return
            else:
                if self.rs == self.dependent_table[0]:
                    self.stall += 2
                    return
                elif self.rs == self.dependent_table[1]:
                    self.stall += 1
                    return
        else:
            print('error check dependent')






    def simulation(self):
        f = open(self.memory_trace)
        self.lines = f.readlines()
        self.len_file = len(self.lines)
        self.lines.extend(self.memory_extend)
        self.PC = 0
        while (self.PC < self.len_file or self.stop == 1):
            self.IF()
            if int(self.inst, 16) == 0:
                break
            self.ID()
            self.EXE()
            # check dependent table for stall
            self.check_depedent()

            # update the dependent table
            self.update_dependent()
            y=0
            self.reset_inst()

        # Final register state:
        print('\nFinal register state')
        print('Program counter: ' + str((self.PC - 1) * 4))
        for i in range(1, 13):
            print('R' + str(i) + ': ' + str(self.R[i]))

        total_instruction=self.arithmetic_inst + self.logical_inst + self.memory_inst + self.control_transfer_inst
        print('\nInstruction counts')
        print('Total number of instruction: ' + str(total_instruction))
        print('Arithmetic instructions: ' + str(self.arithmetic_inst))
        print('Logical instructions: ' + str(self.logical_inst))
        print('Memory access instructions: ' + str(self.memory_inst))
        print('Control transfer instructions: ' + str(self.control_transfer_inst))
        print('Stall_cycle: ' + str(self.stall))

        print('Without forwarding: ' + str(self.stall+total_instruction+4) + ' cycles')