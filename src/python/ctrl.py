"""Main Ctrl unit"""
from os import system

from myhdl import Cosimulation


def ctrl(**kwargs):
    """
    :param funct_in: from if_id.funct_out
    :param op_in: This is a MIPS op code from IF_ID
    :param jump: 1 for jump. to inst_mem_mux.jmp_ctrl, pc_mux_b.jmp_ctrl
    :param branch: activate branch unit, to id_ex.branch_in
    :param alu_op: multi-bit alu op code.  see table. to id_ex.alu_op_in
    :param mem_read: activate read from memory, to id_ex.mem_read_in
    :param mem_to_reg: 0 for Alu result writeback, 1 for data writeback. to id_ex.mem_to_reg
    :param mem_write: activate to write to memory. to id_ex
    :param alu_src: 0 for register input, 1 for immediate. to id_ex.alu_src_in
    :param reg_write: activate to write to register.  to id_ex.reg_write_in
    :param reg_dst: 0 to write to Rt ([20:16]), 1 to write to Rd ([15:11]). to id_ex.reg_dst_in
    :param reset_out: 1 to insert a 1 cycle stall in the pipeline.  to id_ex.reset_in
    :return: module logic
    """

    def logic():
        # NOT IMPLEMENTED
        pass
    return logic


def ctrl_v(**kwargs):
    """
    Verilog logic
    :param kwargs: See above.
    :return: module logic
    """
    return Cosimulation()
