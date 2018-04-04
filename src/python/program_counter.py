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
