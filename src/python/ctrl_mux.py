"""Ctrl Unit Mux"""
from os import system

from myhdl import always_comb, Cosimulation


def ctrl_mux(ex_stall, jump, branch, mem_read, mem_to_reg, mem_write, alu_src, reg_write, reg_dst,
                alu_op, jump_out, branch_out, mem_read_out, mem_to_reg_out, mem_write_out,
                alu_src_out, reg_write_out, reg_dst_out, alu_op_out):
    """
    Ctrl multiplexer
    :param ex_stall:
    :param jump:
    :param branch:
    :param mem_read:
    :param mem_to_reg:
    :param mem_write:
    :param alu_src:
    :param reg_write:
    :param reg_dst:
    :param alu_op:
    :param jump_out:
    :param branch_out:
    :param mem_read_out:
    :param mem_to_reg_out:
    :param mem_write_out:
    :param alu_src_out:
    :param reg_write_out:
    :param reg_dst_out:
    :param alu_op_out:
    :return: module logic
    """

    @always_comb
    def logic():
        if ex_stall == 1:
            jump_out.next = 0
            branch_out.next = 0
            mem_read_out.next = 0
            mem_to_reg_out.next = 0
            mem_write_out.next = 0
            alu_src_out.next = 0
            reg_write_out.next = 0
            reg_dst_out.next = 0
            alu_op_out.next = 0
        else:
            jump_out.next = jump
            branch_out.next = branch
            mem_read_out.next = mem_read
            mem_to_reg_out.next = mem_to_reg
            mem_write_out.next = mem_write
            alu_src_out.next = alu_src
            reg_write_out.next = reg_write
            reg_dst_out.next = reg_dst
            alu_op_out.next = alu_op
    return logic


def ctrl_mux_v(ex_stall, jump, branch, mem_read, mem_to_reg, mem_write, alu_src, reg_write, reg_dst,
                    alu_op, jump_out, branch_out, mem_read_out, mem_to_reg_out, mem_write_out,
                    alu_src_out, reg_write_out, reg_dst_out, alu_op_out):
    """
    Ctrl Mux module verilog
    :param kwargs: See structure.txt :: ctrl_mux
    :return: module logic
    """
    cmd = "iverilog -o bin/ctrl_mux.out src/verilog/ctrl_mux.v src/verilog/tb_ctrL_mux.v"
    system(cmd)

    return Cosimulation("vvp -m lib/myhdl.vpi bin/ctrl_mux.out",
                        ex_stall=ex_stall,
                        jump=jump,
                        branch=branch,
                        mem_read=mem_read,
                        mem_to_reg=mem_to_reg,
                        mem_write=mem_write,
                        alu_src=alu_src,
                        reg_write=reg_write,
                        reg_dst=reg_dst,
                        alu_op=alu_op,
                        jump_out=jump_out,
                        branch_out=branch_out,
                        mem_read_out=mem_read_out,
                        mem_to_reg_out=mem_to_reg_out,
                        mem_write_out=mem_write_out,
                        alu_src_out=alu_src_out,
                        reg_write_out=reg_write_out,
                        reg_dst_out=reg_dst_out,
                        alu_op_out=alu_op_out)
