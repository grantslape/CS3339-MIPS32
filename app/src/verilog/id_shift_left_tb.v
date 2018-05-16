module tb_id_shift_left;

reg [3:0] top4;
reg [25:0] target;
wire [31:0] jaddr_out;

initial begin
    $from_myhdl(
        top4,
        target
    );
    $to_myhdl(
        jaddr_out
    );
end

id_shift_left dut(
    top4,
    target,
    jaddr_out
);

endmodule
