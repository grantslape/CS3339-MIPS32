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
from __future__ import print_function
from os import system
from myhdl import Simulation, bin, StopSimulation, ResetSignal, join, toVerilog, instance, instances, Cosimulation, \
    delay

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
from src.commons.clock import clock_gen, half_period
from src.commons.settings import settings as sf
from src.commons.signal_generator import *

clock, pc_src, reset_ctrl, branch_ctrl, branch_gate, branch_id_ex, \
    branch_ex_mem, mem_read_ctrl, mem_read_gate, mem_read_ex_mem, mem_write_ctrl, \
    mem_read_id_ex, mem_write_gate, mem_write_id_ex, mem_write_ex_mem, alu_src_ctrl, alu_src_gate, \
    alu_src_id_ex, reg_write_ctrl, reg_write_gate, reg_write_id_ex, reg_write_ex_mem, \
    ex_stall, zero_flag, \
    zero_flag_ex_mem, pc_write \
    = unsigned_signal_set(26, width=1)

cur_pc = Signal(unsigned_intbv())

mem_to_reg_ctrl, mem_to_reg_gate, mem_to_reg_id_ex, mem_to_reg_ex_mem, mem_to_reg_mem_wb, \
    forward_a_out, forward_b_out, reg_dst_ctrl, reg_dst_gate, reg_dst_id_ex, jmp_ctrl, jump_gate \
    = unsigned_signal_set(12, width=2)

nxt_pc, nxt_inst_mux_a, jmp_addr_last, inst_out, inst_if, \
pc_id, pc_id_ex, pc_value_ex_mem, pc_value_mem_wb, if_id_write, reg_write_final, nxt_inst, ZERO = \
    unsigned_signal_set(13)

imm_out, w_data, r_data1, r_data1_id_ex, r_data2, r_data2_id_ex, result, result_ex_mem, \
    result_mem_wb, op1_out, op2_out, op2_final, jmp_imm_id_ex, jmp_imm_shift, b_addr_out, \
    wdata_mem, read_data, read_data_mem_wb, imm_jmp_addr = signed_signal_set(19)

rs, rs_id_ex, rt, rt_id_ex, rd, rd_id_ex, rd_ex, rd_mem, rd_wb, w_addr \
    = unsigned_signal_set(10, width=5)

alu_op_code, alu_op_gate, alu_op_id_ex = unsigned_signal_set(3, width=sf['ALU_CODE_SIZE'])

imm, imm_id_ex = [
    Signal(intbv(min=sf['16_SIGNED_MIN_VALUE'], max=sf['16_SIGNED_MAX_VALUE'])) for _ in range(2)
]
top4 = Signal(unsigned_intbv(width=4))
target_out = Signal(unsigned_intbv(width=26))
op_code, funct_out = unsigned_signal_set(2, width=6)

pc_src_v, reset_ctrl_v, branch_ctrl_v, branch_gate_v, branch_id_ex_v, \
    branch_ex_mem_v, mem_read_ctrl_v, mem_read_gate_v, mem_read_ex_mem_v, mem_write_ctrl_v, \
    mem_read_id_ex_v, mem_write_gate_v, mem_write_id_ex_v, mem_write_ex_mem_v, alu_src_ctrl_v, alu_src_gate_v, \
    alu_src_id_ex_v, reg_write_ctrl_v, reg_write_gate_v, reg_write_id_ex_v, reg_write_ex_mem_v, \
    ex_stall_v, zero_flag_v, \
    zero_flag_ex_mem_v, pc_write_v \
    = unsigned_signal_set(25, width=1)

cur_pc_v = Signal(unsigned_intbv())

mem_to_reg_ctrl_v, mem_to_reg_gate_v, mem_to_reg_id_ex_v, mem_to_reg_ex_mem_v, mem_to_reg_mem_wb_v, \
    forward_a_out_v, forward_b_out_v, reg_dst_ctrl_v, reg_dst_gate_v, reg_dst_id_ex_v, jmp_ctrl_v, jump_gate_v \
    = unsigned_signal_set(12, width=2)

