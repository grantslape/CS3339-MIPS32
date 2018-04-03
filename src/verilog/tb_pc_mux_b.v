module tb_pc_mux_b;

reg jmp_ctrl;
reg [31:0] next_inst_address;
reg [31:0] jump_address;
wire [31:0] next_address;

initial begin
    $from_myhdl(
        jmp_ctrl,
        next_inst_address,
        jump_address
    );
    $to_myhdl(
        next_address
    );
end

pc_mux_b dut(
    jmp_ctrl,
    next_inst_address,
    jump_address,
    next_address
);

endmodule
