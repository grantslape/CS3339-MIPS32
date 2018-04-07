import os

from myhdl import always_comb, Cosimulation


def alu_mux_a(forward_a, r_data1, mem_rd, wb_rd, op1_out):
    """
    3:1 Mux for forwarding results from 2 cycles ago
    :param forward_a: forward_a: two bit input selector from fwd_unit
    :param r_data1: rs data received from id_ex 0
    :param mem_rd: rd from the previous cycle, received from ex_mem 01
    :param wb_rd: rd from two cycles ago, received from wb_mux 10
    :param op1_out: Output for Rs/Op1.  Sent to ALU
    :return: module logic
    """

    @always_comb
    def logic():
      if forward_a == 2:
      	#the data source is the ex/mem pipeline register mem_rd
	    	op1_out = mem_rd;
      elif forward_a == 1:
         #the data source is the mem/wb pipeline register wb_rd
         op1_out = wb_rd;
      else:
         #the data source is the id/ex pipeline register r_data1
         op1_out = r_data1;
    return logic


def alu_mux_a_v(forward_a, r_data1, mem_rd, wb_rd, op1_out):
    """
    3:1 Mux for forwarding results from 2 cycles ago Verilog
    :param forward_a: forward_a: two bit input selector from fwd_unit
    :param r_data1: rs data received from id_ex 0
    :param mem_rd: rd from the previous cycle, received from ex_mem 01
    :param wb_rd: rd from two cycles ago, received from wb_mux 10
    :param op1_out: Output for Rs/Op1.  Sent to ALU
    :return: module logic
    """

    cmd = "iverilog -o alu_mux_a.out src/verilog/alu_mux_a.v src/verilog/alu_mux_a_tb.v"
    os.system(cmd)
    return Cosimulation("vvp -m  lib/myhdl.vpi alu_mux_a.out",
		         forward_a = forward_a,
			 r_data1 = r_data1,
			 mem_rd = mem_rd,
			 wb_rd = wb_rd,
			 op1_out = op1_out)
