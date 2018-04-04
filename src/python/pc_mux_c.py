import os

from myhdl import always_comb, Cosimulation

def pc_mux_c(pc_write, cur_pc, zero, nxt_pc):
    """
    PC Mux C
    :param pc_write: 1 to stall, from hazard_unit.pc_write
    :param cur_pc: cur_pc: current PC.  from program_counter
    :param zero: zero input for nop. subject to change
    :param nxt_pc: nxt_pc: to program_counter
    :return: module logic
    """
    # NOT IMPLEMENTED
    pass


def pc_mux_c_v(pc_write, cur_pc, zero, nxt_pc):
    """
    PC Mux C Verilog
    :param pc_write: 1 to stall, from hazard_unit.pc_write
    :param cur_pc: cur_pc: current PC.  from program_counter
    :param zero: zero input for nop. subject to change
    :param nxt_pc: nxt_pc: to program_counter
    :return: module logic
    """
    return Cosimulation()