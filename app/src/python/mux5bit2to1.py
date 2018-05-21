from os import system

from myhdl import always_comb, Cosimulation, block


@block
def mux5bit2to1(ctrl_line, input1, input2, out):
    """
    5_bit_2_to_1_mux

    :param ctrl_line: Which input should be output. If 1 input2, if 0 input1, if 2 then $ra
    :param input1: first 5-bit input
    :param input2: second 5-bit input
    :param out: 5-bit output
    :param registerRA: internal $ra value
    :return: generator logic
    """
    registerRA = 0b11111

    @always_comb
    def logic():
        if ctrl_line == 0:
            out.next = input1
        elif ctrl_line == 1:
            out.next = input2
        else:
            out.next = registerRA

    return logic


def mux5bit2to1_v(ctrl_line, input1, input2, out):
    """
    Instantiate Vefilog module

    :param ctrl_line: Which input should be output. If 1 input2 else input1
    :param input1: first 5-bit input
    :param input2: second 5-bit input
    :param out: 5-bit output
    :param registerRA: internal $ra value
    :return: Cosimulation
    """
    cmd = "iverilog -o bin/mux5bit2to1.out src/verilog/mux5bit2to1.v src/verilog/mux5bit2to1_tb.v"
    system(cmd)
    return Cosimulation("vvp -m lib/myhdl.vpi bin/mux5bit2to1.out",
                        ctrl_line=ctrl_line,
                        input1=input1,
                        input2=input2,
                        out=out)