nxt_pc_v, nxt_inst_mux_a_v, jmp_addr_last_v, inst_out_v, inst_if_v, \
pc_id_v, pc_id_ex_v, pc_value_ex_mem_v, pc_value_mem_wb_v, if_id_write_v, reg_write_final_v, nxt_inst_v, ZERO_v = \
    unsigned_signal_set(13)

imm_out_v, w_data_v, r_data1_v, r_data1_id_ex_v, r_data2_v, r_data2_id_ex_v, result_v, result_ex_mem_v, \
    result_mem_wb_v, op1_out_v, op2_out_v, op2_final_v, jmp_imm_id_ex_v, jmp_imm_shift_v, b_addr_out_v, \
    wdata_mem_v, read_data_v, read_data_mem_wb_v, imm_jmp_addr_v = signed_signal_set(19)

rs_v, rs_id_ex_v, rt_v, rt_id_ex_v, rd_v, rd_id_ex_v, rd_ex_v, rd_mem_v, rd_wb_v, w_addr_v \
    = unsigned_signal_set(10, width=5)

alu_op_code_v, alu_op_gate_v, alu_op_id_ex_v = unsigned_signal_set(3, width=sf['ALU_CODE_SIZE'])

imm_v, imm_id_ex_v = [
    Signal(intbv(min=sf['16_SIGNED_MIN_VALUE'], max=sf['16_SIGNED_MAX_VALUE'])) for _ in range(2)
]
top4_v = Signal(unsigned_intbv(width=4))
target_out_v = Signal(unsigned_intbv(width=26))
op_code_v, funct_out_v = unsigned_signal_set(2, width=6)


