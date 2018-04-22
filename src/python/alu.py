import os
from myhdl import *


def alu(op_1, op_2, alu_op,z,result):
    """
        alu: The main ALU
        input [31:0] op_1: a 32 bit operand.  from alu_mux_1
        input [31:0] op_2: a 32 bit operand.  from alu_mux_imm
        input [3:0] alu_op: The 4-bit ALU op code.  See  OpCode table.
        output [31:0] result: a 32 bit result of operation.  to ex_mem
        output z: Zero flag.  to ex_mem
    """
    
    @always_comb 
    def logic():
        if(alu_op == 1):
	     result.next = op_1.signed() + op_2.signed()
        elif(alu_op == 2):
            result.next = op_1.signed() - op_2.signed()
        elif(alu_op == 3):
            result.next = op_1 ^ op_2
        elif(alu_op == 4):
            result.next = op_1 | op_2
        elif(alu_op == 5):
            result.next = op_1 & op_2
        elif(alu_op == 8):
            result.next = ~(op_1 | op_2)
        elif(alu_op == 9):
            if(op_1.signed() < op_2.signed()):
               result.next = 1
            else:
               result.next = 0

    @always_comb
    def zero_detect():
        if result.next == 0:
            z.next = 1
        else:
            z.next = 0

    return logic, zero_detect


def alu_v(op_1, op_2, alu_op, z, result):

    cmd = "iverilog -o bin/alu.out src/verilog/alu.v src/verilog/alu_tb.v"
    os.system(cmd)
    return Cosimulation("vvp -m  lib/myhdl.vpi bin/alu.out",
                         op_1=op_1,
                         op_2=op_2,
                         alu_op=alu_op,
                         z=z,
                         result=result)
