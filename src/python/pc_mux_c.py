#pc_mux_c: Mux for stalling
#input pc_write: 1 to stall (hazard)
#input[31:0] cur_pc: Current instruction address
#input zero: zero for nop
#output [31:0] next_pc:

import os
from myhdl import Cosimulation, always_comb

def pc_mux_c(pc_write, cur_pc, zero, next_pc):
	@always_comb
	def logic():
		if pc_write == 1:
			next_pc.next = zero
		else:
			next_pc.next = cur_pc
	return logic

def pc_mux_c_v(pc_write, cur_pc, zero, next_pc):
	cmd = "iverilog -o pc_mux_c.out src/verilog/pc_mux_c.v src/verilog/tb_pc_mux_c.v"
	os.system(cmd)

	return Cosimulation("vvp -m lib/myhdl.vpi pc_mux_c.out",
			pc_write = pc_write,
			cur_pc = cur_pc,
			zero = zero,
			next_pc = next_pc)
