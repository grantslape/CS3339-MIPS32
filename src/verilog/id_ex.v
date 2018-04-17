module id_ex (
    input clock,
	input reset_in,
	
	//control
	input reg_dst_in,
	input reg_write_in,
	input alu_src_in,
	input mem_read_in,
	input mem_write_in,
	input mem_to_reg_in,
	input [1:0] alu_op_in,
	input branch_in,
	
	input [31:0] r_data1,
	input [31:0] r_data2,
	input [4:0] rs,
	input [4:0] rt,
	input [4:0] rd,
	input [31:0] pc_value_in, 
	input [31:0] imm,
	
    output reg_dst_out,
	output reg_write_out,
	output alu_src_out,
	output mem_read_out,
	output mem_write_out,
	output mem_to_reg_out,
	output [1:0] alu_op_out,
	output branch_out,
	
	output [31:0] r_data1_out,
	output [31:0] r_data2_out,
	output [4:0] rs_out,
	output [4:0] rt_out,
	output [4:0] rd_out,
	output [31:0] pc_value_out, 
	output [31:0] imm_out
	);
	
	reg reg_dst_out;
	reg reg_write_out;
	reg alu_src_out;
	reg mem_read_out;
	reg mem_write_out;
	reg mem_to_reg_out;
	reg [1:0] alu_op_out;
	reg branch_out;
	
	reg [31:0] r_data1_out;
	reg [31:0] r_data2_out;
	reg [4:0] rs_out;
	reg [4:0] rt_out;
	reg [4:0] rd_out;
	reg [31:0] pc_value_out; 
	reg [31:0] imm_out;
	
	always@(negedge reset_in or posedge clock)begin
	    if(reset_in==0)begin
		    reg_dst_out <= 0;
            reg_write_out <= 0;
			alu_src_out <= 0;
			mem_read_out <= 0;
			mem_write_out <= 0;
			mem_to_reg_out <= 0;
			alu_op_out <= 0;
			branch_out <= 0;
			
			r_data1_out <= 0;
			r_data2_out <= 0;
			rs_out <= 0;
			rt_out <= 0;
			rd_out <= 0;
			pc_value_out <= 0;
			imm_out <= 0;
		end else begin
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
	end
	

endmodule