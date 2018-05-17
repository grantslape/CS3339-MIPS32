module tb_alu;

reg [31:0] op_1;
reg [31:0] op_2;
reg [3:0] alu_op;
wire [0:0] z;
wire [31:0] result;

initial begin
    $from_myhdl(
        op_1,
        op_2,
        alu_op
    );
    $to_myhdl(
        z,
        result
    );
end

alu dut(
    op_1,
    op_2,
    alu_op,
    z,
    result
);

endmodule
