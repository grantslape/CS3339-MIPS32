from os import system
from myhdl import Cosimulation, always_comb, block


@block
def pc_adder(cur_pc, next_pc):
    """
    PC Adder
    :param cur_pc: current instruction address. from program_counter
    :param next_pc: next sequential instruction address to pc_mux_a and if_id
    :return: module logic
    """
    @always_comb
    def logic():
        next_pc.next = cur_pc + int(0x4)
    return logic


def pc_adder_v(cur_pc, next_pc):
    """
    PC Adder Verilog
    :param cur_pc: current instruction address. from program_counter
    :param next_pc: next sequential instruction address to pc_mux_a and if_id
    :return: cosimulation
    """
    cmd = "iverilog -o bin/pc_adder.out src/verilog/pc_adder.v src/verilog/pc_adder_tb.v"
    system(cmd)

    return Cosimulation("vvp -m lib/myhdl.vpi bin/pc_adder.out", cur_pc=cur_pc, next_pc=next_pc)
