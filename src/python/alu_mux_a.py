import os

from myhdl import always_comb, Cosimulation


def alu_mux_a(forward_a, r_data1, mem_rd, wb_rd, op1_out):
    """
    3:1 Mux for forwarding results from 2 cycles ago
    :param forward_a: forward_a: two bit input selector from fwd_unit
    :param r_data1: rs data received from id_ex
    :param mem_rd: rd from the previous cycle, received from ex_mem
    :param wb_rd: rd from two cycles ago, received from wb_mux
    :param op1_out: Output for Rs/Op1.  Sent to ALU
    :return: module logic
    """
    # NOT IMPLEMENTED
    pass


def alu_mux_a_v(forward_a, r_data1, mem_rd, wb_rd, op1_out):
    """
    3:1 Mux for forwarding results from 2 cycles ago Verilog
    :param forward_a: forward_a: two bit input selector from fwd_unit
    :param r_data1: rs data received from id_ex
    :param mem_rd: rd from the previous cycle, received from ex_mem
    :param wb_rd: rd from two cycles ago, received from wb_mux
    :param op1_out: Output for Rs/Op1.  Sent to ALU
    :return: module logic
    """
    return Cosimulation()
