module top_tb;
parameter TBSIZE = 0;

reg [0:0] clock;
wire [0:0] pc_src;
wire [0:0] branch_ctrl;
wire [0:0] branch_gate;
wire [0:0] branch_id_ex;
wire [0:0] branch_ex_mem;
wire [0:0] mem_read_ctrl;
wire [0:0] mem_read_gate;
wire [0:0] mem_read_ex_mem;
wire [0:0] mem_read_id_ex;
wire [0:0] mem_write_ctrl;
wire [0:0] mem_write_gate;
wire [0:0] mem_write_id_ex;
wire [0:0] mem_write_ex_mem;
wire [0:0] alu_src_ctrl;
wire [0:0] alu_src_gate;
wire [0:0] alu_src_id_ex;
wire [0:0] reg_write_ctrl;
wire [0:0] reg_write_gate;
wire [0:0] reg_write_id_ex;
wire [0:0] reg_write_ex_mem;
wire [0:0] ex_stall;
wire [0:0] zero_flag;
wire [0:0] zero_flag_ex_mem;
wire [0:0] pc_write;
wire [31:0] cur_pc;
wire [1:0] mem_to_reg_ctrl;
wire [1:0] mem_to_reg_gate;
wire [1:0] mem_to_reg_id_ex;
wire [1:0] mem_to_reg_ex_mem;
wire [1:0] mem_to_reg_mem_wb;
wire [1:0] forward_a_out;
wire [1:0] forward_b_out;
wire [1:0] reg_dst_ctrl;
wire [1:0] reg_dst_gate;
wire [1:0] reg_dst_id_ex;
wire [1:0] jmp_ctrl;
wire [1:0] jump_gate;
wire [31:0] nxt_pc;
wire [31:0] nxt_inst_mux_a;
wire [31:0] jmp_addr_last;
wire [31:0] inst_out;
wire [31:0] inst_if;
wire [31:0] pc_id;
wire [31:0] pc_id_ex;
wire [31:0] pc_value_ex_mem;
wire [31:0] pc_value_mem_wb;
wire [0:0] if_id_write;
wire [0:0] reg_write_final;
wire [31:0] nxt_inst;
wire signed [31:0] imm_out;
wire signed [31:0] w_data;
wire signed [31:0] r_data1;
wire signed [31:0] r_data1_id_ex;
wire signed [31:0] r_data2;
wire signed [31:0] r_data2_id_ex;
wire signed [31:0] result;
wire signed [31:0] result_ex_mem;
wire signed [31:0] result_mem_wb;
wire signed [31:0] op1_out;
wire signed [31:0] op2_out;
wire signed [31:0] op2_final;
wire signed [31:0] jmp_imm_id_ex;
wire signed [31:0] jmp_imm_shift;
wire signed [31:0] b_addr_out;
wire signed [31:0] wdata_mem;
wire signed [31:0] read_data;
wire signed [31:0] read_data_mem_wb;
wire signed [31:0] imm_jmp_addr;
wire [4:0] rs;
wire [4:0] rs_id_ex;
wire [4:0] rt;
wire [4:0] rt_id_ex;
wire [4:0] rd;
wire [4:0] rd_id_ex;
wire [4:0] rd_ex;
wire [4:0] rd_mem;
wire [4:0] w_addr;
wire [3:0] alu_op_code;
wire [3:0] alu_op_gate;
wire [3:0] alu_op_id_ex;
wire signed [15:0] imm;
wire signed [31:0] imm_id_ex;
wire [3:0] top4;
wire [25:0] target_out;
wire [5:0] op_code;
wire [5:0] funct_out;
wire [31:0] ZERO;

