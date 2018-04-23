"""EX/MEM Pipeline register"""
import os
from myhdl import always, Cosimulation


# YOU NEED TO INSTANTIATE WITH KEYWORD ARGUMENTS
def ex_mem(**kwargs):
    """
    EX/MEM Pipeline register
    :param clock: system clock
    :param branch_in: branch ctrl signal from id_ex.branch_out
    :param mem_read_in: mem_read ctrl signal. from id_ex.mem_read_out
    :param mem_write_in: mem_write ctrl signal. from id_ex.mem_write_out
    :param mem_to_reg_in: mem_to_reg ctrl signal from id_ex
    :param reg_write_in: reg_write ctrl signal. from id_ex.reg_write_out
    :param mem_to_reg_in: mem_to_reg ctrl signal. from id_ex.mem_to_reg_out
    :param jmp_addr: jump address.  from branch_adder.addr_out
    :param z_in: zero flag.  from alu.
    :param pc_value_in: pc+4 value, from id_ex
    :param result_in: result input. from ALU
    :param rt_in: special rt input, for sw. from alu_mux_b
    :param reg_dst: destination reg address. from ex_mux
    :param jmp_addr_out: jump address. to pc_mux_a
    :param z_out: zero flag. to branch_unit
    :param result_out: read ALU result output. to data_mem, mem_wb, alu_mux_a
    :param rt_out: special rt output for sw. to data_mem.rt_in, fwd_unit.ex_rd
    :param branch_out: branch ctrl signal to branch_unit.branch_ctrl
    :param mem_read_out: mem_read ctrl signal to data_mem.read_ctrl
    :param mem_write_out: mem_write ctrl signal to data_mem.w_ctrl
    :param reg_write_out: reg_write ctrl signal to mem_wb.reg_write_in
    :param mem_to_reg_out: mem_to_reg ctrl signal to mem_wb.
    :param reg_dst_out: Destination Register for write back to mem_wb
    :param pc_value_out:
    :param mem_to_reg_out: mem_to_reg ctrl signal to mem_wb
    :return:
    """
    def logic():
        # NOT IMPLEMENTED
        pass
    return logic


# YOU NEED TO INSTANTIATE WITH KEYWORD ARGUMENTS
def ex_mem_v(**kwargs):
    """
    Verilog See above
    :param kwargs:
    :return:
    """
    return Cosimulation()
