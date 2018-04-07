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
		else:
			cur_pc.next = cur_pc
	return seq_logic

def program_counter_v(clock, pc_write, nxt_inst, cur_pc):
	cmd = "iverilog -o program_counter_v.out src/verilog/program_counter.v src/verilog/program_counter_tb.v"
	os.system(cmd)
	
	return Cosimulation("vvp -m lib/myhdl.vpi program_counter.out", 
			clock = clock,
			pc_write = pc_write,
			nxt_inst = nxt_inst,
			cur_pc=cur_pc)
