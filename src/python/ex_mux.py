from os import system

from myhdl import always_comb, Cosimulation

def ex_mux(reg_dst, rt_in, rd_in, dest):
    """
    2:1 Mux to select write address
    :param reg_dst: 1 bit selector from id_ex.reg_dst_out 0 for rt, 1 for rd
    :param rt_in: rt, sent from id_ex
    :param rd_in: rd, sent from id_ex
    :param dest: destination register address, sent to ex_mem
    :return: module logic
    """

    @always_comb
    def logic():
        if reg_dst == 0:
            dest.next = rt_in
        else:
            dest.next = rd_in

    return logic


def ex_mux_v(reg_dst, rt_in, rd_in, dest):
    """
    2:1 Mux to select write address Verilog
    :param reg_dst: 1 bit selector from id_ex.reg_dst_out 0 for rt, 1 for rd
    :param rt_in: rt, sent from id_ex
    :param rd_in: rd, sent from id_ex
    :param dest: destination register address, sent to ex_mem
    :return: module logic
    """
    cmd = "iverilog -o bin/ex_mux.out src/verilog/ex_mux.v src/verilog/ex_mux_tb.v"
    system(cmd)
    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/ex_mux.out",
                        reg_dst=reg_dst,
                        rt_in=rt_in,
                        rd_in=rd_in,
                        dest=dest)
