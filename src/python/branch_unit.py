import os
from myhdl import always_comb, Cosimulation


def branch_unit(branch_ctrl, zero_in, pc_src):
    """
    Branch Unit
    :param branch_ctrl: Branch control signal.  from fwd_unit
    :param zero_in: zero flag.  From ex_mem.z_out
    :param pc_src: pc ctrl signal.  to pc_mux_a.pc_src
    :return: module logic
    """
    def logic():
        # NOT IMPLEMENTED
        pass
    return logic


def branch_unit_v(branch_ctrl, zero_in, pc_src):
    """See above, Verilog"""
    return Cosimulation()
