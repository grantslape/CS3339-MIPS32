module id_ex (
    input clk,
	input rst,
	
	//control
	input reg_dst_in,
	input reg_write_in,
	input alu_src_in,
	input mem_read_in,
	input mem_write_in,
	input memto_reg_in,
	input [1:0] alu_op_in,
	input branch_in,
	
	input [31:0] rs_in,
	input [31:0] rt_in,
	input [31:0] rd_in,
	input [31:0] pc_value_in, 
	input [31:0] im_in,
	
    output reg_dst_out,
	output reg_write_out,
	output alu_src_out,
	output mem_read_out,
	output mem_write_out,
	output memto_reg_out,
	output [1:0] alu_op_out,
	output branch_out,
	
	output [31:0] rs_out,
	output [31:0] rt_out,
	output [31:0] rd_out,
	output [31:0] pc_value_out, 
	output [31:0] im_out
	);
	
	reg reg_dst_out;
	reg reg_write_out;
	reg alu_src_out;
	reg mem_read_out;
	reg mem_write_out;
	reg memto_reg_out;
	reg [1:0] alu_op_out;
	reg branch_out;
	
	reg [31:0] rs_out;
	reg [31:0] rt_out;
	reg [31:0] rd_out;
	reg [31:0] pc_value_out; 
	reg [31:0] im_out;
	
	always@(negedge rst or posedge clk)begin
	    if(rst==0)begin
		    reg_dst_out <= 0;
            reg_write_out <= 0;
			alu_src_out <= 0;
			mem_read_out <= 0;
			mem_write_out <= 0;
			memto_reg_out <= 0;
			alu_op_out <= 0;
			branch_out <= 0;
			
			rs_out <= 0;
			rt_out <= 0;
			rd_out <= 0;
			pc_value_out <= 0;
			im_out <= 0;
		end else begin
		    reg_dst_out <= reg_dst_in;
            reg_write_out <= reg_write_in;
			alu_src_out <= alu_src_in;
			mem_read_out <= mem_read_in;
			mem_write_out <= mem_write_in;
			memto_reg_out <= memto_reg_in;
			alu_op_out <= alu_op_in;
			branch_out <= branch_in;
			
			rs_out <= rs_in;
			rt_out <= rt_in;
			rd_out <= rd_in;
			pc_value_out <= pc_value_in;
			im_out <= im_in;			
		end
	end
	

endmodule