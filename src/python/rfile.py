from os import system

from myhdl import always, posedge, negedge, Cosimulation, intbv, always_seq, Signal

from src.commons.settings import settings as sf

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
    reg_file = [Signal(intbv(0, min=-(2**31), max=2**31-1)) for i in range(sf['WIDTH'])]

    @always_seq(clock.negedge, reset=reset)
    def logic():
        if reg_write == 1:
            reg_file[w_addr] = w_data
        r_data1.next = reg_file[r_addr1]
        r_data2.next = reg_file[r_addr2]


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
    cmd = "iverilog -o bin/rfile.out src/verilog/rfile.v src/verilog/rfile_tb.v"
    system(cmd)
    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/rfile.out",
                        clock=clock,
                        reset=reset,
                        reg_write=reg_write, 
                        r_addr1=r_addr1, 
                        r_addr2=r_addr2, 
                        w_addr=w_addr, 
                        w_data=w_data, 
                        r_data1=r_data1, 
                        r_data2=r_data2)
