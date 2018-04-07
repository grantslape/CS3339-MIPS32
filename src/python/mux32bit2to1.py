import os

from myhdl import always_comb, Cosimulation


def mux32bit2to1(ctrl_line, input1, input2, out):
    """
    32_bit_2_to_1_mux

    :param ctrl_line: Which input should be output. If 1 input2 else input1
    :param input1: first 32-bit input
    :param input2: second 32-bit input
    :param output: 32-bit output
    :return: generator logic
    """

    @always_comb
    def logic():
        if ctrl_line == 0:
            out.next = input1
        else:
            out.next = input2

    return logic


def mux32bit2to1_v(ctrl_line, input1, input2, out):
    """
    Instantiate Vefilog module

    :param ctrl_line: Which input should be output. If 1 input2 else input1
    :param input1: first 32-bit input
    :param input2: second 32-bit input
    :param out: 32-bit output
    :return: Cosimulation
    """
    cmd = "iverilog -o bin/mux32bit2to1.out src/verilog/mux32bit2to1.v src/verilog/mux32bit2to1_tb.v"
    os.system(cmd)
    return Cosimulation("vvp -m lib/myhdl.vpi bin/mux32bit2to1.out",
                        ctrl_line=ctrl_line,
                        input1=input1,
                        input2=input2,
                        out=out)
