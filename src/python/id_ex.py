"""ID/EX Pipeline register"""
import os
from myhdl import always_seq, Cosimulation


# YOU NEED TO INSTANTIATE WITH KEYWORD ARGUMENTS
def id_ex(clock, **kwargs):
    """
    ID/EX Pipeline Register
    :param branch_in:
    :param alu_op:
    :param mem_read_in:
    :param mem_to_reg_in:
    :param mem_write_in:
    :param reg_dst_in:
    :param top4_in:
    :param r_data1:
    :param r_data2:
    :param rs:
    :param rt:
    :param rd:
    :param imm:
    :param r_data1_out:
    :param r_data2_out:
    :param imm_out:
    :param rs_out:
    :param rt_out:
    :param rd_out:
    :param top4_out:
    :param branch_out:
    :param alu_op_out:
    :param mem_read_out:
    :param mem_write_out:
    :param alu_src_out:
    :param reg_write_out:
    :param reg_dst_out:
    :return: module logic
    """
    def logic():
        # NOT IMPLEMENTED
        pass
    return logic

# YOU NEED TO INSTANTIATE WITH KEYWORD ARGUMENTS
def id_ex_v(clock, **kwargs):
    """ See above, Verilog"""
    return Cosimulation()
