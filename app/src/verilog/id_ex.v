`timescale 1ns/10ps

module id_ex (
    clock,
    reg_dst_in,
    reg_write_in,
    alu_src_in,
    mem_read_in,
    mem_write_in,
    mem_to_reg_in,
    alu_op_in,
    branch_in,
    r_data1,
    r_data2,
    rs,
    rt,
    rd,
    pc_value_in,
    imm,
    reg_dst_out,
    reg_write_out,
    alu_src_out,
    mem_read_out,
    mem_write_out,
    mem_to_reg_out,
    alu_op_out,
    branch_out,
    r_data1_out,
    r_data2_out,
    rs_out,
    rt_out,
    rd_out,
    pc_value_out,
    imm_out
);


input [0:0] clock;
input [1:0] reg_dst_in;
input [0:0] reg_write_in;
input [0:0] alu_src_in;
input [0:0] mem_read_in;
input [0:0] mem_write_in;
input [1:0] mem_to_reg_in;
input [3:0] alu_op_in;
input [0:0] branch_in;
input signed [31:0] r_data1;
input signed [31:0] r_data2;
input [4:0] rs;
input [4:0] rt;
input [4:0] rd;
input [31:0] pc_value_in;
input signed [15:0] imm;
output [1:0] reg_dst_out;
reg [1:0] reg_dst_out;
output [0:0] reg_write_out;
reg [0:0] reg_write_out;
output [0:0] alu_src_out;
reg [0:0] alu_src_out;
output [0:0] mem_read_out;
reg [0:0] mem_read_out;
output [0:0] mem_write_out;
reg [0:0] mem_write_out;
output [1:0] mem_to_reg_out;
reg [1:0] mem_to_reg_out;
output [3:0] alu_op_out;
reg [3:0] alu_op_out;
output [0:0] branch_out;
reg [0:0] branch_out;
output signed [31:0] r_data1_out;
reg signed [31:0] r_data1_out;
output signed [31:0] r_data2_out;
reg signed [31:0] r_data2_out;
output [4:0] rs_out;
reg [4:0] rs_out;
output [4:0] rt_out;
reg [4:0] rt_out;
output [4:0] rd_out;
reg [4:0] rd_out;
output [31:0] pc_value_out;
reg [31:0] pc_value_out;
output signed [31:0] imm_out;
reg signed [31:0] imm_out;



always @(posedge clock) begin: ID_EX_SEQ_LOGIC
    reg_dst_out <= reg_dst_in;
    reg_write_out <= reg_write_in;
    alu_src_out <= alu_src_in;
    mem_read_out <= mem_read_in;
    mem_write_out <= mem_write_in;
    mem_to_reg_out <= mem_to_reg_in;
    alu_op_out <= alu_op_in;
    branch_out <= branch_in;
    r_data1_out <= r_data1;
    r_data2_out <= r_data2;
    rs_out <= rs;
    rt_out <= rt;
    rd_out <= rd;
    pc_value_out <= pc_value_in;
    imm_out <= imm;
end

endmodule
