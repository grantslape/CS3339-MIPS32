module tb_program_counter;

reg clock;
reg [31:0] nxt_inst;
wire [31:0] cur_pc;

initial begin
    $from_myhdl(
        clock,
        nxt_inst
    );
    $to_myhdl(
        cur_pc
    );
end

program_counter dut(
    clock,
    nxt_inst,
    cur_pc
);

endmodule
