module wb_mux_tb;

reg [0:0] sel;
wire [31:0] wb_out;
reg [31:0] rdata_in;
reg [31:0] result_in;

initial begin
    $from_myhdl(
        sel,
        rdata_in,
        result_in
    );
    $to_myhdl(
        wb_out
    );
end

wb_mux dut(
    sel,
    wb_out,
    rdata_in,
    result_in
);

endmodule
