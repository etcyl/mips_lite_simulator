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
        self.rs = 0
        self.rd = 0
        self.rt = 0
        self.immediate = 0
        self.type = "NONE"
        self.current_action = "NOOP" # This will be IF, ID, EX, MEM, or WB; NULL means no instruction is being used

    def set_current_action(self, stage):
        self.current_action = str(stage)

    def get_current_action(self):
        return self.current_action

    def set_instruction(self, instruction):
        self.instruction = int(instruction, 2)

    def get_instruction(self):
        return self.instruction

    def set_opcode(self, opcode):
        self.opcode = opcode

    def get_opcode(self):
        return self.opcode

    def get_rs(self):
        return self.source

    def set_rs(self, rs):
        self.rs = rs

    def get_rd(self):
        return self.rd

    def set_rd(self, rd):
        self.rd = rd

    def get_rt(self):
        return self.rt

    def set_rt(self, rt):
        self.rt = rt

    def set_immediate(self, immediate):
        self.immediate = immediate
    
    def get_immediate(self):
        return self.immediate
    
    def get_type(self):
        return self.type

    def set_type(self, _type):
        self.type = _type
