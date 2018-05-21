from os import system

from myhdl import always_comb, Cosimulation, block


@block
def ex_mux(reg_dst, rt_in, rd_in, dest):
    """
    2:1 Mux to select write address
    :param reg_dst: 2 bit selector from id_ex.reg_dst_out 0 for rt, 1 for rd, 2 for ra
    :param rt_in: rt, sent from id_ex
    :param rd_in: rd, sent from id_ex
    :param dest: destination register address, sent to ex_mem
    :return: module logic
    """

    registerRA = 0b11111

    @always_comb
    def logic():
        if reg_dst == 0:
            dest.next = rt_in
        elif reg_dst == 1:
            dest.next = rd_in
        elif reg_dst == 2:
            dest.next = registerRA

    return logic


def ex_mux_v(reg_dst, rt_in, rd_in, dest):
    """
    2:1 Mux to select write address Verilog
    :param reg_dst: 2 bit selector from id_ex.reg_dst_out 0 for rt, 1 for rd, 2 for ra
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
