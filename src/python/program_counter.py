import os

from myhdl import always_seq, Cosimulation


def program_counter(clock, nxt_inst, cur_pc):
    """
    Program Counter
    :param clock: system clock
    :param nxt_inst: next instruction address from pc_mux_b
    :param cur_pc: next instruction address goes to inst_mem, pc_mux_c
    :return: module logic
    """
    # NOT IMPLEMENTED
    pass


def program_counter_v(clock, nxt_inst, cur_pc):
    """
    Program Counter Verilog
    :param clock: system clock
    :param nxt_inst: next instruction address from pc_mux_b
    :param cur_pc: next instruction address goes to inst_mem, pc_mux_c
    :return: module logic
    """
    return Cosimulation()
