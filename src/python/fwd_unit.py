import os

from myhdl import always_comb, intbv, Cosimulation


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
        forward_a.next = intbv(0)[2:]
        forward_b.next = intbv(0)[2:]
        if mem_reg_write == 1 and ex_rd != 0:
            if ex_rd == rs_in:
                forward_a.next = intbv(2)[2:]
            else:
                forward_a.next = intbv(0)[2:]
            
            if ex_rd == rt_in:
                forward_b.next = intbv(2)[2:]
            else:
                forward_b.next = intbv(0)[2:]

        if wb_reg_write == 1 and mem_rd != 0:
            if mem_rd == rs_in:
                forward_a.next = intbv(1)[2:]
            else:
                forward_a.next = intbv(0)[2:]
            
            if mem_rd == rt_in:
                forward_b.next = intbv(1)[2:]
            else:
                forward_b.next = intbv(0)[2:]

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
    cmd = "iverilog -o fwd_unit.out src/verilog/fwd_unit.v src/verilog/fwd_unit_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m ./lib/myhdl.vpi fwd_unit.out",
                        rt_in=rt_in,
                        rs_in=rs_in,
                        ex_rd=ex_rd,
                        mem_rd=mem_rd,
                        mem_reg_write=mem_reg_write,
                        wb_reg_write=wb_reg_write,
                        forward_a=forward_a,
                        forward_b=forward_b)
