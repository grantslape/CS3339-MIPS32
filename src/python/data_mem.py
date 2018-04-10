"""Data memory module"""
from os import system
from myhdl import Signal, always, intbv, Cosimulation
from src.commons.settings import settings as sf

def data_mem(clk, address, write_data, read_data, read_wire, write_wire):
    """
    data memory
    :param clk: clock (input)
    :param address: 32-bit memory address to access
    :param write_data: data to write to address
    :param read_data: data to read from address
    :param read_wire: activate read from mem
    :param write_wire: activate write to mem
    :return: module logic
    """
    # Initialize 4KB of "RAM"
    mem = [Signal(intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE']))]*4096

    @always(clk.posedge)
    def logic():
        if write_wire == 1:
            mem[intbv(address)] = write_data.val
        elif read_wire == 1:
            read_data.next = mem[intbv(address)]

    return logic


def wb_mux_v(clk, address, write_data, read_data, read_wire, write_wire):
    """
    data memory (verilog)
    :param clk: clock (input)
    :param address: 32-bit memory address to access
    :param write_data: data to write to address
    :param read_data: data to read from address
    :param read_wire: activate read from mem
    :param write_wire: activate write to mem
    :return: module logic
    """
    cmd = "iverilog -o bin/data_mem.o src/verilog/data_mem.v src/verilog/data_mem_tb.v"
    system(cmd)
    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/data_mem.out",
                        clk=clk,
                        address=address,
                        write_data=write_data,
                        read_data=read_data,
                        read_wire=read_wire,
                        write_wire=write_wire)
