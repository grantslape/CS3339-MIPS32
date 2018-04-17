module tb_sign_extender;
	reg imm_in;
	wire imm_out;
	
	initial begin
		$from_myhdl(
			imm_in
		);
		$to_myhdl(
			imm_out
		);
	end
endmodule