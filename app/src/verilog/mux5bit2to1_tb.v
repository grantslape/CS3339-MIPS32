module tb_mux5bit2to1;

reg [1:0] ctrl_line;
reg [4:0] input1;
reg [4:0] input2;
wire [4:0] out;

initial begin
    $from_myhdl(
        ctrl_line,
        input1,
        input2
    );
    $to_myhdl(
        out
    );
end

mux5bit2to1 dut(
    ctrl_line,
    input1,
    input2,
    out
);

endmodule
