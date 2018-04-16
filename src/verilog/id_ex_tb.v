module tb_id_ex;

    reg clk;
	reg rst;
	
	//control
	reg reg_dst_in;
	reg reg_write_in;
	reg alu_src_in;
	reg mem_read_in;
	reg mem_write_in;
	reg memto_reg_in;
	reg [1:0] alu_op_in;
	reg branch_in;
	
	reg [31:0] rs_in;
	reg [31:0] rt_in;
	reg [31:0] rd_in;
	reg [31:0] pc_value_in; 
	reg [31:0] im_in;
	
	
	wire reg_dst_out;
	wire reg_write_out;
	wire alu_src_out;
	wire mem_read_out;
	wire mem_write_out;
	wire memto_reg_out;
	wire [1:0] alu_op_out;
	wire branch_out;
	
	wire [31:0] rs_out;
	wire [31:0] rt_out;
	wire [31:0] rd_out;
	wire [31:0] pc_value_out; 
	wire [31:0] im_out;
	
	initial begin
	    $from_myhdl(
		    clk,
	        rst,
	
	        //control
	        reg_dst_in,
	        reg_write_in,
	        alu_src_in,
	        mem_read_in,
	        mem_write_in,
	        memto_reg_in,
	        alu_op_in,
	        branch_in,
	
	        rs_in,
	        rt_in,
	        rd_in,
	        pc_value_in, 
	        im_in
		);
		
		$to_myhdl(
		    reg_dst_out,
		    reg_write_out,
		    alu_src_out,
		    mem_read_out,
		    mem_write_out,
		    memto_reg_out,
		    [alu_op_out,
		    branch_out,
	
		    rs_out,
		    rt_out,
		    rd_out,
		    pc_value_out, 
		    im_out
		);
	end

endmodule