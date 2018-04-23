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

from src.python.branch_unit import branch_unit
from src.python.data_mem import data_mem
from src.python.mem_wb import mem_wb
from src.python.ex_mem import ex_mem
from src.python.branch_adder import branch_adder
from src.python.shift_unit import shift_unit
from src.python.fwd_unit import fwd_unit
from src.python.ex_mux import ex_mux
from src.python.alu import alu
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
    branch_ex_mem, mem_read_ctrl, mem_read_gate, mem_read_ex_mem, mem_to_reg_ctrl, \
    mem_to_reg_gate, mem_to_reg_id_ex, mem_to_reg_ex_mem, mem_to_reg_mem_wb, mem_write_ctrl, \
    mem_read_id_ex, mem_write_gate, mem_write_id_ex, mem_write_ex_mem, alu_src_ctrl, alu_src_gate, \
    alu_src_id_ex, reg_write_ctrl, reg_write_gate, reg_write_id_ex, reg_write_ex_mem, \
    reg_write_mem_wb, reg_dst_ctrl, reg_dst_gate, reg_dst_id_ex, ex_stall, zero_flag, \
    zero_flag_ex_mem \
    = unsigned_signal_set(37, width=1)

forward_a_out, forward_b_out = unsigned_signal_set(2, width=2)

nxt_inst, cur_pc, imm_jmp_addr, nxt_pc, nxt_inst_mux_a, jmp_addr_last, jmp_reg, inst_out, inst_if, \
pc_id, pc_id_ex, if_id_write, reg_write_final = unsigned_signal_set(13)

imm_out, w_data, r_data1, r_data1_id_ex, r_data2, r_data2_id_ex, result, result_ex_mem, \
    result_mem_wb, op1_out, op2_out, op2_final, jmp_imm_id_ex, jmp_imm_shift, b_addr_out, \
    wdata_mem, read_data, read_data_mem_wb = signed_signal_set(18)

