from os import system

from myhdl import always_comb, Cosimulation, block


@block
def mux32bit3to1(ctrl_line, data1, data2, data3, out):
    """
    3:1 Mux for forwarding results from 2 cycles ago
    :param ctrl_line: two bit input selector from fwd_unit
    :param data1: rs data received from id_ex 0
    :param data2: rd from the previous cycle, received from ex_mem 01
    :param data3: rd from two cycles ago, received from wb_mux 10
    :param out: Output for rs/op1.  Sent to ALU
    :return: module logic
    """
    @always_comb
    def logic():
        if ctrl_line == 2:
            # datasrc is the mem/wb pipeline register
            out.next = data3
        elif ctrl_line == 1:
            # datasrc is ex/mem pipeline register
            out.next = data2
        elif ctrl_line == 0:
            # datasrc is the id/ex pipeline register
            out.next = data1
    return logic


def mux32bit3to1_v(ctrl_line, data1, data2, data3, out):

    """
    3:1 Mux for forwarding results from 2 cycles ago Verilog
    :param forward_a: forward_a: two bit input selector from fwd_unit
    :param r_data1: rs data received from id_ex 0
    :param data2: rd from the previous cycle, received from ex_mem 01
    :param data3: rd from two cycles ago, received from wb_mux 10
    :param op1_out: Output for Rs/Op1.  Sent to ALU
    :return: module logic
    """

    cmd = "iverilog -o bin/mux32bit3to1.out src/verilog/mux32bit3to1.v src/verilog/mux32bit3to1_tb.v"
    system(cmd)
    return Cosimulation("vvp -m lib/myhdl.vpi bin/mux32bit3to1.out",
                        ctrl_line=ctrl_line,
                        data1=data1,
                        data2=data2,
                        data3=data3,
                        out=out)
