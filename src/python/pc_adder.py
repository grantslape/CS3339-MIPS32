<<<<<<< HEAD
#pc_adder: increment PC by 4
#input[31:0] cur_pc
#output[31:0] next_pc

import os
from myhdl import Cosimulation, always_comb

def pc_adder(cur_pc, next_pc):
	@always_comb
	def logic():
		next_pc.next = cur_pc + 0x4
	return logic

def pc_adder_v(cur_pc, next_pc):
	cmd = "iverilog -o pc_adder.out src/verilog/pc_adder.v src/verilog/tb_pc_adder_.v"
	os.system(cmd)
	
	return Cosimulation("vvp -m lib/myhdl.vpi pc_adder.out", cur_pc = cur_pc, next_pc = next_pc)

=======
import os

from myhdl import always_comb, Cosimulation


def pc_adder(cur_pc, nxt_pc):
    """
    PC Adder
    :param cur_pc: current instruction address. from program_counter
    :param nxt_pc: next sequential instruction address to pc_mux_a and if_id
    :return: module logic
    """
    # NOT IMPLEMENTED
    pass


def pc_adder_v(cur_pc, nxt_pc):
    """
    PC Adder Verilog
    :param cur_pc: current instruction address. from program_counter
    :param nxt_pc: next sequential instruction address to pc_mux_a and if_id
    :return: module logic
    """
    return Cosimulation()
>>>>>>> master
