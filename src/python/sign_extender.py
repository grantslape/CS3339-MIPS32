import os

from myhdl import always_comb, Cosimulation


def sign_extender(imm_in, imm_out):
    """
    Sign Extender
    :param imm_in: immediate from if_id state register
    :param imm_out: sign extended imm_in to 32 bits.  send to id_ex.
    :return: module logic
    """
    # NOT IMPLEMENTED
    pass


def sign_extender_v(imm_in, imm_out):
    """
    Sign Extender Verilog
    :param imm_in: immediate from if_id state register
    :param imm_out: sign extended imm_in to 32 bits.  send to id_ex.
    :return: module logic
    """
    return Cosimulation()