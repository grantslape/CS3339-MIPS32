module ex_mux_tb;

reg [4:0] rt_in;
reg [4:0] rd_in;
reg [1:0] reg_dst;
wire [4:0] dest;

initial begin
    $from_myhdl(
        reg_dst,
        rt_in,
        rd_in
    );
    $to_myhdl(
        dest
    );
end

ex_mux dut(
    reg_dst,
    rt_in,
    rd_in,
    dest
);

endmodule
