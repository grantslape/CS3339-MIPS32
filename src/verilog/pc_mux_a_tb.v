module tb_pc_mux_a;

reg [0:0] pc_src;
reg [31:0] imm_jmp_addr;
reg [31:0] nxt_pc;
wire [31:0] nxt_inst;

initial begin
    $from_myhdl(
        pc_src,
        imm_jmp_addr,
        nxt_pc
    );
    $to_myhdl(
        nxt_inst
    );
end

pc_mux_a dut(
    pc_src,
    imm_jmp_addr,
    nxt_pc,
    nxt_inst
);

endmodule
