from os import system
from myhdl import always_comb, Cosimulation

def wb_mux(sel, dest, rt_in, rd_in):
    """
    memory writeback mux
    :param sel: 1 bit selector, 1 for rd, 0 for rt
    :param rt_in: rt, sent from mem
    :param rd_in: rd, sent from ex_mem
    :param dest: destination register address, sent to reg
    :return: module logic
    """

    @always_comb
    def logic():

        if sel == 1:
            dest.next = rd_in.val
        else:
            dest.next = rt_in.val

    return logic


def wb_mux_v(sel, dest, mem_in, ex_in):
    """
    memory writeback mux (verilog)
    :param sel: 1 bit selector, 1 for ex, 0 for mem
    :param mem_in: mem, sent from mem
    :param ex_in: ex, sent from ex_mem
    :param dest: destination register address, sent to reg
    :return: module logic
    """
    cmd = "iverilog -o bin/wb_mux.o src/verilog/wb_mux.v src/verilog/wb_mux_tb.v"
    system(cmd)
    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/wb_mux.out",
                        mem_in=mem_in,
                        ex_in=ex_in,
                        sel=sel,
                        dest=dest)
