"""Ctrl Unit Mux"""
from os import system

from myhdl import always_comb, Cosimulation


def ctrl_mux(**kwargs):
    """
    Ctrl Mux module
    :param kwargs: See structure.txt :: ctrl_mux
    :return: module logic
    """

    @always_comb
    def logic():
        # NOT IMPLEMENTED
        pass
    return logic


def ctrl_mux_v(**kwargs):
    """
    Ctrl Mux module verilog
    :param kwargs: See structure.txt :: ctrl_mux
    :return: module logic
    """
    return Cosimulation()
