module tb_mux32bit2to1;

reg ctrl_line;
reg [31:0] input1;
reg [31:0] input2;
wire [31:0] out;

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

mux32bit2to1 dut(
    ctrl_line,
    input1,
    input2,
    out
);

endmodule
