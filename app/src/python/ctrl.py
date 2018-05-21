"""Main Ctrl unit"""
from os import system

from myhdl import Cosimulation, always_comb, block


@block
def ctrl(funct_in, op_in, jump, branch, mem_read, mem_to_reg, mem_write, alu_src, reg_write,
         reg_dst, alu_op):
    """
    :param clock: system clock maybe
    :param funct_in: from if_id.funct_out
    :param op_in: This is a MIPS op code from IF_ID
    :param jump: 1 for jump. to inst_mem_mux.jmp_ctrl, pc_mux_b.jmp_ctrl
    :param branch: activate branch unit, to id_ex.branch_in
    :param alu_op: multi-bit alu op code.  see table. to id_ex.alu_op_in
    :param mem_read: activate read from memory, to id_ex.mem_read_in
    :param mem_to_reg: 0 for Alu result writeback, 1 for data writeback. to id_ex.mem_to_reg, 
        2 for data writeback of pc_next to register ra
    :param mem_write: activate to write to memory. to id_ex
    :param alu_src: 0 for register input, 1 for immediate. to id_ex.alu_src_in
    :param reg_write: activate to write to register.  to id_ex.reg_write_in
    :param reg_dst: 0 to write to Rt ([20:16]), 1 to write to Rd ([15:11]). to id_ex.reg_dst_in, 2 for ra register (pc_value)
    :param reset_out: 1 to insert a 1 cycle stall in the pipeline.  to if_id.reset_in
    :return: module logic
    """

    @always_comb
    def logic():
        if op_in == 35:
            # LOAD WORD
            jump.next = 0
            branch.next = 0
            mem_read.next = 1
            mem_to_reg.next = 1
            mem_write.next = 0
            alu_src.next = 1
            reg_write.next = 1
            reg_dst.next = 0
            alu_op.next = 1
        elif op_in == 43:
            # STORE WORD
            jump.next = 0
            branch.next = 0
            mem_read.next = 0
            mem_write.next = 1
            alu_src.next = 1
            reg_write.next = 0
            alu_op.next = 1
        elif op_in == 4:
            # BRANCH EQUALS
            alu_op.next = 0b0010
            jump.next = 0
            branch.next = 1
            mem_read.next = 0
            mem_write.next = 0
            alu_src.next = 0
            reg_write.next = 0
        # we may want to "reg_write" here and drop PC+4 value into the flow.
        elif op_in == 2:
            # JUMP
            jump.next = 1
            branch.next = 0
            mem_write.next = 0
            reg_write.next = 0
            mem_read.next = 0
            alu_src.next = 0
            alu_op.next = 0
        elif op_in == 3:
            # JAL
            jump.next = 1
            branch.next = 0
            mem_write.next = 0
            reg_write.next = 1
            mem_read.next = 0
            alu_src.next = 0
            alu_op.next = 0
            mem_to_reg.next = 2
            reg_dst.next = 2
        elif op_in == 25:
            # jr $ra
            jump.next = 0b10
            branch.next = 0
            mem_read.next = 0
            alu_src.next = 0
            reg_write.next = 0
            mem_write.next = 0
            alu_op.next = 0
        elif op_in == 8:
            # ADDI
            alu_op.next = 0b0001
            jump.next = 0
            branch.next = 0
            mem_read.next = 0
            mem_to_reg.next = 0
            mem_write.next = 0
            alu_src.next = 1
            reg_write.next = 1
            reg_dst.next = 0
        elif op_in == 24:
            # SUBI
            alu_op.next = 0b0010
            jump.next = 0
            branch.next = 0
            mem_read.next = 0
            mem_to_reg.next = 0
            mem_write.next = 0
            alu_src.next = 1
            reg_write.next = 1
            reg_dst.next = 0
        elif op_in == 0:
            # R STYLE INSTRUCTIONS
            jump.next = 0
            branch.next = 0
            mem_read.next = 0
            mem_to_reg.next = 0
            mem_write.next = 0
            alu_src.next = 0
            reg_write.next = 1
            reg_dst.next = 1

            if funct_in == 20:
                # ADD
                alu_op.next = 0b0001
            elif funct_in == 22:
                # SUB
                alu_op.next = 0b0010
            elif funct_in == 38:
                # XOR
                alu_op.next = 0b0011
            elif funct_in == 37:
                # OR
                alu_op.next = 0b0100
            elif funct_in == 36:
                # AND
                alu_op.next = 0b0101
            elif funct_in == 0:
                # SHIFT LEFT LOGICAL
                alu_op.next = 0b0110
            elif funct_in == 2:
                # SHIFT RIGHT LOGICAL
                alu_op.next = 0b0111
            elif funct_in == 39:
                # NOT OR
                alu_op.next = 0b1000
            elif funct_in == 42:
                # SET LESS THAN
                alu_op.next = 0b1001

    return logic


def ctrl_v(funct_in, op_in, jump, branch, mem_read, mem_to_reg, mem_write, alu_src,
           reg_write, reg_dst, alu_op):
    """
    Verilog logic
    :param kwargs: See above.
    :return: module logic
    """
    cmd = "iverilog -o bin/ctrl.out src/verilog/ctrl.v src/verilog/ctrl_tb.v"
    system(cmd)

    return Cosimulation("vvp -m lib/myhdl.vpi bin/ctrl.out",
                        funct_in=funct_in,
                        op_in=op_in,
                        jump=jump,
                        branch=branch,
                        mem_read=mem_read,
                        mem_to_reg=mem_to_reg,
                        mem_write=mem_write,
                        alu_src=alu_src,
                        reg_write=reg_write,
                        reg_dst=reg_dst,
                        alu_op=alu_op)
