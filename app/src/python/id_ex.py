from os import system
from myhdl import Cosimulation, always, block


@block
def id_ex(clock, reg_dst_in, reg_write_in, alu_src_in, mem_read_in, mem_write_in, mem_to_reg_in, alu_op_in,
          branch_in, r_data1, r_data2, rs, rt, rd, pc_value_in, imm, reg_dst_out, reg_write_out, alu_src_out,
          mem_read_out, mem_write_out, mem_to_reg_out, alu_op_out, branch_out, r_data1_out, r_data2_out, rs_out, rt_out,
          rd_out, pc_value_out, imm_out):
    @always(clock.posedge)
    def seq_logic():
        reg_dst_out.next = reg_dst_in
        reg_write_out.next = reg_write_in
        alu_src_out.next = alu_src_in
        mem_read_out.next = mem_read_in
        mem_write_out.next = mem_write_in
        mem_to_reg_out.next = mem_to_reg_in
        alu_op_out.next = alu_op_in
        branch_out.next = branch_in
        r_data1_out.next = r_data1
        r_data2_out.next = r_data2
        rs_out.next = rs
        rt_out.next = rt
        rd_out.next = rd
        pc_value_out.next = pc_value_in
        imm_out.next = imm

    return seq_logic


def id_ex_v(clock, reg_dst_in, reg_write_in, alu_src_in, mem_read_in, mem_write_in, mem_to_reg_in, alu_op_in,
            branch_in, r_data1, r_data2, rs, rt, rd, pc_value_in, imm, reg_dst_out, reg_write_out, alu_src_out,
            mem_read_out, mem_write_out, mem_to_reg_out, alu_op_out, branch_out, r_data1_out, r_data2_out, rs_out,
            rt_out, rd_out, pc_value_out, imm_out):
    cmd = "iverilog -o bin/id_ex.out src/verilog/id_ex.v src/verilog/id_ex_tb.v"
    system(cmd)

    return Cosimulation("vvp -m lib/myhdl.vpi bin/id_ex.out",
                        clock=clock,
                        reg_dst_in=reg_dst_in,
                        reg_write_in=reg_write_in,
                        alu_src_in=alu_src_in,
                        mem_read_in=mem_read_in,
                        mem_write_in=mem_write_in,
                        mem_to_reg_in=mem_to_reg_in,
                        alu_op_in=alu_op_in,
                        branch_in=branch_in,
                        r_data1=r_data1,
                        r_data2=r_data2,
                        rs=rs,
                        rt=rt,
                        rd=rd,
                        pc_value_in=pc_value_in,
                        imm=imm,
                        reg_dst_out=reg_dst_out,
                        reg_write_out=reg_write_out,
                        alu_src_out=alu_src_out,
                        mem_read_out=mem_read_out,
                        mem_write_out=mem_write_out,
                        mem_to_reg_out=mem_to_reg_out,
                        alu_op_out=alu_op_out,
                        branch_out=branch_out,
                        r_data1_out=r_data1_out,
                        r_data2_out=r_data2_out,
                        rs_out=rs_out,
                        rt_out=rt_out,
                        rd_out=rd_out,
                        pc_value_out=pc_value_out,
                        imm_out=imm_out)
