module rfile_tb;

reg [0:0] clock;
reg reset;
reg [0:0] reg_write;
reg [4:0] r_addr1;
reg [4:0] r_addr2;
reg [4:0] w_addr;
reg [31:0] w_data;
wire [31:0] r_data1;
wire [31:0] r_data2;

initial begin
    $from_myhdl(
        clock,
        reset,
        reg_write,
        r_addr1,
        r_addr2,
        w_addr,
        w_data
    );
    $to_myhdl(
        r_data1,
        r_data2
    );
end

rfile dut(
    clock,
    reset,
    reg_write,
    r_addr1,
    r_addr2,
    w_addr,
    w_data,
    r_data1,
    r_data2
);

endmodule
