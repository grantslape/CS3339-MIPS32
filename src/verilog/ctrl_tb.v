module tb_ctrl;

reg [5:0] funct_in;
reg [5:0] op_in;
wire [1:0] jump;
wire [0:0] branch;
wire [0:0] mem_read;
wire [1:0] mem_to_reg;
wire [0:0] mem_write;
wire [0:0] alu_src;
wire [0:0] reg_write;
wire [1:0] reg_dst;
wire [3:0] alu_op;

initial begin
    $from_myhdl(
        funct_in,
        op_in
    );
    $to_myhdl(
        jump,
        branch,
        mem_read,
        mem_to_reg,
        mem_write,
        alu_src,
        reg_write,
        reg_dst,
        alu_op
    );
end

ctrl dut(
    funct_in,
    op_in,
    jump,
    branch,
    mem_read,
    mem_to_reg,
    mem_write,
    alu_src,
    reg_write,
    reg_dst,
    alu_op
);

endmodule
