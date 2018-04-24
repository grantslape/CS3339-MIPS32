`timescale 1ns/10ps

module top (
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
// Instantiate modules

input [0:0] clock;
output [0:0] pc_src;
wire [0:0] pc_src;
output [0:0] reset_ctrl;
reg [0:0] reset_ctrl;
output [0:0] branch_ctrl;
reg [0:0] branch_ctrl;
output [0:0] branch_gate;
reg [0:0] branch_gate;
output [0:0] branch_id_ex;
reg [0:0] branch_id_ex;
output [0:0] branch_ex_mem;
reg [0:0] branch_ex_mem;
output [0:0] mem_read_ctrl;
reg [0:0] mem_read_ctrl;
output [0:0] mem_read_gate;
reg [0:0] mem_read_gate;
output [0:0] mem_read_ex_mem;
reg [0:0] mem_read_ex_mem;
output [0:0] mem_write_ctrl;
reg [0:0] mem_write_ctrl;
output [0:0] mem_read_id_ex;
reg [0:0] mem_read_id_ex;
output [0:0] mem_write_gate;
reg [0:0] mem_write_gate;
output [0:0] mem_write_id_ex;
reg [0:0] mem_write_id_ex;
output [0:0] mem_write_ex_mem;
reg [0:0] mem_write_ex_mem;
output [0:0] alu_src_ctrl;
reg [0:0] alu_src_ctrl;
output [0:0] alu_src_gate;
reg [0:0] alu_src_gate;
output [0:0] alu_src_id_ex;
reg [0:0] alu_src_id_ex;
output [0:0] reg_write_ctrl;
reg [0:0] reg_write_ctrl;
output [0:0] reg_write_gate;
reg [0:0] reg_write_gate;
output [0:0] reg_write_id_ex;
reg [0:0] reg_write_id_ex;
output [0:0] reg_write_ex_mem;
reg [0:0] reg_write_ex_mem;
input [0:0] reg_write_mem_wb;
output [0:0] ex_stall;
reg [0:0] ex_stall;
output [0:0] zero_flag;
reg [0:0] zero_flag;
output [0:0] zero_flag_ex_mem;
reg [0:0] zero_flag_ex_mem;
output [0:0] pc_write;
reg [0:0] pc_write;
output [31:0] cur_pc;
reg [31:0] cur_pc;
output [1:0] mem_to_reg_ctrl;
reg [1:0] mem_to_reg_ctrl;
output [1:0] mem_to_reg_gate;
reg [1:0] mem_to_reg_gate;
output [1:0] mem_to_reg_id_ex;
reg [1:0] mem_to_reg_id_ex;
output [1:0] mem_to_reg_ex_mem;
reg [1:0] mem_to_reg_ex_mem;
output [1:0] mem_to_reg_mem_wb;
reg [1:0] mem_to_reg_mem_wb;
output [1:0] forward_a_out;
reg [1:0] forward_a_out;
output [1:0] forward_b_out;
reg [1:0] forward_b_out;
output [1:0] reg_dst_ctrl;
reg [1:0] reg_dst_ctrl;
output [1:0] reg_dst_gate;
reg [1:0] reg_dst_gate;
output [1:0] reg_dst_id_ex;
reg [1:0] reg_dst_id_ex;
output [1:0] jmp_ctrl;
reg [1:0] jmp_ctrl;
output [1:0] jump_gate;
reg [1:0] jump_gate;
output [31:0] nxt_pc;
wire [31:0] nxt_pc;
output [31:0] nxt_inst_mux_a;
reg [31:0] nxt_inst_mux_a;
output [31:0] jmp_addr_last;
wire [31:0] jmp_addr_last;
output [31:0] inst_out;
wire [31:0] inst_out;
output [31:0] inst_if;
reg [31:0] inst_if;
output [31:0] pc_id;
reg [31:0] pc_id;
output [31:0] pc_id_ex;
reg [31:0] pc_id_ex;
output [31:0] pc_value_ex_mem;
reg [31:0] pc_value_ex_mem;
output [31:0] pc_value_mem_wb;
reg [31:0] pc_value_mem_wb;
output [31:0] if_id_write;
reg [31:0] if_id_write;
output [31:0] reg_write_final;
reg [31:0] reg_write_final;
output [31:0] nxt_inst;
reg [31:0] nxt_inst;
output signed [31:0] imm_out;
reg signed [31:0] imm_out;
output signed [31:0] w_data;
reg signed [31:0] w_data;
output signed [31:0] r_data1;
reg signed [31:0] r_data1;
output signed [31:0] r_data1_id_ex;
reg signed [31:0] r_data1_id_ex;
output signed [31:0] r_data2;
reg signed [31:0] r_data2;
output signed [31:0] r_data2_id_ex;
reg signed [31:0] r_data2_id_ex;
output signed [31:0] result;
reg signed [31:0] result;
output signed [31:0] result_ex_mem;
reg signed [31:0] result_ex_mem;
output signed [31:0] result_mem_wb;
reg signed [31:0] result_mem_wb;
output signed [31:0] op1_out;
reg signed [31:0] op1_out;
output signed [31:0] op2_out;
reg signed [31:0] op2_out;
output signed [31:0] op2_final;
reg signed [31:0] op2_final;
output signed [31:0] jmp_imm_id_ex;
reg signed [31:0] jmp_imm_id_ex;
output signed [31:0] jmp_imm_shift;
wire signed [31:0] jmp_imm_shift;
output signed [31:0] b_addr_out;
wire signed [31:0] b_addr_out;
output signed [31:0] wdata_mem;
reg signed [31:0] wdata_mem;
output signed [31:0] read_data;
reg signed [31:0] read_data;
output signed [31:0] read_data_mem_wb;
reg signed [31:0] read_data_mem_wb;
output signed [31:0] imm_jmp_addr;
reg signed [31:0] imm_jmp_addr;
output [4:0] rs;
reg [4:0] rs;
output [4:0] rs_id_ex;
reg [4:0] rs_id_ex;
output [4:0] rt;
reg [4:0] rt;
output [4:0] rt_id_ex;
reg [4:0] rt_id_ex;
output [4:0] rd;
reg [4:0] rd;
output [4:0] rd_id_ex;
reg [4:0] rd_id_ex;
output [4:0] rd_ex;
reg [4:0] rd_ex;
output [4:0] rd_mem;
reg [4:0] rd_mem;
output [4:0] w_addr;
reg [4:0] w_addr;
output [3:0] alu_op_code;
reg [3:0] alu_op_code;
output [3:0] alu_op_gate;
reg [3:0] alu_op_gate;
output [3:0] alu_op_id_ex;
reg [3:0] alu_op_id_ex;
output signed [15:0] imm;
reg signed [15:0] imm;
output signed [15:0] imm_id_ex;
reg signed [15:0] imm_id_ex;
output [3:0] top4;
reg [3:0] top4;
output [25:0] target_out;
reg [25:0] target_out;
output [5:0] op_code;
reg [5:0] op_code;
output [5:0] funct_out;
reg [5:0] funct_out;
input [31:0] ZERO;

//THESE ARE INSIDE MODULES.
//reg signed [31:0] data_memory_mem_array [0:1048576-1];
//reg signed [31:0] registers_reg_file [0:32-1];
//reg [31:0] inst_memory_raw_mem [0:262144-1];
//initial
//    $readmemb("lib/instructions", inst_memory_raw_mem);

program_counter pc(.clock(clock), .pc_write(pc_write), .nxt_inst(nxt_inst), .cur_pc(cur_pc))

mux32bit2to1 pc_mux_a(.ctrl_line(pc_src), .input1(nxt_pc), .input2(imm_jmp_addr), .out(nxt_inst_mux_a))

mux32bit3to1 pc_mux_b(.ctrl_line(jmp_ctrl), .data1(nxt_inst_mux_a), .data2(jmp_addr_last), .data3(r_data1), .out(nxt_inst))

pc_adder pc_add(.cur_pc(cur_pc), .next_pc(nxt_pc))

inst_mem memory(.inst_reg(cur_pc), .inst_out(inst_out))

mux32bit2to1 inst_mem_mux(.ctrl_line(jmp_ctrl), .input1(inst_out), .input2(ZERO), .out(inst_if))

if_id if_pipe(.if_id_write(if_id_write), .clock(clock), .nxt_pc(nxt_pc), .inst_in(inst_if), .op_code(op_code),
              .rs(rs), .rt(rt), .imm(imm), .rd(rd), .funct_out(funct_out), .pc_out(pc_id), .top4(top4),
              .target_out(target_out))

sign_extender extender(.imm_in(imm), .imm_out(imm_out))

rfile registers(.clock(clock), .r_addr1(rs), .raddr2(rt), .w_addr(w_addr), .w_data(w_data), .r_data1(r_data1),
                .r_data2(r_data2), .reg_write(reg_write_final))

id_shift_left id_shifter(.top4(top4), .target(target_out), .jaddr_out(jmp_addr_last))

ctrl ctrl_unit(.funct_in(funct_out), .op_in(op_code), .jump(jmp_ctrl), .branch(branch_ctrl), .alu_op(alu_op_code),
               .mem_read(mem_read_ctrl), .mem_to_reg(mem_to_reg_ctrl), .mem_write(mem_write_ctrl), .alu_src(alu_src_ctrl),
               .reg_write(reg_write_ctrl), .reg_dst(reg_dst_ctrl), .reset_out(reset_ctrl))

ctrl_mux ctrl_gate(.ex_stall(ex_stall), .jump(jmp_ctrl), .branch(branch_ctrl), .mem_read(mem_read_ctrl),
                   .mem_to_reg(mem_to_reg_ctrl), .mem_write(mem_write_ctrl), .alu_src(alu_src_ctrl),
                   .reg_write(reg_write_ctrl), .reg_dst(reg_dst_ctrl), .alu_op(alu_op_code),
                   .jump_out(jump_gate), .branch_out(branch_gate), .mem_read_out(mem_read_gate),
                   .mem_to_reg_out(mem_to_reg_gate), .mem_write_out(mem_write_gate), .alu_src_out(alu_src_gate),
                   .reg_write_out(reg_write_gate), .reg_dst_out(reg_dst_gate), .alu_op_out(alu_op_gate))

hazard_unit hzd(.if_id_rs(rs), .if_id_rt(rt), .id_ex_rt(rt_id_ex), .mem_read(mem_read_id_ex),
                .pc_write(pc_write), .if_id_write(if_id_write), .ex_stall(ex_stall)

id_ex id_pipe(.clock(clock), .branch_in(branch_gate), .alu_op_in(alu_code_gate), .mem_read_in(mem_read_gate),
              .mem_write_in(mem_write_gate), .alu_src_in(alu_src_gate), .reg_write_in(reg_write_gate),
              .reg_dst_in(reg_dst_gate), .pc_value_in(pc_id), .mem_to_reg_in(mem_to_reg_gate),
              .r_data1(r_data1), .r_data2(r_data2). .rs(rs), .rt(rt), .rd(rd), .imm(imm), .jmp_mm(imm_out),
              .r_data1_out(r_data1_id_ex), .r_data2_out(r_data2_id_ex), .imm_out(imm_id_ex),
              .rs_out(rs_id_ex), .rt_out(rt_id_ex), .rd_out(rd_id_ex), pc_value_out(pc_id_ex),
              .branch_out(branch_id_ex), .alu_op_out(alu_op_id_ex), .mem_read_out(mem_read_id_ex),
              .mem_write_out(mem_write_id_ex), .alu_src_out(alu_src_id_ex), .reg_write_out(reg_write_id_ex),
              .reg_dst_out(reg_dst_id_ex), .mem_to_reg_out(mem_to_reg_id_ex), .jmp_imm_out(jmp_imm_id_ex))

mux32bit3to1 alu_mux_a(.ctrl_line(forward_a_out), .data1(r_data1_id_ex), .data2(result_ex_mem),
                       .data3(result_mem_wb), .out(op1_out))

mux32bit3to1 alu_mux_b(.ctrl_line(forward_b_out), .data1(r_data2_id_ex), .data2(result_ex_mem),
                       .data3(result_mem_wb), .out(op2_out))

mux32bit2to1 alu_mux_imm(.ctrl_line(alu_src_id_ex), .input1(op2_out), .input2(imm_out), .out(op2_final))

alu alu_dut(.op_1(op1_out), .op_2(op2_final), .alu_op(alu_op_id_ex), .result(result), .z(zero_flag))

ex_mux dest_mux(.reg_dst(reg_dst_id_ex), .rt_in(rt_id_ex), .rd_in(rd_id_ex), .dest(rd_ex))

forward_unit fwd(.rt_in(rt_id_ex), .rs_in(rs_id_ex), .ex_rd(rd_ex), .mem_rd(rd_mem), .forward_b(forward_b_out)
                 .mem_reg_write(reg_write_ex_mem), .wb_reg_write(reg_write_mem_wb), .forward_a(forward_a_out))

shift_unit shifter(.imm_in(jmp_imm_id_ex), .imm_out(jmp_imm_shift))

branch_adder b_addr(.pc_in(pc_id_ex), .imm_in(jmp_imm_shift), .addr_out(b_addr_out))

ex_mem ex_pipe(.clock(clock), .branch_in(branch_id_ex), .mem_read_in(mem_read_id_ex), .mem_write_in(mem_write_id_ex),
               .reg_write_in(reg_write_id_ex), .mem_to_reg_in(mem_to_reg_id_ex), .jmp_addr(b_addr_out),
               .z_in(zero_flag), .result_in(result), .rt_in(op2_out), .reg_dst_in(rd_ex), .jmp_addr_out(imm_jmp_addr),
               .z_out(zero_flag_ex_mem), .result_out(result_ex_mem), .rt_out(wdata_mem), .branch_out(branch_ex_mem),
               .mem_read_out(mem_read_ex_mem), .mem_write_out(mem_write_ex_mem), .mem_to_reg_out(mem_to_reg_ex_mem),
               .reg_dst_out(rd_mem), .pc_value_in(pc_id_ex), .pc_value_out(pc_value_ex_mem))

branch_unit b_unit(.branch_ctrl(branch_ex_mem), .zero_in(zero_flag_ex_mem), .pc_src(pc_src))

data_mem data(.clk(clock), .read_wire(mem_read_ex_mem), .write_wire(mem_write_ex_mem), .address(result_ex_mem),
              .write_data(wdata_mem), .read_data(read_data))

mem_wb wb_pipe(.clk(clock), .w_reg_ctl_in(reg_write_ex_mem), .mem_data_in(read_data), .alu_result_in(result_ex_mem),
               .w_reg_addr_in(rd_mem), .mem_to_reg_in(mem_to_reg_ex_mem), .mem_data_out(read_data_mem_wb),
               .alu_result_out(result_mem_wb), .w_reg_addr_out(w_addr), .w_reg_ctl_out(reg_write_final),
               .mem_to_reg_out(mem_to_reg_mem_wb), .pc_value_in(pc_value_ex_mem), .pc_value_out(pc_value_mem_wb))

mux32bit3to1 wb_mux(.ctrl_line(mem_to_reg_mem_wb), .data1(read_data_mem_wb), .data2(result_mem_wb),
                    .data3(pc_value_mem_wb), .out(w_data))

endmodule