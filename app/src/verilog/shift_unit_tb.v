module tb_shift_unit;

reg [31:0] imm_in;
wire [31:0] imm_out;

initial begin
	$from_myhdl(
	  imm_in
	);
	$to_myhdl(
	  imm_out
	);
end

shift_unit dut(
	imm_in,
	imm_out
);

endmodule
