module tb_hazard_unit;

reg [4:0] if_id_rs;
reg [4:0] if_id_rt;
reg [4:0] id_ex_rt;
reg mem_read;
wire pc_write;
wire if_id_write;
wire ex_stall;

initial begin
    $from_myhdl(
        if_id_rs,
        if_id_rt,
        id_ex_rt,
        mem_read
    );
    $to_myhdl(
        pc_write,
        if_id_write,
        ex_stall
    );
end

hazard_unit dut(
    if_id_rs,
    if_id_rt,
    id_ex_rt,
    mem_read,
    pc_write,
    if_id_write,
    ex_stall
);

endmodule
