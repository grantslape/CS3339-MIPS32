module branch_unit_tb;

reg [0:0] branch_ctrl;
reg [0:0] zero_in;
wire [0:0] pc_src;

initial begin
    $from_myhdl(
        branch_ctrl,
        zero_in
    );
    $to_myhdl(
        pc_src
    );
end

branch_unit dut(
    branch_ctrl,
    zero_in,
    pc_src
);

endmodule
