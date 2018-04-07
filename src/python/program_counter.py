import os
from myhdl import Cosimulation, always


def program_counter(clock, pc_write, nxt_inst, cur_pc):
    """
    Program Counter
    :param clock: system clock
    :param pc_write: 1 to stall (repeat instruction), from hazard_unit.pc_write
    :param nxt_inst: next instruction address from pc_mux_b
    :param cur_pc: next instruction addres goes to inst_mem, pc_mux_c
    :return: module logic
    """
    @always(clock.posedge)
    def seq_logic():
        if pc_write == 0:
            cur_pc.next = nxt_inst
        else:
            cur_pc.next = cur_pc
    return seq_logic


def program_counter_v(clock, pc_write, nxt_inst, cur_pc):
    """
    Program Counter Verilog
    :param clock: system clock
    :param pc_write: 1 to stall (repeat instruction), from hazard_unit.pc_write
    :param nxt_inst: next instruction address from pc_mux_b
    :param cur_pc: next instruction addres goes to inst_mem, pc_mux_c
    :return: cosimulation
    """
    cmd = "iverilog -o program_counter.out src/verilog/program_counter.v src/verilog/program_counter_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m lib/myhdl.vpi program_counter.out",
                        clock=clock,
                        pc_write=pc_write,
                        nxt_inst=nxt_inst,
                        cur_pc=cur_pc)
