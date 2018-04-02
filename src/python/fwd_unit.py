import os

from myhdl import always_comb, Cosimulation


def fwd_unit(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b):
    """
    Main Forwading Unit.  Detects matches on either rt or rs from previous two cycles, and forwards appropriately
    :param rt_in: current rt address. from id_ex
    :param rs_in:  current rs_address. from id_ex
    :param ex_rd: address of previous rd.  from ex_mem
    :param mem_rd: address of 2nd previous rd.  from mem_wb
    :param mem_reg_write: control signal.  from ex_mem
    :param wb_reg_write: control signal.  from mem_wb
    :param forward_a: two bit input selector. to alu_mux_a
    :param forward_b: two bit input selector. to alu_mux_b
    :return: generator logic
    """
    @always_comb
    def logic():
        # NOT IMPLEMENTED
        return logic

def fwd_unit_v(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write, forward_a, forward_b):
    """
    Verilog Forwading Unit.  Detects matches on either rt or rs from previous two cycles, and forwards appropriately
    :param rt_in: current rt address. from id_ex
    :param rs_in:  current rs_address. from id_ex
    :param ex_rd: address of previous rd.  from ex_mem
    :param mem_rd: address of 2nd previous rd.  from mem_wb
    :param mem_reg_write: control signal.  from ex_mem
    :param wb_reg_write: control signal.  from mem_wb
    :param forward_a: two bit input selector. to alu_mux_a
    :param forward_b: two bit input selector. to alu_mux_b
    :return: generator logic
    """
    cmd = "iverilog -o fwd_unit_v.out src/verilog/fwd_unit.v src/verilog/fwd_unit_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m lib/myhdl.vpi fwd_unit.out",
                        rt_in=rt_in,
                        rs_in=rs_in,
                        ex_rd=ex_rd,
                        mem_rd=mem_rd,
                        mem_reg_write=mem_reg_write,
                        wb_reg_write=wb_reg_write,
                        forward_a=forward_a,
                        forward_b=forward_b)