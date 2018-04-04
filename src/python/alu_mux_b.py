import os

from myhdl import always_comb, Cosimulation


def alu_mux_b(forward_b, r_data2, mem_rd, wb_rd, op2_out):
    """
    3:1 Mux for forwarding results from 2 cycles ago
    :param forward_b: forward_b: two bit input selector from fwd_unit
    :param r_data2: rt data received from id_ex 0
    :param mem_rd: rd from the previous cycle, received from ex_mem 01
    :param wb_rd: rd from two cycles ago, received from wb_mux 10
    :param op2_out: Output for Rs/Op1.  Sent to ALU 
    :return: module logic
    """
    # NOT IMPLEMENTED
    pass


def alu_mux_b_v(forward_b, r_data2, mem_rd, wb_rd, op2_out):
    """
    3:1 Mux for forwarding results from 2 cycles ago Verilog
    :param forward_b: forward_b: two bit input selector from fwd_unit
    :param r_data2: rt data received from id_ex 0
    :param mem_rd: rd from the previous cycle, received from ex_mem 01
    :param wb_rd: rd from two cycles ago, received from wb_mux 10
    :param op2_out: Output for Rt/Op2.  Sent to ALU
    :return: module logic
    """
    return Cosimulation()
