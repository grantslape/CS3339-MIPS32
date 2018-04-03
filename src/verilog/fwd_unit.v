`timescale 1ns/10ps

module fwd_unit(
	rt_in, rs_in,
	ex_rd, mem_rd,
    mem_reg_write,
    wb_reg_write,
    forward_a, forward_b
);

// Fwd_Unit
// :param: rt_in: current rt address. from id_ex
// :param: rs_in: currentrs adress. from id_ex
// :param: ex_rd: address of previous rd. from ex_mem
// :param: mem_rd: address of 2nd previous rd. from mem_wb
// :param: mem_reg_write: control signal. from ex_mem
// :param: wb_reg_write: control signal: from mem_wb
// :return: forward_a: two bit input selector. to alu_mux_a
// :return: forward_b: two bit input selector. to alu_mux_b

input [4:0] rt_in, rs_in, ex_rd, mem_rd;
input mem_reg_write, wb_reg_write;
output [1:0] forward_a, forward_b;
reg [1:0] forward_a, forward_b; 


//combinational logic
always @(rt_in, rs_in, ex_rd, mem_rd, mem_reg_write, wb_reg_write) begin: FWD_UNIT_LOGIC
      forward_a = 2'b00;
	  forward_b = 2'b00;
     //EX to EX forwarding
	 if (mem_reg_write && ex_rd != 0)
	  begin
	    if (ex_rd == rs_in)
		 begin
		    forward_a = 2'b10;
		 end
		else
		 begin
		    forward_a = 2'b00;
		 end
		 
		if (ex_rd == rt_in)
		 begin
		   forward_b = 2'b10;
		 end
		else 
		 begin
		  forward_b = 2'b00;
		 end
	  end
	  
	  //MEM to EX forwarding
	  if (wb_reg_write && mem_rd != 0)
	  begin
	    if (mem_rd == rs_in)
		 begin
		    forward_a = 2'b01;
		 end
		else
		 begin
		    forward_a = 2'b00;
		 end
		 
		if (mem_rd == rt_in)
		 begin
		   forward_b = 2'b01;
		 end
		else 
		 begin
		  forward_b = 2'b00;
		 end
	  end
   end
 endmodule


