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
from myhdl import Simulation, bin, StopSimulation, ResetSignal

from src.python.id_ex import id_ex
from src.python.hazard_unit import hazard_unit
from src.python.ctrl_mux import ctrl_mux
from src.python.ctrl import ctrl
from src.python.id_shift_left import id_shift_left
from src.python.rfile import rfile
from src.python.sign_extender import sign_extender
from src.python.mux32bit3to1 import mux32bit3to1
from src.python.mux32bit2to1 import mux32bit2to1
from src.python.pc_adder import pc_adder
from src.python.inst_mem import inst_mem
from src.python.program_counter import program_counter
from src.python.if_id import if_id
from src.commons.clock import clock_gen
from src.commons.settings import settings as sf
from src.commons.signal_generator import *

clock, pc_write, pc_src, jmp_ctrl, jump_gate, reset_ctrl, branch_ctrl, branch_gate, branch_id_ex, \
    mem_read_ctrl, mem_read_gate, mem_to_reg_ctrl, mem_to_reg_gate, mem_to_reg_id_ex, mem_write_ctrl, mem_read_id_ex, \
    mem_write_gate, mem_write_id_ex, alu_src_ctrl, alu_src_gate, alu_src_id_ex, reg_write_ctrl, \
    reg_write_gate, reg_write_id_ex, reg_dst_ctrl, reg_dst_gate, reg_dst_id_ex, ex_stall \
    = unsigned_signal_set(28, width=1)

nxt_inst, cur_pc, imm_jmp_addr, nxt_pc, nxt_inst_mux_a, jmp_addr_last, jmp_reg, inst_out, inst_if, \
    pc_id, pc_id_ex, if_id_write, reg_write_final = unsigned_signal_set(13)

imm_out, w_data, r_data1, r_data1_id_ex, r_data2, r_data2_id_ex = signed_signal_set(6)

rs, rs_id_ex, rt, rt_id_ex, rd, rd_id_ex, w_addr = unsigned_signal_set(7, width=5)

alu_op_code, alu_op_gate, alu_op_id_ex = unsigned_signal_set(3, width=sf['ALU_CODE_SIZE'])

imm, imm_id_ex = [
    Signal(intbv(min=sf['16_SIGNED_MIN_VALUE'], max=sf['16_SIGNED_MAX_VALUE'])) for _ in range(2)
]
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
                       target_out=target_out,
                       reset=reset_ctrl)

    extender = sign_extender(imm_in=imm, imm_out=imm_out)
    registers = rfile(clock=clock,
                      # dummy for now
                      reset=ResetSignal(sf['INACTIVE_HIGH'], active=sf['ACTIVE_LOW'], async=True),
                      r_addr1=rs,
                      r_addr2=rt,
                      w_addr=w_addr,
                      w_data=w_data,
                      r_data1=r_data1,
                      r_data2=r_data2,
                      reg_write=reg_write_final)

    id_shifter = id_shift_left(top4=top4,
                               target=target_out,
                               jaddr_out=jmp_addr_last)

    ctrl_unit = ctrl(clock=clock,
                     funct_in=funct_out,
                     op_in=op_code,
                     jump=jmp_ctrl,
                     branch=branch_ctrl,
                     alu_op=alu_op_code,
                     mem_read=mem_read_ctrl,
                     mem_to_reg=mem_to_reg_ctrl,
                     mem_write=mem_write_ctrl,
                     alu_src=alu_src_ctrl,
                     reg_write=reg_write_ctrl,
                     reg_dst=reg_dst_ctrl,
                     reset_out=reset_ctrl)

    ctrl_gate = ctrl_mux(ex_stall=ex_stall,
                         jump=jmp_ctrl,
                         branch=branch_ctrl,
                         mem_read=mem_read_ctrl,
                         mem_to_reg=mem_to_reg_ctrl,
                         mem_write=mem_write_ctrl,
                         alu_src=alu_src_ctrl,
                         reg_write=reg_write_ctrl,
                         reg_dst=reg_dst_ctrl,
                         alu_op=alu_op_code,
                         jump_out=jump_gate,
                         branch_out=branch_gate,
                         mem_read_out=mem_read_gate,
                         mem_to_reg_out=mem_to_reg_gate,
                         mem_write_out=mem_write_gate,
                         alu_src_out=alu_src_gate,
                         reg_write_out=reg_write_gate,
                         reg_dst_out=reg_dst_gate,
                         alu_op_out=alu_op_gate)

    hzd = hazard_unit(if_id_rs=rs,
                      if_id_rt=rt,
                      id_ex_rt=rt_id_ex,
                      mem_read=mem_read_id_ex,
                      pc_write=pc_write,
                      if_id_write=if_id_write,
                      ex_stall=ex_stall)

    id_ex_pipe = id_ex(clock=clock,
                       branch_in=branch_gate,
                       alu_op_in=alu_op_gate,
                       mem_read_in=mem_read_gate,
                       mem_write_in=mem_write_gate,
                       alu_src_in=alu_src_gate,
                       reg_write_in=reg_write_gate,
                       reg_dst_in=reg_dst_gate,
                       pc_value_in=pc_id,
                       mem_to_reg_in=mem_to_reg_gate,
                       r_data1=r_data1,
                       r_data2=r_data2,
                       rs=rs,
                       rt=rt,
                       rd=rd,
                       imm=imm,
                       r_data1_out=r_data1_id_ex,
                       r_data2_out=r_data2_id_ex,
                       imm_out=imm_id_ex,
                       rs_out=rs_id_ex,
                       rt_out=rt_id_ex,
                       rd_out=rd_id_ex,
                       pc_value_out=pc_id_ex,
                       branch_out=branch_id_ex,
                       alu_op_out=alu_op_id_ex,
                       mem_read_out=mem_read_id_ex,
                       mem_write_out=mem_write_id_ex,
                       alu_src_out=alu_src_id_ex,
                       reg_write_out=reg_write_id_ex,
                       reg_dst_out=reg_dst_id_ex,
                       mem_to_reg_out=mem_to_reg_id_ex)

    clock_inst = clock_gen(clock)

    return clock_inst, pc, pc_mux_a, pc_mux_b, pc_add, inst_memory, inst_mem_mux, if_id_pipe, \
        extender, registers, id_shifter, ctrl_unit, ctrl_gate, hzd, id_ex_pipe


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
        print("Cycle: {}, PC: {}, R1: {}, R2: {}, rs: {}, rt: {}, rd: {}, imm: {}, B: {}, MR: {}, MW: {}, "
              "AS: {}, RW: {}, RD: {}, MTR: {}, ALU: {}".format(int(nxt_inst // 4) + 1,
                bin(pc_id_ex, width=32), bin(r_data1_id_ex, width=32), bin(r_data2_id_ex, width=32),
                bin(rs_id_ex, width=5), bin(rt_id_ex, width=5), bin(rd_id_ex, width=5),
                bin(imm_id_ex, width=16), bin(branch_id_ex), bin(mem_read_id_ex),
                bin(mem_write_id_ex), bin(alu_src_id_ex), bin(reg_write_id_ex), bin(reg_dst_id_ex),
                bin(mem_to_reg_id_ex), bin(alu_op_id_ex, width=4)))


def monitor():
    """Monitoring output"""
    # TODO: make this work
    yield clock.negedge
    print("Inst: {}".format(intbv(nxt_inst)))


def main():
    """Run the simulation!!"""
    Simulation(top(), stim()).run(duration=97507)


if __name__ == '__main__':
    main()
