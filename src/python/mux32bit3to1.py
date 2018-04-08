import os

from myhdl import always_comb, Cosimulation

def mux32bit3to1(ctrl, data1, mem_rd, wb_rd, output):
    """
    3:1 Mux for forwarding results from 2 cycles ago
    :param ctrl: two bit input selector from fwd_unit
    :param data1: rs data received from id_ex 0
    :param mem_rd: rd from the previous cycle, received from ex_mem 01
    :param wb_rd: rd from two cycles ago, received from wb_mux 10
    :param output: Output for rs/op1.  Sent to ALU
    :return: module logic
    """

    @always_comb
    def logic():
        if ctrl == 2:
           #datasrc is the mem/wb pipeline register
            output.next = wb_rd
        elif ctrl == 1:
            #datasrc is ex/mem pipeline register
            output.next = mem_rd
        elif ctrl == 0:
           #datasrc is the id/ex pipeline register
            output.next = data1
    return logic

def mux32bit3to1_v(ctrl, data1, mem_rd, wb_rd, output):

    """
    3:1 Mux for forwarding results from 2 cycles ago Verilog
    :param forward_a: forward_a: two bit input selector from fwd_unit
    :param r_data1: rs data received from id_ex 0
    :param mem_rd: rd from the previous cycle, received from ex_mem 01
    :param wb_rd: rd from two cycles ago, received from wb_mux 10
    :param op1_out: Output for Rs/Op1.  Sent to ALU
    :return: module logic
    """

    cmd = "iverilog -o bin/mux32bit3to1.out src/verilog/mux32bit3to1.v src/verilog/mux32bit3to1_tb.v"
    os.system(cmd)
    return Cosimulation("vvp -m  lib/myhdl.vpi bin/mux32bit3to1.out",
                        ctrl=ctrl,
                        data1=data1,
                        mem_rd=mem_rd,
                        wb_rd=wb_rd,
                        output=output)
