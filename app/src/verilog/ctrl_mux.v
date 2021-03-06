`timescale 1ns/10ps

module ctrl_mux (
    ex_stall,
    jump,
    branch,
    mem_read,
    mem_to_reg,
    mem_write,
    alu_src,
    reg_write,
    reg_dst,
    alu_op,
    jump_out,
    branch_out,
    mem_read_out,
    mem_to_reg_out,
    mem_write_out,
    alu_src_out,
    reg_write_out,
    reg_dst_out,
    alu_op_out
);
// Ctrl multiplexer
// :param ex_stall:
// :param jump:
// :param branch:
// :param mem_read:
// :param mem_to_reg:
// :param mem_write:
// :param alu_src:
// :param reg_write:
// :param reg_dst:
// :param alu_op:
// :param jump_out:
// :param branch_out:
// :param mem_read_out:
// :param mem_to_reg_out:
// :param mem_write_out:
// :param alu_src_out:
// :param reg_write_out:
// :param reg_dst_out:
// :param alu_op_out:
// :return: module logic

input [0:0] ex_stall;
input [1:0] jump;
input [0:0] branch;
input [0:0] mem_read;
input [1:0] mem_to_reg;
input [0:0] mem_write;
input [0:0] alu_src;
input [0:0] reg_write;
input [1:0] reg_dst;
input [3:0] alu_op;
output [1:0] jump_out;
reg [1:0] jump_out;
output [0:0] branch_out;
reg [0:0] branch_out;
output [0:0] mem_read_out;
reg [0:0] mem_read_out;
output [1:0] mem_to_reg_out;
reg [1:0] mem_to_reg_out;
output [0:0] mem_write_out;
reg [0:0] mem_write_out;
output [0:0] alu_src_out;
reg [0:0] alu_src_out;
output [0:0] reg_write_out;
reg [0:0] reg_write_out;
output [1:0] reg_dst_out;
reg [1:0] reg_dst_out;
output [3:0] alu_op_out;
reg [3:0] alu_op_out;






always @(mem_to_reg, reg_dst, alu_op, mem_write, reg_write, jump, alu_src, mem_read, branch, ex_stall) begin: CTRL_MUX_LOGIC
    if ((ex_stall == 1)) begin
        jump_out = 0;
        branch_out = 0;
        mem_read_out = 0;
        mem_to_reg_out = 0;
        mem_write_out = 0;
        alu_src_out = 0;
        reg_write_out = 0;
        reg_dst_out = 0;
        alu_op_out = 0;
    end
    else begin
        jump_out = jump;
        branch_out = branch;
        mem_read_out = mem_read;
        mem_to_reg_out = mem_to_reg;
        mem_write_out = mem_write;
        alu_src_out = alu_src;
        reg_write_out = reg_write;
        reg_dst_out = reg_dst;
        alu_op_out = alu_op;
    end
end

endmodule
