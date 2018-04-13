"""Data memory module"""
from os import system
from myhdl import always, Cosimulation, intbv

def data_mem2(clk, address, write_wire, read_wire, write_data, read_data):
    """
    main data memory
    :param clk: clock (input)
    :param address: 32-bit memory address to access
    :param write_data: data to write to address
    :param read_data: data to read from address
    :param read_wire: activate read from mem
    :param write_wire: activate write to mem
    :return: module logic
    """

    # Initialize RAM from memory_file
    mem_file = open('memory_file')
    mem_array = []
    try:
        mem_array = [intbv(line) for line in mem_file]
    except IOError:
        pass
    mem_file.close()

    @always(clk.posedge)
    def logic():
        if read_wire == 1:
            read_data.next = mem_array[address]
        elif write_wire == 1:
            mem_array[address] = write_data

    return logic


def data_mem2_v(clk, address, write_wire, read_wire, write_data, read_data):
    """
    main data memory (verilog)
    :param clk: clock (input)
    :param address: 32-bit memory address to access
    :param write_data: data to write to address
    :param read_data: data to read from address
    :param read_wire: activate read from mem
    :param write_wire: activate write to mem
    :return: module logic
    """
    cmd = "iverilog -o bin/data_mem2.out src/verilog/data_mem2.v src/verilog/data_mem_tb.v"
    system(cmd)
    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/data_mem2.out",
                        clk=clk,
                        address=address,
                        write_wire=write_wire,
                        read_wire=read_wire,
                        write_data=write_data,
                        read_data=read_data)
