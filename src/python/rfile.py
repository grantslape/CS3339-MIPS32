import os

from myhdl import always_seq, posedge, negedge, Cosimulation


def rfile(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2):
    """
    32-bit Register File of 32 registers
    :param clock: Input from system clock
    :param reset: ResetSignal, async
    :param reg_write: write control signal
    :param r_addr1: read address of rs. from if_id
    :param r_addr2: read address of rt. from if_id
    :param w_addr: write address of "rd". from mem_wb
    :param w_data: write data.  From write_mux
    :param r_data1: rs data read from regs[r_addr1].  sent to id_ex
    :param r_data2: data read from regs[r_addr2].  sent to id_ex
    :return: module logic
    """
    @always_seq(clock.negedge, reset=reset)
    def logic():
        # NOT IMPLEMENTED
        pass
    return logic


def rfile_v(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2):
    """
    32-bit Register File of 32 registers Verilog
    :param clock: Input from system clock
    :param reset: ResetSignal, async
    :param reg_write: write control signal
    :param r_addr1: read address of rs. from if_id
    :param r_addr2: read address of rt. from if_id
    :param w_addr: write address of "rd". from mem_wb
    :param w_data: write data.  From write_mux
    :param r_data1: rs data read from regs[r_addr1].  sent to id_ex
    :param r_data2: data read from regs[r_addr2].  sent to id_ex
    :return: module logic
    """
    return Cosimulation()