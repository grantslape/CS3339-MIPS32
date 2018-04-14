import os
from myhdl import always_comb, Cosimulation


def branch_adder(pc_in, imm_in, addr_out):
    """
    calculate addresses for branches
    :param pc_in: PC+4.  from id_ex
    :param imm_in: 32 bit immediate from shift_unit
    :param addr_out: 32 bit jump address. to ex_mem
    :return: module logic
    """

    @always_comb
    def logic():
        # NOT IMPLEMENTED
        pass
    return logic


def branch_adder_v(pc_in, imm_in, addr_out):
    """
    calculate addresses for branches verilog
    :param pc_in:
    :param imm_in:
    :param addr_out:
    :return:
    """
    return Cosimulation()
