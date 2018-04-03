import os

from myhdl import always_comb, Cosimulation

def shift_unit(imm_in, imm_out):
    """
    Shift Left 2 Unit, for calculating addresses from a 16 bit immediate
    :param imm_in: 32 bit immediate from id_ex
    :param imm_out: input value shifted left 2 bits
    :return: module logic
    """
    @always_comb
    def logic():
        # NOT IMPLEMENTED
        return logic

def shift_unit_v(imm_in, imm_out):
    """
    Verilog Shift Left 2 Unit, for calculating addresses from a 16 bit immediate
    :param imm_in: 32 bit immediate from id_ex
    :param imm_out: input value shifted left 2 bits
    :return: module logic
    """
    cmd = "iverilog -o shift_unit_v.out src/verilog/shift_unit.v src/verilog/shift_unit_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m lib/myhdl.vpi shift_unit.out",
                        imm_in=imm_in,
                        imm_out=imm_out)