def top_v():
    """Instantiate Verilog design"""
    cmd = "iverilog -o bin/mips.out -Ptop_tb.TBSIZE={} src/verilog/top.v src/verilog/top_tb.v".format(2 ** sf['MEMORY_WIDTH'])
    system(cmd)

    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/mips.out",
                        clock=clock,
                        pc_src=pc_src_v,
                        reset_ctrl=reset_ctrl_v,
                        branch_ctrl=branch_ctrl_v,
                        branch_gate=branch_gate_v,
                        branch_id_ex=branch_id_ex_v,
                        branch_ex_mem=branch_ex_mem_v,
                        mem_read_ctrl=mem_read_ctrl_v,
                        mem_read_gate=mem_read_gate_v,
                        mem_read_ex_mem=mem_read_ex_mem_v,
                        mem_write_ctrl=mem_write_ctrl_v,
                        mem_read_id_ex=mem_read_id_ex_v,
                        mem_write_gate=mem_write_gate_v,
                        mem_write_id_ex=mem_write_id_ex_v,
                        mem_write_ex_mem=mem_write_ex_mem,
                        alu_src_ctrl=alu_src_ctrl_v,
                        alu_src_gate=alu_src_gate_v,
                        alu_src_id_ex=alu_src_id_ex_v,
                        reg_write_ctrl=reg_write_ctrl_v,
                        reg_write_gate=reg_write_gate_v,
                        reg_write_id_ex=reg_write_id_ex_v,
                        reg_write_ex_mem=reg_write_ex_mem_v,
                        forward_a_out=forward_a_out_v,
                        forward_b_out=forward_b_out_v,
                        reg_dst_ctrl=reg_dst_ctrl_v,
                        reg_dst_gate=reg_dst_gate_v,
                        reg_dst_id_ex=reg_dst_id_ex_v,
                        jmp_ctrl=jmp_ctrl_v,
                        jump_gate=jump_gate_v,
                        nxt_pc=nxt_pc_v,
                        nxt_inst_mux_a=nxt_inst_mux_a_v,
                        jmp_addr_last=jmp_addr_last_v,
                        inst_out=inst_out_v,
                        inst_if=inst_if_v,
                        pc_id=pc_id_v,
                        pc_id_ex=pc_id_ex_v,
                        pc_value_ex_mem=pc_value_ex_mem_v,
                        pc_value_mem_wb=pc_value_mem_wb_v,
                        if_id_write=if_id_write,
                        reg_write_final=reg_write_final,
                        nxt_inst=nxt_inst,
                        imm_out=imm_out_v,
                        w_data=w_data_v,
                        r_data1=r_data1_v,
                        r_data1_id_ex=r_data1_id_ex_v,
                        r_data2=r_data2_v,
                        r_data2_id_ex=r_data2_id_ex_v,
                        result=result_v,
                        result_ex_mem=result_ex_mem_v,
                        result_mem_wb=result_mem_wb_v,
                        op1_out=op1_out_v,
                        op2_out=op2_out_v,
                        op2_final=op2_final_v,
                        jmp_imm_id_ex=jmp_imm_id_ex_v,
                        jmp_imm_shift=jmp_imm_shift_v,
                        b_addr_out=b_addr_out_v,
                        wdata_mem=wdata_mem_v,
                        read_data=read_data_v,
                        read_data_mem_wb=read_data_mem_wb_v,
                        imm_jmp_addr=imm_jmp_addr_v,
                        rs=rs_v,
                        rs_id_ex=rs_id_ex_v,
                        rt=rt_v,
                        rt_id_ex=rt_id_ex_v,
                        rd=rd_v,
                        rd_id_ex=rd_id_ex_v,
                        rd_ex=rd_ex_v,
                        rd_mem=rd_mem_v,
                        w_addr=w_addr_v,
                        alu_op_code=alu_op_code_v,
                        alu_op_gate=alu_op_gate_v,
                        alu_op_id_ex=alu_op_id_ex_v,
                        imm=imm_v,
                        imm_id_ex=imm_id_ex_v,
                        top4=top4_v,
                        target_out=target_out_v,
                        op_code=op_code_v,
                        funct_out=funct_out_v,
                        ZERO=ZERO_v,
                        ex_stall=ex_stall_v,
                        zero_flag=zero_flag_v,
                        zero_flag_ex_mem=zero_flag_ex_mem_v,
                        cur_pc=cur_pc_v,
                        pc_write=pc_write_v,
                        mem_to_reg_ctrl=mem_to_reg_ctrl_v,
                        mem_to_reg_gate=mem_to_reg_gate_v,
                        mem_to_reg_id_ex=mem_to_reg_id_ex_v,
                        mem_to_reg_ex_mem=mem_to_reg_ex_mem_v,
                        mem_to_reg_mem_wb=mem_to_reg_mem_wb_v)


