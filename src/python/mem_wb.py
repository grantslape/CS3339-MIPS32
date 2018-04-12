"""MEM/WB Pipline Register"""
import os
from myhdl import always, Cosimulation


def mem_wb(clock, reg_write_in, rdata_in, result_in, rt_in, rdata_out, result_out, rt_out,
           reg_write_out):
    """
    Memory/Writeback pipeline register
    :param clock:
    :param reg_write_in:
    :param rdata_in:
    :param result_in:
    :param rt_in:
    :param rdata_out:
    :param result_out:
    :param rt_out:
    :param reg_write_out:
    :return:
    """
    @always
    def logic():
        # NOT IMPLEMENTED
        pass
    return logic


def mem_wb_v(clock, reg_write_in, rdata_in, result_in, rt_in, rdata_out, result_out, rt_out,
           reg_write_out):
    """
    Memory/Writeback pipeline register
    see above for docs
    """
    return Cosimulation()