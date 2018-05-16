module tb_mux32bit3to1;

reg [1:0] ctrl_line;
reg [31:0] data1;
reg [31:0] data2;
reg [31:0] data3;
wire [31:0] out;

initial begin
    $from_myhdl(
        ctrl_line,
        data1,
        data2,
        data3
    );
    $to_myhdl(
        out
    );
end

mux32bit3to1 dut(
    ctrl_line,
    data1,
    data2,
    data3,
    out
);

endmodule
