#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 16 21:04:14 2019

@author: mattf
"""

class stage():
    """A stage class is used in a MIPS pipeline"""
    # The class accepts an instruction and performs subsequent actions such as:
    # IF: Instruction Fetch
    # ID: Instruction Decode
    # EX: Execute
    # MEM: Memory access
    # Writeback: WB
    def __init__(self):
        self.opcode = 0
        self.source = 0
        self.dest = 0
        self.current_action = 'NULL' # This will be IF, ID, EX, MEM, or WB; NULL means no instruction is being used

    def set_current_action(self, stage):
        self.current_action = str(stage)

    def get_current_action(self):
        return self.current_action

    def set_instruction(self, instruction):
        self.instruction = int(instruction, 2)


    def get_instruction(self):
        return self.instruction

    def get_source(self):
        return self.source

    def set_source(self, source):
        self.source = source

    def get_dest(self):
        return self.dest

    def set_dest(self, dest):
        self.dest = dest

    def set_opcode(self, opcode):
        self.opcode = opcode

    def get_opcode(self):
        return self.opcode
