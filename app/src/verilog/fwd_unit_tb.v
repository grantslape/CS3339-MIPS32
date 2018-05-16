module tb_fwd_unit;

reg [4:0] rt_in, rs_in, ex_rd, mem_rd;
reg mem_reg_write, wb_reg_write;
wire [1:0] forward_a, forward_b;

initial begin
	$from_myhdl(
		rt_in,
		rs_in,
		ex_rd,
		mem_rd,
		mem_reg_write,
		wb_reg_write
	);
	$to_myhdl(
		forward_a,
		forward_b
	);
end

fwd_unit dut(
	rt_in, rs_in,
	ex_rd, mem_rd,
    mem_reg_write,
    wb_reg_write,
    forward_a, forward_b
);

endmodule