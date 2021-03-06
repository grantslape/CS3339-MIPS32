""" Register file """
from os import system
from myhdl import Cosimulation, always, block
from src.commons.settings import settings as sf
from src.commons.signal_generator import signed_signal_set


@block
def rfile(clock, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2):
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
    reg_file = signed_signal_set(sf['WIDTH'], value=0)

    @always(clock.negedge)
    def read_logic():
        """ Read logic triggered on negative edge of clock """
        r_data1.next = reg_file[r_addr1]
        r_data2.next = reg_file[r_addr2]

    @always(clock.posedge)
    def write_logic():
        """ Write logic triggered on positive edge of clock """
        if reg_write == 1:
            reg_file[w_addr].next = w_data

    return read_logic, write_logic


def rfile_v(clock, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2):
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
    cmd = "iverilog -o bin/rfile.out src/verilog/rfile.v src/verilog/rfile_tb.v"
    system(cmd)
    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/rfile.out",
                        clock=clock,
                        reg_write=reg_write,
                        r_addr1=r_addr1,
                        r_addr2=r_addr2,
                        w_addr=w_addr,
                        w_data=w_data,
                        r_data1=r_data1,
                        r_data2=r_data2)