rs, rs_id_ex, rt, rt_id_ex, rd, rd_id_ex, rd_ex, rd_mem, rd_wb, w_addr \
    = unsigned_signal_set(10, width=5)

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
                       jmp_imm=imm_out,
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
                       mem_to_reg_out=mem_to_reg_id_ex,
                       jmp_imm_out=jmp_imm_id_ex)

    # TODO: CHECK THESE SIGNALS
    alu_mux_a = mux32bit3to1(ctrl_line=forward_a_out,
                             data1=r_data1_id_ex,
                             data2=result_ex_mem,
                             data3=result_mem_wb,
                             out=op1_out)
    alu_mux_b = mux32bit3to1(ctrl_line=forward_b_out,
                             data1=r_data2_id_ex,
                             data2=result_ex_mem,
                             data3=result_mem_wb,
                             out=op2_out)
    alu_mux_imm = mux32bit2to1(ctrl_line=alu_src_id_ex,
                               input1=op2_out,
                               input2=imm_out,
                               out=op2_final)

    alu_ = alu(op_1=op1_out,
               op_2=op2_final,
               alu_op=alu_op_id_ex,
               result=result,
               z=zero_flag)

    ex_mux_ = ex_mux(reg_dst=reg_dst_id_ex,
                     rt_in=rt_id_ex,
                     rd_in=rd_id_ex,
                     dest=rd_ex)

    forwarder = fwd_unit(rt_in=rt_id_ex,
                         rs_in=rs_id_ex,
                         ex_rd=rd_ex,
                         mem_rd=rd_mem,
                         mem_reg_write=reg_write_ex_mem,
                         wb_reg_write=reg_write_mem_wb,
                         forward_a=forward_a_out,
                         forward_b=forward_b_out)

    shifter = shift_unit(imm_in=jmp_imm_id_ex, imm_out=jmp_imm_shift)
    branch_adder_ = branch_adder(pc_in=pc_id_ex,
                                 imm_in=jmp_imm_shift,
                                 addr_out=b_addr_out)

    ex_mem_pipe = ex_mem(clock=clock,
                         branch_in=branch_id_ex,
                         mem_read_in=mem_read_id_ex,
                         mem_write_in=mem_write_id_ex,
                         reg_write_in=reg_write_id_ex,
                         mem_to_reg_in=mem_to_reg_id_ex,
                         jmp_addr=b_addr_out,
                         z_in=zero_flag,
                         result_in=result,
                         rt_in=op2_out,
                         reg_dst=rd_ex,
                         jmp_addr_out=imm_jmp_addr,
                         z_out=zero_flag_ex_mem,
                         result_out=result_ex_mem,
                         rt_out=wdata_mem,
                         branch_out=branch_ex_mem,
                         mem_read_out=mem_read_ex_mem,
                         mem_write_out=mem_write_ex_mem,
                         reg_write_out=reg_write_ex_mem,
                         mem_to_reg_out=mem_to_reg_ex_mem,
                         reg_dst_out=rd_mem)

    brancher = branch_unit(branch_ctrl=branch_ex_mem,
                           zero_in=zero_flag_ex_mem,
                           pc_src=pc_src)

    data_memory = data_mem(clk=clock,
                           read_wire=mem_read_ex_mem,
                           write_wire=mem_write_ex_mem,
                           address=result_ex_mem,
                           write_data=wdata_mem,
                           read_data=read_data)

    mem_wb_pipe = mem_wb(clk=clock,
                         reset=Signal(intbv()),
                         w_reg_ctl_in=reg_write_ex_mem,
                         mem_data_in=read_data,
                         alu_result_in=result_ex_mem,
                         w_reg_addr_in=rd_mem,
                         mem_to_reg=mem_to_reg_ex_mem,
                         mem_data_out=read_data_mem_wb,
                         alu_result_out=result_mem_wb,
                         w_reg_addr_out=rd_wb,
                         w_reg_ctl_out=reg_write_mem_wb,
                         mem_to_reg_out=mem_to_reg_mem_wb)

    wb_mux = mux32bit2to1(ctrl_line=mem_to_reg_mem_wb,
                          input1=read_data_mem_wb,
                          input2=result_mem_wb,
                          out=w_data)

    clock_inst = clock_gen(clock)

    return clock_inst, pc, pc_mux_a, pc_mux_b, pc_add, inst_memory, inst_mem_mux, if_id_pipe, \
        extender, registers, id_shifter, ctrl_unit, ctrl_gate, hzd, id_ex_pipe, alu_mux_a, \
        alu_mux_b, alu_mux_imm, alu_, ex_mux_, forwarder, shifter, branch_adder_, ex_mem_pipe, \
        brancher, data_memory, mem_wb_pipe, wb_mux



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
        # print("Cycle: {0}, PC: {1}, Op: {2}, Funct: {3}, J: {}, B: {}, MR: {}, MW: {}, AS: {}, "
        #       "RW: {}, RD: {}, MTR: {}, ALU: {}, result: {}, op1: {}, op2: {}")
        print("Cycle: {}, PC: {}, R1: {}, R2: {}, rs: {}, rt: {}, rd: {}, imm: {}, J: {}, B: {}, MR: {}, MW: {}, "
              "AS: {}, RW: {}, RD: {}, MTR: {}, ALU: {}, result: {}, op1: {}, op2: {}"
              # We are looking at values for 2 cycles ago
              .format(int(nxt_inst // 4) + 1 - 2,
                      bin(pc_id_ex, width=32), bin(r_data1_id_ex, width=32), bin(r_data2_id_ex, width=32),
                      bin(rs_id_ex, width=5), bin(rt_id_ex, width=5), bin(rd_id_ex, width=5),
                      bin(imm_id_ex, width=16), bin(jmp_ctrl), bin(branch_id_ex), bin(mem_read_id_ex),
                      bin(mem_write_id_ex), bin(alu_src_id_ex), bin(reg_write_id_ex), bin(reg_dst_id_ex),
                      bin(mem_to_reg_id_ex), bin(alu_op_id_ex, width=4), bin(result, width=32),
                      bin(op1_out), bin(op2_final)))


def monitor():
    """Monitoring output"""
    # TODO: make this work
    yield clock.negedge
    print("Inst: {}".format(intbv(nxt_inst)))


def main():
    """Run the simulation!!"""
    Simulation(top(), stim()).run(duration=975070)


if __name__ == '__main__':
    main()
