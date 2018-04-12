"""Memory writeback module"""
from os import system
import sys
from myhdl import always, Cosimulation, block

@block
def mem_wb(clk, reset,
           w_reg_ctl_in=0,
           mux_ctl_in=0,
           mem_data_in=0,
           alu_result_in=0,
           w_reg_addr_in=0,
           w_reg_ctl_out=0,
           mux_ctl_out=0,
           mem_data_out=0,
           alu_result_out=0,
           w_reg_addr_out=0):
    """mem_wb: Memory/Writeback pipeline latch
    :param clk: clock (input)
    :param reset: reset signal
    :param w_reg_ctl_(in/out): write register control signal
    :param mux_ctl_(in/out): mux control signal
    :param mem_data_(in/out): data from mem stage
    :param alu_result_(in/out): result from ex stage
    :param w_reg_addr_(in/out): write register address
    :return: module latch
    """

    @always(clk.posedge, reset.posedge)
    def latch():
        if reset == 1:
            w_reg_ctl_out.next = 0
            mux_ctl_out.next = 0
            mem_data_out.next = 0
            alu_result_out.next = 0
            w_reg_addr_out.next = 0
        else:
            w_reg_ctl_out.next = w_reg_ctl_in
            mux_ctl_out.next = mux_ctl_in
            mem_data_out.next = mem_data_in
            alu_result_out.next = alu_result_in
            w_reg_addr_out.next = w_reg_addr_in

    return latch



def mem_wb_v(clk, reset, w_reg_ctl_in, mux_ctl_in, mem_data_in, alu_result_in, w_reg_addr_in, 
             w_reg_ctl_out, mux_ctl_out, mem_data_out, alu_result_out, w_reg_addr_out):
    """mem_wb: Memory/Writeback pipeline latch
    :param clk: clock (input)
    :param reset: reset signal
    :param w_reg_ctl_(in/out): write register control signal
    :param mux_ctl_(in/out): mux control signal
    :param mem_data_(in/out): data from mem stage
    :param alu_result_(in/out): result from ex stage
    :param w_reg_addr_(in/out): write register address
    :return: module latch"""
    cmd = "iverilog -o bin/mem_wb.out src/verilog/mem_wb.v src/verilog/mem_wb_tb.v"
    system(cmd)
    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/mem_wb.out",
                        clk=clk,
                        reset=reset,
                        w_reg_ctl_in=w_reg_ctl_in,
                        mux_ctl_in=mux_ctl_in,
                        mem_data_in=mem_data_in,
                        alu_result_in=alu_result_in,
                        w_reg_addr_in=w_reg_addr_in,
                        w_reg_ctl_out=w_reg_ctl_out,
                        mux_ctl_out=mux_ctl_out,
                        mem_data_out=mem_data_out,
                        alu_result_out=alu_result_out,
                        w_reg_addr_out=w_reg_addr_out)
