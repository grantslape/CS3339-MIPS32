module tb_program_counter;

reg clock;
reg pc_write;
reg [31:0] nxt_inst;
wire [31:0] cur_pc;

initial begin
    $from_myhdl(
        clock,
        pc_write,
        nxt_inst
    );
    $to_myhdl(
        cur_pc
    );
end

program_counter dut(
    clock,
    pc_write,
    nxt_inst,
    cur_pc
);

endmodule
