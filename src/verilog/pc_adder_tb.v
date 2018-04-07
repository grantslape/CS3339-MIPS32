module tb_pc_adder;

reg [31:0] cur_pc;
wire [31:0] next_pc;

initial begin
    $from_myhdl(
        cur_pc
    );
    $to_myhdl(
        next_pc
    );
end

pc_adder dut(
    cur_pc,
    next_pc
);

endmodule
