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

from sign_extender import sign_extender
from src.python.mux32bit3to1 import mux32bit3to1
from src.python.mux32bit2to1 import mux32bit2to1
from src.python.pc_adder import pc_adder
from src.python.inst_mem import inst_mem
from src.python.program_counter import program_counter
from src.python.if_id import if_id
from src.commons.clock import clock_gen
from src.commons.settings import settings as sf
from src.commons.signal_generator import *

clock, pc_write, pc_src, jmp_ctrl = unsigned_signal_set(4, width=1)

nxt_inst, cur_pc, imm_jmp_addr, nxt_pc, nxt_inst_mux_a, jmp_addr_last, jmp_reg, inst_out, inst_if, \
    pc_id, if_id_write = unsigned_signal_set(11)

imm_out = Signal(signed_intbv())

rs, rt, rd = unsigned_signal_set(3, width=5)

imm = Signal(intbv(min=sf['16_SIGNED_MIN_VALUE'], max=sf['16_SIGNED_MAX_VALUE']))
top4 = Signal(unsigned_intbv(width=4))
target_out = Signal(unsigned_intbv(width=26))
op_code, funct_out = unsigned_signal_set(2, width=6)


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

    if_id_pipe = if_id(if_id_write=if_id_write,
                       clock=clock,
                       nxt_pc=nxt_pc,
                       inst_in=inst_out,
                       op_code=op_code,
                       rs=rs,
                       rt=rt,
                       imm=imm,
                       rd=rd,
                       funct_out=funct_out,
                       pc_out=pc_id,
                       top4=top4,
                       target_out=target_out)

    extender = sign_extender(imm_in=imm, imm_out=imm_out)


    clock_inst = clock_gen(clock)

    return clock_inst, pc, pc_mux_a, pc_mux_b, pc_add, inst_memory, inst_mem_mux, if_id_pipe, extender


def stim():
    """Test stimulus"""
    cur_pc.next = 4
    while 1:
        # if cur_pc % 50000 == 0:
        #     pc_write.next = 1
        #     for _ in range(100):
        #         yield clock.negedge
        #         print("Inst: {}".format(bin(inst_out)))
        #     pc_write.next = 0
        #     yield clock.negedge
        #     print("Inst: {}".format(bin(inst_out)))
        if pc_id == 350000:
            pc_write.next = 1
        yield clock.negedge
        print("PC: {}, Op: {}, funct: {}, rs: {}, rt: {}, rd: {}, imm: {}".format(
            bin(pc_id, width=32), bin(op_code, width=6), bin(funct_out, width=6), bin(rs),
            bin(rt, width=5), bin(rd), bin(imm, width=16)))


def monitor():
    """Monitoring output"""
    # TODO: make this work
    yield clock.negedge
    print("Inst: {}".format(bin(inst_out)))


def main():
    """Run the simulation!!"""
    Simulation(top(), stim()).run(duration=1000000)


if __name__ == '__main__':
    main()
