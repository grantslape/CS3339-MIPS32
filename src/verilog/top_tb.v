module top_tb;
parameter TBSIZE = 0;

reg [0:0] clock;
wire [0:0] pc_src;
reg [0:0] reset_ctrl;
reg [0:0] branch_ctrl;
reg [0:0] branch_gate;
reg [0:0] branch_id_ex;
reg [0:0] branch_ex_mem;
reg [0:0] mem_read_ctrl;
reg [0:0] mem_read_gate;
reg [0:0] mem_read_ex_mem;
reg [0:0] mem_read_id_ex;
reg [0:0] mem_write_ctrl;
reg [0:0] mem_write_gate;
reg [0:0] mem_write_id_ex;
reg [0:0] mem_write_ex_mem;
reg [0:0] alu_src_ctrl;
reg [0:0] alu_src_gate;
reg [0:0] alu_src_id_ex;
reg [0:0] reg_write_ctrl;
reg [0:0] reg_write_gate;
reg [0:0] reg_write_id_ex;
reg [0:0] reg_write_ex_mem;
reg [0:0] reg_write_mem_wb;
reg [0:0] ex_stall;
reg [0:0] zero_flag;
reg [0:0] zero_flag_ex_mem;
reg [0:0] pc_write;
reg [31:0] cur_pc;
reg [1:0] mem_to_reg_ctrl;
reg [1:0] mem_to_reg_gate;
reg [1:0] mem_to_reg_id_ex;
reg [1:0] mem_to_reg_ex_mem;
reg [1:0] mem_to_reg_mem_wb;
reg [1:0] forward_a_out;
reg [1:0] forward_b_out;
reg [1:0] reg_dst_ctrl;
reg [1:0] reg_dst_gate;
reg [1:0] reg_dst_id_ex;
reg [1:0] jmp_ctrl;
reg [1:0] jump_gate;
wire [31:0] nxt_pc;
reg [31:0] nxt_inst_mux_a;
wire [31:0] jmp_addr_last;
wire [31:0] inst_out;
reg [31:0] inst_if;
reg [31:0] pc_id;
reg [31:0] pc_id_ex;
reg [31:0] pc_value_ex_mem;
reg [31:0] pc_value_mem_wb;
reg [31:0] if_id_write;
reg [31:0] reg_write_final;
reg [31:0] nxt_inst;
reg signed [31:0] imm_out;
reg signed [31:0] w_data;
reg signed [31:0] r_data1;
reg signed [31:0] r_data1_id_ex;
reg signed [31:0] r_data2;
reg signed [31:0] r_data2_id_ex;
reg signed [31:0] result;
reg signed [31:0] result_ex_mem;
reg signed [31:0] result_mem_wb;
reg signed [31:0] op1_out;
reg signed [31:0] op2_out;
reg signed [31:0] op2_final;
reg signed [31:0] jmp_imm_id_ex;
wire signed [31:0] jmp_imm_shift;
wire signed [31:0] b_addr_out;
reg signed [31:0] wdata_mem;
reg signed [31:0] read_data;
reg signed [31:0] read_data_mem_wb;
reg signed [31:0] imm_jmp_addr;
reg [4:0] rs;
reg [4:0] rs_id_ex;
reg [4:0] rt;
reg [4:0] rt_id_ex;
reg [4:0] rd;
reg [4:0] rd_id_ex;
reg [4:0] rd_ex;
reg [4:0] rd_mem;
reg [4:0] w_addr;
reg [3:0] alu_op_code;
reg [3:0] alu_op_gate;
reg [3:0] alu_op_id_ex;
reg signed [15:0] imm;
reg signed [15:0] imm_id_ex;
reg [3:0] top4;
reg [25:0] target_out;
reg [5:0] op_code;
reg [5:0] funct_out;
wire [31:0] ZERO;

initial begin
    $from_myhdl(
        clock
    );
    $to_myhdl(
        pc_src,
        reset_ctrl,
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
        reg_write_mem_wb,
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
        jmp_imm_id_ex,
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

top #(TBSIZE) dut(
    clock,
    pc_src,
    reset_ctrl,
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
    reg_write_mem_wb,
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
    jmp_imm_id_ex,
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

endmodule
