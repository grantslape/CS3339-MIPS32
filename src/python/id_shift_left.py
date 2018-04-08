import os
from myhdl import Cosimulation, always_comb


def id_shift_left(top4, target, jaddr_out):
    """
    early jump support shift target left 2, then concat with top4
    :param top4: top 4 bits of PC.  from if_id
    :param target: 26 bit immediate jump target.  from if_id
    :param jaddr_out: jump address. to pc_mux_b
    :return: module logic
    """
    @always_comb
    def logic():
        # NOT IMPLEMENTED
        pass
    return logic


def id_shift_left_v(top4, target, jaddr_out):
    """
        early jump support shift target left 2, then concat with top4 Verilog
        :param top4: top 4 bits of PC.  from if_id
        :param target: 26 bit immediate jump target.  from if_id
        :param jaddr_out: jump address. to pc_mux_b
        :return: module logic
        """
    return Cosimulation()