module tb_mux32bit3to1;

reg [1:0] ctrl_line;
reg [31:0] data1;
reg [31:0] mem_rd;
reg [31:0] wb_rd;
wire [31:0] out;

initial begin
    $from_myhdl(
        ctrl_line,
        data1,
        mem_rd,
        wb_rd
    );
    $to_myhdl(
        out
    );
end

mux32bit3to1 dut(
    ctrl_line,
    data1,
    mem_rd,
    wb_rd,
    out
);

endmodule
