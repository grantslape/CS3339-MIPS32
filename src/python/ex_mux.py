import os

from myhdl import always_comb, Cosimulation


def ex_mux(reg_dst, rt_in, rd_in, dest):
    """
    2:1 Mux to select write address
    :param reg_dst: 1 bit selector from id_ex.reg_dst_out
    :param rt_in: rt, sent from id_ex
    :param rd_in: rd, sent from id_ex
    :param dest: destination register address, sent to ex_mem
    :return: module logic
    """

    @always_comb
    def logic():
        pass
        # NOT IMPLEMENTED
    return logic


def ex_mux_v(reg_dst, rt_in, rd_in, dest):
    """
    2:1 Mux to select write address Verilog
    :param reg_dst: 1 bit selector from id_ex.reg_dst_out
    :param rt_in: rt, sent from id_ex
    :param rd_in: rd, sent from id_ex
    :param dest: destination register address, sent to ex_mem
    :return: module logic
    """
    return Cosimulation()
