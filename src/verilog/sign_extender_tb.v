module tb_sign_extender;

reg [15:0] imm_in;
wire [31:0] imm_out;

initial begin
    $from_myhdl(
        imm_in
    );
    $to_myhdl(
        imm_out
    );
end

sign_extender dut(
    imm_in,
    imm_out
);

endmodule
