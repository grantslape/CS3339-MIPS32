module tb_id_ex;

    reg clock;
	reg reset_in;
	
	//control
	reg reg_dst_in;
	reg reg_write_in;
	reg alu_src_in;
	reg mem_read_in;
	reg mem_write_in;
	reg mem_to_reg_in;
	reg [1:0] alu_op_in;
	reg branch_in;
	
	reg [31:0] r_data1;
	reg [31:0] r_data2;
	reg [4:0] rs;
	reg [4:0] rt;
	reg [4:0] rd;
	reg [31:0] pc_value_in; 
	reg [31:0] imm;
	
    wire reg_dst_out;
	wire reg_write_out;
	wire alu_src_out;
	wire mem_read_out;
	wire mem_write_out;
	wire mem_to_reg_out;
	wire [1:0] alu_op_out;
	wire branch_out;
	
	wire [31:0] r_data1_out;
	wire [31:0] r_data2_out;
	wire [4:0] rs_out;
	wire [4:0] rt_out;
	wire [4:0] rd_out;
	wire [31:0] pc_value_out; 
	wire [31:0] imm_out;

	initial begin
	    $from_myhdl(
		    clock,
			reset_in,
	
			//control
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
			imm
		);
		
		$to_myhdl(
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
	end

endmodule