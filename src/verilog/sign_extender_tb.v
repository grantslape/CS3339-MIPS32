module tb_sign_extender;
	reg a;
	wire result;
	
	initial begin
		$from_myhdl(
			a
		);
		$to_myhdl(
			result
		);
	end
endmodule