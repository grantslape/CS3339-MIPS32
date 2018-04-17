module inst_mem_tb;
parameter TBSIZE = 0;

reg [31:0] inst_reg;
wire [31:0] inst_out;


initial begin
    $from_myhdl(
        inst_reg
    );
    $to_myhdl(
        inst_out
	);
end

inst_mem #(TBSIZE) dut(
    inst_reg,
    inst_out
);

endmodule
