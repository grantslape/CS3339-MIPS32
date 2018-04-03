import os

from myhdl import always_comb, Cosimulation


def shift_unit(imm_in, imm_out):
    """
    Shift Unit
    :param imm_in: The sign-extended 32 bit immediate values
    :param imm_out: The sign extended value has been shifted left two bits
    :return: Shift unit module logic
    """

    @always_comb
    def logic():
        imm_out.next = imm_in << 2
    return logic


def shift_unit_v(imm_in, imm_out):
    """
    :param imm_in: The sign-extended 32 bit immediate values
    :param imm_out: The sign extended value has been shifted left two bits
    :return:A cosimulation object 
    """

    cmd = "iverilog -o shift_unit.out src/verilog/shift_unit.v src/verilog/shift_unit_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m ./lib/myhdl.vpi shift_unit.out",
                        imm_in=imm_in,
                        imm_out=imm_out)
