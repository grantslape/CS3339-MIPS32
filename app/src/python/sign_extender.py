"""Sign Extender Module"""
from os import system
from myhdl import always_comb, Cosimulation, block


@block
def sign_extender(imm_in, imm_out):
    """
    Sign Extend 16 bit immediate to 32 bit
    :param imm_in:
    :param imm_out:
    :return:
    """
    @always_comb
    def logic():
        if imm_in.next >= 0x8000:
            imm_out.next = imm_in | 0xffff0000
        else:
            imm_out.next = imm_in
    return logic


def sign_extender_v(imm_in, imm_out):
    cmd = "iverilog -o bin/sign_extender.out src/verilog/sign_extender.v src/verilog/sign_extender_tb.v"
    system(cmd)

    return Cosimulation("vvp -m lib/myhdl.vpi bin/sign_extender.out",
                        imm_in=imm_in,
                        imm_out=imm_out)
