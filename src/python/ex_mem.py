"""EX/MEM Pipeline register"""
import os
from myhdl import always, Cosimulation


def ex_mem(clock, branch_in, mem_read_in, mem_write_in, mem_to_reg_in, reg_write_in, jmp_addr,
           z_in, result_in, rt_in, reg_dst, jmp_addr_out, z_out, result_out, rt_out,
           branch_out, mem_read_out, mem_write_out, reg_write_out, reg_dst_out, mem_to_reg_out):
    """
    EX/MEM Pipeline register
    :param clock: system clock
    :param branch_in: branch ctrl signal from id_ex.branch_out
    :param mem_read_in: mem_read ctrl signal. from id_ex.mem_read_out
    :param mem_write_in: mem_write ctrl signal. from id_ex.mem_write_out
    :param mem_to_reg_in: mem_to_reg ctrl signal from id_ex
    :param reg_write_in: reg_write ctrl signal. from id_ex.reg_write_out
    :param jmp_addr: jump address.  from branch_adder.addr_out
    :param z_in: zero flag.  from alu.
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
    :param reg_dst_out: Destination Register for write back to mem_wb
    :param mem_to_reg_out: mem_to_reg ctrl signal to mem_wb
    :return:
    """
    @always(clock.posedge)
    def logic():
        branch_out.next = branch_in
        mem_read_out.next = mem_read_in
        mem_write_out.next = mem_write_in
        mem_to_reg_out.next = mem_to_reg_in
        reg_write_out.next = reg_write_in
        jmp_addr_out.next = jmp_addr
        z_out.next = z_in
        result_out.next = result_in
        rt_out.next = rt_in
        reg_dst_out.next = reg_dst
        
    return logic


def ex_mem_v(clock, branch_in, mem_read_in, mem_write_in, mem_to_reg_in, reg_write_in, jmp_addr,
           z_in, result_in, rt_in, reg_dst, jmp_addr_out, z_out, result_out, rt_out,
           branch_out, mem_read_out, mem_write_out, reg_write_out, reg_dst_out, mem_to_reg_out):
    """
    Verilog See above
    :param kwargs:
    :return:
    """
    cmd = "iverilog -o bin/ex_mem.out src/verilog/ex_mem.v src/verilog/ex_mem_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m lib/mydhl.vpi bin/ex_mem.out",
                        clock=clock,
                        branch_in=branch_in,
                        mem_read_in=mem_read_in,
                        mem_write_in=mem_write_in,
                        mem_to_reg_in=mem_to_reg_in,
                        reg_write_in=reg_write_in,
                        jmp_addr=jmp_addr,
                        z_in=z_in,
                        result_in=result_in,
                        rt_in=rt_in,
                        reg_dst=reg_dst,
                        jmp_addr_out=jmp_addr_out,
                        z_out=z_out,
                        result_out=result_out,
                        rt_out=rt_out,
                        branch_out=branch_out,
                        mem_read_out=mem_read_out,
                        mem_write_out=mem_write_out,
                        reg_write_out=reg_write_out,
                        reg_dst_out=reg_dst_out,
                        mem_to_reg_out=mem_to_reg_out)
