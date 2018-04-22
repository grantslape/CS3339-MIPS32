module tb_ctrl_mux;

reg [0:0] ex_stall;
reg [1:0] jump;
reg [0:0] branch;
reg [0:0] mem_read;
reg [1:0] mem_to_reg;
reg [0:0] mem_write;
reg [0:0] alu_src;
reg [0:0] reg_write;
reg [0:0] reg_dst;
reg [3:0] alu_op;
wire [1:0] jump_out;
wire [0:0] branch_out;
wire [0:0] mem_read_out;
wire [1:0] mem_to_reg_out;
wire [0:0] mem_write_out;
wire [0:0] alu_src_out;
wire [0:0] reg_write_out;
wire [0:0] reg_dst_out;
wire [3:0] alu_op_out;

initial begin
    $from_myhdl(
        ex_stall,
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
    $to_myhdl(
        jump_out,
        branch_out,
        mem_read_out,
        mem_to_reg_out,
        mem_write_out,
        alu_src_out,
        reg_write_out,
        reg_dst_out,
        alu_op_out
    );
end

ctrl_mux dut(
    ex_stall,
    jump,
    branch,
    mem_read,
    mem_to_reg,
    mem_write,
    alu_src,
    reg_write,
    reg_dst,
    alu_op,
    jump_out,
    branch_out,
    mem_read_out,
    mem_to_reg_out,
    mem_write_out,
    alu_src_out,
    reg_write_out,
    reg_dst_out,
    alu_op_out
);

endmodule
