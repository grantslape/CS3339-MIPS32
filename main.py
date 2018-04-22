"""
# CS339-265 Team White Group Project
# Grant Slape
# Isaac Jaimes
# Patrick Vinas
# Mark Gitthens
# Serena Gutierrez
# Natalie Garza
# Huan Wu
"""
from myhdl import Simulation, bin, StopSimulation

from src.python.program_counter import program_counter
from src.commons.clock import clock_gen
from src.commons.settings import settings as sf
from src.commons.signal_generator import *
from src.python.mux32bit3to1 import mux32bit3to1
from src.python.mux32bit2to1 import mux32bit2to1

clock, pc_write, pc_src, jmp_ctrl = unsigned_signal_set(4, width=1)
nxt_inst, cur_pc, imm_jmp_addr, nxt_pc, nxt_inst_mux_a, jmp_addr_last, jmp_reg = unsigned_signal_set(7)


def top():
    """Instantiate modules"""
    pc = program_counter(clock=clock, pc_write=pc_write, nxt_inst=nxt_inst, cur_pc=cur_pc)
    pc_mux_a = mux32bit2to1(ctrl_line=pc_src,
                            input1=nxt_pc,
                            input2=imm_jmp_addr,
                            out=nxt_inst_mux_a)
    pc_mux_b = mux32bit3to1(ctrl_line=jmp_ctrl,
                            data1=nxt_inst_mux_a,
                            data2=jmp_addr_last,
                            data3=jmp_reg,
                            out=nxt_inst)

    clock_inst = clock_gen(clock)

    return clock_inst, pc, pc_mux_a, pc_mux_b


def stim():
    """Test stimulus"""
    while 1:
        nxt_pc.next += 4
        yield clock.negedge
        print("PC: {}".format(hex(cur_pc)))


def main():
    """Run the simulation!!"""
    Simulation(top(), stim()).run(duration=1000000)


if __name__ == '__main__':
    main()
