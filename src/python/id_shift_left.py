import os
from myhdl import Cosimulation, always_comb, intbv


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
        # top four bits of jump address from top4
        jaddr_out[:28].next = top4
        # shift target over 2 bits and replace jump address with target
        jaddr_out[28:2].next = target

    return logic


def id_shift_left_v(top4, target, jaddr_out):
    """
        early jump support shift target left 2, then concat with top4 Verilog
        :param top4: top 4 bits of PC.  from if_id
        :param target: 26 bit immediate jump target.  from if_id
        :param jaddr_out: jump address. to pc_mux_b
        :return: module logic
        """

    cmd = "iverilog -o bin/id_shift_left.out src/verilog/id_shift_left.v src/verilog/id_shift_left_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/id_shift_left.out",
                        top4=top4,
                        target=target,
                        jaddr_out=jaddr_out)
