module tb_pc_mux_c;

reg pc_write;
reg [31:0] cur_pc;
reg zero;
wire [31:0] next_pc;

initial begin
    $from_myhdl(
        pc_write,
        cur_pc,
        zero
    );
    $to_myhdl(
        next_pc
    );
end

pc_mux_c dut(
    pc_write,
    cur_pc,
    zero,
    next_pc
);

endmodule
