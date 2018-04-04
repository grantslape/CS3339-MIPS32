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