top #(TBSIZE) dut(
    clock,
    pc_src,
    branch_ctrl,
    branch_gate,
    branch_id_ex,
    branch_ex_mem,
    mem_read_ctrl,
    mem_read_gate,
    mem_read_ex_mem,
    mem_write_ctrl,
    mem_read_id_ex,
    mem_write_gate,
    mem_write_id_ex,
    mem_write_ex_mem,
    alu_src_ctrl,
    alu_src_gate,
    alu_src_id_ex,
    reg_write_ctrl,
    reg_write_gate,
    reg_write_id_ex,
    reg_write_ex_mem,
    ex_stall,
    zero_flag,
    zero_flag_ex_mem,
    pc_write,
    cur_pc,
    mem_to_reg_ctrl,
    mem_to_reg_gate,
    mem_to_reg_id_ex,
    mem_to_reg_ex_mem,
    mem_to_reg_mem_wb,
    forward_a_out,
    forward_b_out,
    reg_dst_ctrl,
    reg_dst_gate,
    reg_dst_id_ex,
    jmp_ctrl,
    jump_gate,
    nxt_pc,
    nxt_inst_mux_a,
    jmp_addr_last,
    inst_out,
    inst_if,
    pc_id,
    pc_id_ex,
    pc_value_ex_mem,
    pc_value_mem_wb,
    if_id_write,
    reg_write_final,
    nxt_inst,
    imm_out,
    w_data,
    r_data1,
    r_data1_id_ex,
    r_data2,
    r_data2_id_ex,
    result,
    result_ex_mem,
    result_mem_wb,
    op1_out,
    op2_out,
    op2_final,
    jmp_imm_shift,
    b_addr_out,
    wdata_mem,
    read_data,
    read_data_mem_wb,
    imm_jmp_addr,
    rs,
    rs_id_ex,
    rt,
    rt_id_ex,
    rd,
    rd_id_ex,
    rd_ex,
    rd_mem,
    w_addr,
    alu_op_code,
    alu_op_gate,
    alu_op_id_ex,
    imm,
    imm_id_ex,
    top4,
    target_out,
    op_code,
    funct_out,
    ZERO
);


initial begin
    $dumpfile("top_v.vcd");
    $dumpvars;
    $from_myhdl(
        clock
    );
    $to_myhdl(
    pc_src,
    branch_ctrl,
    branch_gate,
    branch_id_ex,
    branch_ex_mem,
    mem_read_ctrl,
    mem_read_gate,
    mem_read_ex_mem,
    mem_write_ctrl,
    mem_read_id_ex,
    mem_write_gate,
    mem_write_id_ex,
    mem_write_ex_mem,
    alu_src_ctrl,
    alu_src_gate,
    alu_src_id_ex,
    reg_write_ctrl,
    reg_write_gate,
    reg_write_id_ex,
    reg_write_ex_mem,
    ex_stall,
    zero_flag,
    zero_flag_ex_mem,
    pc_write,
    cur_pc,
    mem_to_reg_ctrl,
    mem_to_reg_gate,
    mem_to_reg_id_ex,
    mem_to_reg_ex_mem,
    mem_to_reg_mem_wb,
    forward_a_out,
    forward_b_out,
    reg_dst_ctrl,
    reg_dst_gate,
    reg_dst_id_ex,
    jmp_ctrl,
    jump_gate,
    nxt_pc,
    nxt_inst_mux_a,
    jmp_addr_last,
    inst_out,
    inst_if,
    pc_id,
    pc_id_ex,
    pc_value_ex_mem,
    pc_value_mem_wb,
    if_id_write,
    reg_write_final,
    nxt_inst,
    imm_out,
    w_data,
    r_data1,
    r_data1_id_ex,
    r_data2,
    r_data2_id_ex,
    result,
    result_ex_mem,
    result_mem_wb,
    op1_out,
    op2_out,
    op2_final,
    jmp_imm_shift,
    b_addr_out,
    wdata_mem,
    read_data,
    read_data_mem_wb,
    imm_jmp_addr,
    rs,
    rs_id_ex,
    rt,
    rt_id_ex,
    rd,
    rd_id_ex,
    rd_ex,
    rd_mem,
    w_addr,
    alu_op_code,
    alu_op_gate,
    alu_op_id_ex,
    imm,
    imm_id_ex,
    top4,
    target_out,
    op_code,
    funct_out,
    ZERO
    );
end

endmodule