def top(clock, pc_src, reset_ctrl, branch_ctrl, branch_gate, branch_id_ex,
    branch_ex_mem, mem_read_ctrl, mem_read_gate, mem_read_ex_mem, mem_write_ctrl,
    mem_read_id_ex, mem_write_gate, mem_write_id_ex, mem_write_ex_mem, alu_src_ctrl, alu_src_gate,
    alu_src_id_ex, reg_write_ctrl, reg_write_gate, reg_write_id_ex, reg_write_ex_mem,
    ex_stall, zero_flag, zero_flag_ex_mem, pc_write, cur_pc, mem_to_reg_ctrl, mem_to_reg_gate, mem_to_reg_id_ex, mem_to_reg_ex_mem, mem_to_reg_mem_wb,
    forward_a_out, forward_b_out, reg_dst_ctrl, reg_dst_gate, reg_dst_id_ex, jmp_ctrl, jump_gate, nxt_pc, nxt_inst_mux_a, jmp_addr_last, inst_out, inst_if, pc_id, pc_id_ex, pc_value_ex_mem, pc_value_mem_wb, if_id_write, reg_write_final, nxt_inst, imm_out, w_data, r_data1, r_data1_id_ex, r_data2, r_data2_id_ex, result, result_ex_mem,
    result_mem_wb, op1_out, op2_out, op2_final, jmp_imm_id_ex, jmp_imm_shift, b_addr_out, wdata_mem, read_data, read_data_mem_wb, imm_jmp_addr, rs, rs_id_ex, rt, rt_id_ex, rd, rd_id_ex, rd_ex, rd_mem, w_addr, alu_op_code, alu_op_gate, alu_op_id_ex, imm, imm_id_ex, top4, target_out, op_code, funct_out, ZERO):
    """Instantiate modules"""
    pc = program_counter(clock=clock, pc_write=pc_write, nxt_inst=nxt_inst, cur_pc=cur_pc)
    pc_mux_a = mux32bit2to1(ctrl_line=pc_src,
                            input1=nxt_pc,
                            input2=imm_jmp_addr,
                            out=nxt_inst_mux_a)

    # Our JR format is 01100111111000000000000000000000, so we just need r_data1 to go to data3
    # would we be calling rfile under certain conditions inside of main? yes
    pc_mux_b = mux32bit3to1(ctrl_line=jmp_ctrl,
                            data1=nxt_inst_mux_a,
                            data2=jmp_addr_last,
                            data3=r_data1,
                            out=nxt_inst)

    pc_add = pc_adder(cur_pc=cur_pc,
                      next_pc=nxt_pc)

    inst_memory = inst_mem(inst_reg=cur_pc,
                           inst_out=inst_out)

    inst_mem_mux = mux32bit2to1(ctrl_line=jmp_ctrl,
                                input1=inst_out,
                                input2=ZERO,
                                out=inst_if)

    if_id_pipe = if_id(if_id_write=if_id_write,
                       clock=clock,
                       nxt_pc=nxt_pc,
                       inst_in=inst_if,
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

    registers = rfile(clock=clock,
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

    ctrl_unit = ctrl(funct_in=funct_out,
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
                         wb_reg_write=reg_write_final,
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
                         reg_dst_in=rd_ex,
                         jmp_addr_out=imm_jmp_addr,
                         z_out=zero_flag_ex_mem,
                         result_out=result_ex_mem,
                         rt_out=wdata_mem,
                         branch_out=branch_ex_mem,
                         mem_read_out=mem_read_ex_mem,
                         mem_write_out=mem_write_ex_mem,
                         reg_write_out=reg_write_ex_mem,
                         mem_to_reg_out=mem_to_reg_ex_mem,
                         reg_dst_out=rd_mem,
                         pc_value_in=pc_id_ex,
                         pc_value_out=pc_value_ex_mem)

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
                         w_reg_ctl_in=reg_write_ex_mem,
                         mem_data_in=read_data,
                         alu_result_in=result_ex_mem,
                         w_reg_addr_in=rd_mem,
                         mem_to_reg_in=mem_to_reg_ex_mem,
                         mem_data_out=read_data_mem_wb,
                         alu_result_out=result_mem_wb,
                         w_reg_addr_out=w_addr,
                         w_reg_ctl_out=reg_write_final,
                         mem_to_reg_out=mem_to_reg_mem_wb,
                         pc_value_in=pc_value_ex_mem,
                         pc_value_out=pc_value_mem_wb)

    wb_mux = mux32bit3to1(ctrl_line=mem_to_reg_mem_wb,
                          data1=read_data_mem_wb,
                          data2=result_mem_wb,
                          data3=pc_value_mem_wb,
                          out=w_data)

    return instances()


def stim(start):
    """Test stimulus"""
    cur_pc.next = start
    cur_pc_v.next = start
    cycle = 1
    while 1:
        yield clock.posedge
        print("\nCYCLE: {}".format(cycle))
        print("IF STAGE: CurPC: {}, NxtPC: {}\n CurInst: {}"
              .format(int(cur_pc), int(nxt_inst), bin(inst_out, width=32)))
        print("MUX A: psrc: {}, nxt_pc: {}, imm_jmp_addr: {}, out: {}"
              .format(bool(pc_src), int(nxt_pc), int(imm_jmp_addr), int(nxt_inst_mux_a)))
        print("MUX B: jctrl: {}, input: {}, jmp_addr: {}, jmp_reg: {} out: {}\n"
              .format(bin(jmp_ctrl), int(nxt_inst_mux_a), int(jmp_addr_last), int(r_data1), int(nxt_inst)))

        print("ID STAGE: ({}): stall: {}, Flush: {}, op_code: {}, rs: {}, rt: {}, rd:{}, funct_out: {}, top4: {} pc_out: {}\ntarget_out: {}, int: {}\n"
              .format(cycle-1, bool(if_id_write), bool(reset_ctrl), bin(op_code, width=6), bin(rs, width=5), bin(rt, width=5),
                      bin(rd, width=5), bin(funct_out, width=6), bin(top4, width=4),
                      int(pc_id), bin(jmp_addr_last, width=32), int(jmp_addr_last)))

        print("RFILE-READ: R1: {}, R2: {}; WRITE ({}): WADDR: {}, WDATA: {}"
              .format(int(r_data1), int(r_data2), cycle-4, bin(w_addr, width=5), int(w_data)))
        # print("CTRL: jmp: {}, branch: {}, mem_read: {}, mem_to_reg: {}. mem_write: {}, alu_src: {}, reg_write: {}. reg_dst: {}, reset_out: {}"
        #       .format(int(jmp_ctrl), bool(branch_ctrl), bool(mem_read_ctrl), int(mem_to_reg_ctrl), bool(mem_write_ctrl), bool(alu_src_ctrl), bool(reg_write_ctrl), int(reg_dst_ctrl), bool(reset_ctrl)))

        print("EX STAGE: ({}): ALU_OP: {} RD1: {}, RD2: {}, RS: {}, RT: {}, RD: {}, PC: {}"
              .format(cycle-2, bin(alu_op_id_ex, width=4), int(r_data1_id_ex), int(r_data2_id_ex), bin(rs_id_ex, width=5),
                      bin(rt_id_ex, width=5), bin(rd_id_ex, width=5), int(pc_id_ex)))

        print("ctrls: branch: {}, mem_read: {}, mem_write: {}, alu_src: {}, reg_write: {}, reg_dst: {}, mem_to_reg: {}\n"
              .format(bool(branch_id_ex), bool(mem_read_id_ex), bool(mem_write_id_ex), bool(alu_src_id_ex),
                      bool(reg_write_id_ex), int(reg_dst_id_ex), int(mem_to_reg_id_ex)))

        print("MEM STAGE: ({}): Result: {}, RT: {}, Z: {}, b_addr: {}"
              .format(cycle-3, int(result), int(wdata_mem), bool(zero_flag_ex_mem), bin(imm_jmp_addr, width=32)))
        print("ctrl: branch: {}, mem_read: {}, mem_write: {}, reg_write: {}, reg_dst: {}, mem_to_reg: {}\n"
              .format(bool(branch_ex_mem), bool(mem_read_ex_mem), bool(mem_write_ex_mem),
                      bool(reg_write_final), bin(rd_mem, width=5), int(mem_to_reg_ex_mem)))

        print ("WB_STAGE: ({}): mem_data: {}, result: {}, wreg: {}, pc_out: {}"
               .format(cycle-4, int(read_data_mem_wb), int(result_mem_wb), bin(w_addr, width=5), int(pc_value_mem_wb)))
        print("wb_mux: ctrl: {}, input1: {}, input2: {}, input3: {}, out: {}\n"
              .format(int(mem_to_reg_mem_wb), int(read_data_mem_wb), int(result_mem_wb), int(pc_value_mem_wb), int(w_data)))
        cycle += 1


def convert():
    return toVerilog(top, clock, pc_src, reset_ctrl, branch_ctrl, branch_gate, branch_id_ex,
    branch_ex_mem, mem_read_ctrl, mem_read_gate, mem_read_ex_mem, mem_write_ctrl,
    mem_read_id_ex, mem_write_gate, mem_write_id_ex, mem_write_ex_mem, alu_src_ctrl, alu_src_gate,
    alu_src_id_ex, reg_write_ctrl, reg_write_gate, reg_write_id_ex, reg_write_ex_mem,
    ex_stall, zero_flag, zero_flag_ex_mem, pc_write, cur_pc, mem_to_reg_ctrl, mem_to_reg_gate, mem_to_reg_id_ex, mem_to_reg_ex_mem, mem_to_reg_mem_wb,
    forward_a_out, forward_b_out, reg_dst_ctrl, reg_dst_gate, reg_dst_id_ex, jmp_ctrl, jump_gate, nxt_pc, nxt_inst_mux_a, jmp_addr_last, inst_out, inst_if, pc_id, pc_id_ex, pc_value_ex_mem, pc_value_mem_wb, if_id_write, reg_write_final, nxt_inst, imm_out, w_data, r_data1, r_data1_id_ex, r_data2, r_data2_id_ex, result, result_ex_mem,
    result_mem_wb, op1_out, op2_out, op2_final, jmp_imm_id_ex, jmp_imm_shift, b_addr_out, wdata_mem, read_data, read_data_mem_wb, imm_jmp_addr, rs, rs_id_ex, rt, rt_id_ex, rd, rd_id_ex, rd_ex, rd_mem, w_addr, alu_op_code, alu_op_gate, alu_op_id_ex, imm, imm_id_ex, top4, target_out, op_code, funct_out, ZERO)


def getDUT():
    return top(clock, pc_src, reset_ctrl, branch_ctrl, branch_gate, branch_id_ex,
               branch_ex_mem, mem_read_ctrl, mem_read_gate, mem_read_ex_mem, mem_write_ctrl,
               mem_read_id_ex, mem_write_gate, mem_write_id_ex, mem_write_ex_mem, alu_src_ctrl, alu_src_gate,
               alu_src_id_ex, reg_write_ctrl, reg_write_gate, reg_write_id_ex, reg_write_ex_mem,
               ex_stall, zero_flag, zero_flag_ex_mem, pc_write, cur_pc, mem_to_reg_ctrl, mem_to_reg_gate, mem_to_reg_id_ex, mem_to_reg_ex_mem, mem_to_reg_mem_wb,
               forward_a_out, forward_b_out, reg_dst_ctrl, reg_dst_gate, reg_dst_id_ex, jmp_ctrl, jump_gate, nxt_pc, nxt_inst_mux_a, jmp_addr_last, inst_out, inst_if, pc_id, pc_id_ex, pc_value_ex_mem, pc_value_mem_wb, if_id_write, reg_write_final, nxt_inst, imm_out, w_data, r_data1, r_data1_id_ex, r_data2, r_data2_id_ex, result, result_ex_mem,
               result_mem_wb, op1_out, op2_out, op2_final, jmp_imm_id_ex, jmp_imm_shift, b_addr_out, wdata_mem, read_data, read_data_mem_wb, imm_jmp_addr, rs, rs_id_ex, rt, rt_id_ex, rd, rd_id_ex, rd_ex, rd_mem, w_addr, alu_op_code, alu_op_gate, alu_op_id_ex, imm, imm_id_ex, top4, target_out, op_code, funct_out, ZERO)


def main():
    """Run the simulation!!"""
    start = int(input("starting PC Value: "))
    clock_inst = clock_gen(clock)
    print("Loading Instructions...")

    # TODO: Why does Verilog not function properly?
    sim = Simulation(getDUT(), stim(start), clock_inst)
    while 1:
        length = int(raw_input("How many clock cycles to run for?: "))
        sim.run(duration=length)


if __name__ == '__main__':
    main()
