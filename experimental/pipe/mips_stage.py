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
        self.instruction = 0
        self.opcode = 0
        self.rs = 0
        self.x = 0
        self.rd = 0
        self.rt = 0
        self.immediate = 0
        self.name_op = ""
        self.type = "NONE"
        self.stall = 0 # Stall due to Read-After-Write (RAW) dependency 
        self.halt = 0 # Halt due to decoding halt opcode
        self.current_action = "NOOP" # This will be IF, ID, EX, MEM, or WB; NOOP means no instruction is being used
        self.ALU_result = 0
        self.MEM_result = 0 

    def set_halt(self):
        self.halt = 1
        
    def clear_halt(self):
        self.halt = 0

    def set_stall(self):
        self.stall = 1

    def clear_stall(self):
        self.stall = 0

    def is_stalled(self):
        return self.stall

    def set_current_action(self, stage):
        self.current_action = str(stage)

    def get_current_action(self):
        return self.current_action

    def set_instruction(self, instruction):
        self.instruction = instruction

    def get_instruction(self):
        return self.instruction

    def set_opcode(self, opcode):
        self.opcode = opcode

    def get_opcode(self):
        return self.opcode

    def get_rs(self):
        return self.rs

    def get_x(self):
        return self.x
    
    def set_x(self, x):
        self.x = x
    
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

    def set_imm(self, immediate):
        self.immediate = immediate
    
    def get_imm(self):
        return self.immediate
    
    def get_type(self):
        return self.type

    def set_type(self, _type):
        self.type = _type

    def set_name_op(self, name):
        self.name_op = name

    def get_name_op(self):
        return self.name_op
    
    def get_ALU_result(self):
        return self.ALU_result
    
    def set_ALU_result(self, result):
        self.ALU_result = result

    def get_MEM_result(self):
        return self.MEM_result
    
    def set_MEM_result(self, result):
        self.MEM_result = result