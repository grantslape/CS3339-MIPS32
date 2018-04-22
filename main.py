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

from src.python.inst_mem import inst_mem
from src.python.program_counter import program_counter
from src.commons.clock import clock_gen
from src.commons.settings import settings as sf
from src.commons.signal_generator import *
from src.python.mux32bit3to1 import mux32bit3to1
from src.python.mux32bit2to1 import mux32bit2to1
from src.python.pc_adder import pc_adder

clock, pc_write, pc_src, jmp_ctrl = unsigned_signal_set(4, width=1)
nxt_inst, cur_pc, imm_jmp_addr, nxt_pc, nxt_inst_mux_a, jmp_addr_last, jmp_reg, inst_out, inst_if = unsigned_signal_set(9)


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
    pc_add = pc_adder(cur_pc=cur_pc,
                      next_pc=nxt_pc)
    inst_memory = inst_mem(inst_reg=nxt_inst,
                           inst_out=inst_out)
    inst_mem_mux = mux32bit2to1(ctrl_line=jmp_ctrl,
                                input1=inst_out,
                                input2=Signal(unsigned_intbv()),
                                out=inst_if)

    clock_inst = clock_gen(clock)

    return clock_inst, pc, pc_mux_a, pc_mux_b, pc_add, inst_memory, inst_mem_mux


def stim():
    """Test stimulus"""
    cur_pc.next = 4
    while 1:
        if cur_pc % 50000 == 0:
            pc_write.next = 1
            for _ in range(100):
                yield clock.negedge
                print("Inst: {}".format(bin(inst_out)))
            pc_write.next = 0
            yield clock.negedge
            print("Inst: {}".format(bin(inst_out)))
        yield clock.negedge
        print("Inst: {}".format(bin(inst_out)))


def monitor():
    """Monitoring output"""
    yield clock.negedge
    print("Inst: {}".format(bin(inst_out)))


def main():
    """Run the simulation!!"""
    Simulation(top(), stim()).run(duration=1000000)


if __name__ == '__main__':
    main()
