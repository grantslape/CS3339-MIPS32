`timescale 1ns/10ps

module if_id (
    clock,
    if_id_write,
    nxt_pc,
    inst_in,
    op_code,
    rs,
    rt,
    imm,
    rd,
    funct_out,
    pc_out,
    top4,
    target_out
);
// IF/ID state register
// :param clock system clock
// :param if_id_write: from hazard unit.  activate to stall by keeping same outputs as last cycle
// :param reset: clear it all out (flush) from ctrl
// :param nxt_pc: next sequential instruction address
// :param inst_in: Instruction input from inst_mem.inst_out
// :param op_code: sliced from inst_in, Forward to ctrl.funct_in
// :param rs: sliced from inst_in, sent to rfile.r_addr1, id_ex, hazard_unit.if_id_rs
// :param rt: sliced from inst_in, sent to rfile.r_addr2, id_ex, hazard_unit.if_id_rt
// :param imm: sliced from inst_in, sent to sign_extender
// :param rd: sliced from inst_in, sent to id_ex
// :param funct_out: Forward inst_in to id_ex, ctrl.funct_in
// :param pc_out: nxt_pc.  to id_ex
// :param top4: top 4 bits of nxt_pc. From pc_adder
// :param target_out: 26 bit jump immediate

input [0:0] clock;
input [0:0] if_id_write;
input [31:0] nxt_pc;
input [31:0] inst_in;
output [5:0] op_code;
reg [5:0] op_code;
output [4:0] rs;
reg [4:0] rs;
output [4:0] rt;
reg [4:0] rt;
output signed [15:0] imm;
reg signed [15:0] imm;
output [4:0] rd;
reg [4:0] rd;
output [5:0] funct_out;
reg [5:0] funct_out;
output [31:0] pc_out;
reg [31:0] pc_out;
output [3:0] top4;
reg [3:0] top4;
output [25:0] target_out;
reg [25:0] target_out;






always @(posedge clock) begin: IF_ID_LOGIC
    if ((if_id_write == 1)) begin
        // pass
    end
    else begin
        pc_out <= nxt_pc;
        top4 <= nxt_pc[32-1:28];
        op_code <= inst_in[32-1:26];
        rs <= inst_in[26-1:21];
        rt <= inst_in[21-1:16];
        rd <= inst_in[16-1:11];
        funct_out <= inst_in[6-1:0];
        imm <= $signed(inst_in[16-1:0]);
        target_out <= inst_in[26-1:0];
    end
end

endmodule
