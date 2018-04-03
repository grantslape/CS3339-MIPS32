#pc_mux_b: Mux used to avoid jump stalls
#input jmp_ctrl
#input [31:0] next_inst_address
#input [31:0] jump_address
#output [31:0] next_address to pc_mux_c

import os
from myhdl import always_comb, Cosimulation

def pc_mux_b(jmp_ctrl, next_inst_address, jump_address, next_address):

	@always_comb
	def logic():
		if jmp_ctrl == 1:
			next_address.next = jump_address
		else:
			next_address.next = next_inst_address
	return logic

def pc_mux_b_v(jmp_ctrl, next_isnt_address, jump_addres, next_address):
	cmd = "iverilog -o pc_mux_b.out src/verilog/pc_mux_b.v src/verilog/tb_pc_mux_b.v"
	os.system(cmd)

	return Cosimulation("vvp -m lib/myhdl.vpi pc_mux_a.out",
			jmp_ctrl = jmp_ctrl,
			next_inst_address = next_inst_address,
			jump_address = jump_address,
			next_address = next_address)
			

