module tb_branch_adder;

reg [31:0] pc_in;
reg [31:0] imm_in;
wire [31:0] addr_out;

initial begin
    $from_myhdl(
        pc_in,
        imm_in
    );
    $to_myhdl(
        addr_out
    );
end

branch_adder dut(
    pc_in,
    imm_in,
    addr_out
);

endmodule
