<<<<<<< HEAD
#input clock: system clock
#input [31:0] next_instruction
#output [31:0] cur_pc: next instruction address

import os
from myhdl import Cosimulation, always

def program_counter(clock, pc_write, nxt_inst, cur_pc):
	
	@always(clock.posedge)
	def seq_logic():
		if pc_write == 0:
			cur_pc.next = nxt_inst
			pc_reg = nxt_inst
			
	return seq_logic

def program_counter_v(clock, reset, nxt_inst, cur_pc):
	cmd = "iverilog -o program_counter_v.out src/verilog/program_counter.v src/verilog/tb_program_counter.v"
	os.system(cmd)
	
	return Cosimulation("vvp -m lib/myhdl.vpi program_counter.out", 
			clock = clock,
			reset = rest,
			nxt_inst = nxt_inst,
			cur_pc=cur_pc)
=======
import os

from myhdl import always_seq, Cosimulation


def program_counter(clock, pc_write, nxt_inst, cur_pc):
    """
    Program Counter
    :param clock: system clock
    :param pc_write: 1 to stall (repeat instruction), from hazard_unit.pc_write
    :param nxt_inst: next instruction address from pc_mux_b
    :param cur_pc: next instruction address goes to inst_mem, pc_mux_c
    :return: module logic
    """
    # NOT IMPLEMENTED
    pass


def program_counter_v(clock, pc_write, nxt_inst, cur_pc):
    """
    Program Counter Verilog
    :param clock: system clock
    :param pc_write: 1 to stall (repeat instruction), from hazard_unit.pc_write
    :param nxt_inst: next instruction address from pc_mux_b
    :param cur_pc: next instruction address goes to inst_mem, pc_mux_c
    :return: module logic
    """
    return Cosimulation()
>>>>>>> master
