module tb_ex_mem;

reg clock;
reg branch_in;
reg mem_read_in;
reg mem_write_in;
reg mem_to_reg_in;
reg reg_write_in;
reg [31:0] jmp_addr;
reg z_in;
reg [31:0] result_in;
reg [31:0] rt_in;
wire [3:0] reg_dst;
wire [31:0] jmp_addr_out;
wire z_out;
wire result_out;
wire [31:0] rt_out;
wire branch_out;
wire mem_read_out;
wire mem_write_out;
wire reg_write_out;
wire [3:0] reg_dst_out;
wire mem_to_reg_out;

initial begin
    $from_myhdl(
        clock,
        branch_in,
        mem_read_in,
        mem_write_in,
        mem_to_reg_in,
        reg_write_in,
        jmp_addr,
        z_in,
        result_in,
        rt_in
    );
    $to_myhdl(
        reg_dst,
        jmp_addr_out,
        z_out,
        result_out,
        rt_out,
        branch_out,
        mem_read_out,
        mem_write_out,
        reg_write_out,
        reg_dst_out,
        mem_to_reg_out
    );
end

ex_mem dut(
    clock,
    branch_in,
    mem_read_in,
    mem_write_in,
    mem_to_reg_in,
    reg_write_in,
    jmp_addr,
    z_in,
    result_in,
    rt_in,
    reg_dst,
    jmp_addr_out,
    z_out,
    result_out,
    rt_out,
    branch_out,
    mem_read_out,
    mem_write_out,
    reg_write_out,
    reg_dst_out,
    mem_to_reg_out
);

endmodule
