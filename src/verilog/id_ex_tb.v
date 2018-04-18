module tb_id_ex;

reg [0:0] clock;
reg [0:0] reg_dst_in;
reg [0:0] reg_write_in;
reg [0:0] alu_src_in;
reg [0:0] mem_read_in;
reg [0:0] mem_write_in;
reg [0:0] mem_to_reg_in;
reg [3:0] alu_op_in;
reg [0:0] branch_in;
reg [31:0] r_data1;
reg [31:0] r_data2;
reg [4:0] rs;
reg [4:0] rt;
reg [4:0] rd;
reg [31:0] pc_value_in;
reg [31:0] imm;
wire [0:0] reg_dst_out;
wire [0:0] reg_write_out;
wire [0:0] alu_src_out;
wire [0:0] mem_read_out;
wire [0:0] mem_write_out;
wire [0:0] mem_to_reg_out;
wire [3:0] alu_op_out;
wire [0:0] branch_out;
wire [31:0] r_data1_out;
wire [31:0] r_data2_out;
wire [4:0] rs_out;
wire [4:0] rt_out;
wire [4:0] rd_out;
wire [31:0] pc_value_out;
wire [31:0] imm_out;

initial begin
    $from_myhdl(
        clock,
        reg_dst_in,
        reg_write_in,
        alu_src_in,
        mem_read_in,
        mem_write_in,
        mem_to_reg_in,
        alu_op_in,
        branch_in,
        r_data1,
        r_data2,
        rs,
        rt,
        rd,
        pc_value_in,
        imm
    );
    $to_myhdl(
        reg_dst_out,
        reg_write_out,
        alu_src_out,
        mem_read_out,
        mem_write_out,
        mem_to_reg_out,
        alu_op_out,
        branch_out,
        r_data1_out,
        r_data2_out,
        rs_out,
        rt_out,
        rd_out,
        pc_value_out,
        imm_out
    );
end

id_ex dut(
    clock,
    reg_dst_in,
    reg_write_in,
    alu_src_in,
    mem_read_in,
    mem_write_in,
    mem_to_reg_in,
    alu_op_in,
    branch_in,
    r_data1,
    r_data2,
    rs,
    rt,
    rd,
    pc_value_in,
    imm,
    reg_dst_out,
    reg_write_out,
    alu_src_out,
    mem_read_out,
    mem_write_out,
    mem_to_reg_out,
    alu_op_out,
    branch_out,
    r_data1_out,
    r_data2_out,
    rs_out,
    rt_out,
    rd_out,
    pc_value_out,
    imm_out
);

endmodule
