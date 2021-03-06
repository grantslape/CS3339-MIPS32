`timescale 1ns/10ps

module ctrl (
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
// :param clock: system clock maybe
// :param funct_in: from if_id.funct_out
// :param op_in: This is a MIPS op code from IF_ID
// :param jump: 1 for jump. to inst_mem_mux.jmp_ctrl, pc_mux_b.jmp_ctrl
// :param branch: activate branch unit, to id_ex.branch_in
// :param alu_op: multi-bit alu op code.  see table. to id_ex.alu_op_in
// :param mem_read: activate read from memory, to id_ex.mem_read_in
// :param mem_to_reg: 0 for Alu result writeback, 1 for data writeback. to id_ex.mem_to_reg, 
//     2 for data writeback of pc_next to register ra
// :param mem_write: activate to write to memory. to id_ex
// :param alu_src: 0 for register input, 1 for immediate. to id_ex.alu_src_in
// :param reg_write: activate to write to register.  to id_ex.reg_write_in
// :param reg_dst: 0 to write to Rt ([20:16]), 1 to write to Rd ([15:11]). to id_ex.reg_dst_in, 2 for ra register (pc_value)
// :param reset_out: 1 to insert a 1 cycle stall in the pipeline.  to if_id.reset_in
// :return: module logic

input [5:0] funct_in;
input [5:0] op_in;
output [1:0] jump;
reg [1:0] jump;
output [0:0] branch;
reg [0:0] branch;
output [0:0] mem_read;
reg [0:0] mem_read;
output [1:0] mem_to_reg;
reg [1:0] mem_to_reg;
output [0:0] mem_write;
reg [0:0] mem_write;
output [0:0] alu_src;
reg [0:0] alu_src;
output [0:0] reg_write;
reg [0:0] reg_write;
output [1:0] reg_dst;
reg [1:0] reg_dst;
output [3:0] alu_op;
reg [3:0] alu_op;






always @(op_in, funct_in) begin: CTRL_LOGIC
    case (op_in)
        'h23: begin
            jump = 0;
            branch = 0;
            mem_read = 1;
            mem_to_reg = 1;
            mem_write = 0;
            alu_src = 1;
            reg_write = 1;
            reg_dst = 0;
            alu_op = 1;
        end
        'h2b: begin
            jump = 0;
            branch = 0;
            mem_read = 0;
            mem_write = 1;
            alu_src = 1;
            reg_write = 0;
            alu_op = 1;
        end
        'h4: begin
            alu_op = 2;
            jump = 0;
            branch = 1;
            mem_read = 0;
            mem_write = 0;
            alu_src = 0;
            reg_write = 0;
        end
        'h2: begin
            jump = 1;
            branch = 0;
            mem_write = 0;
            reg_write = 0;
            mem_read = 0;
            alu_src = 0;
            alu_op = 0;
        end
        'h3: begin
            jump = 1;
            branch = 0;
            mem_write = 0;
            reg_write = 1;
            mem_read = 0;
            alu_src = 0;
            alu_op = 0;
            mem_to_reg = 2;
            reg_dst = 2;
        end
        'h19: begin
            jump = 2;
            branch = 0;
            mem_read = 0;
            alu_src = 0;
            reg_write = 0;
            mem_write = 0;
            alu_op = 0;
        end
        'h8: begin
            alu_op = 1;
            jump = 0;
            branch = 0;
            mem_read = 0;
            mem_to_reg = 0;
            mem_write = 0;
            alu_src = 1;
            reg_write = 1;
            reg_dst = 0;
        end
        'h18: begin
            alu_op = 2;
            jump = 0;
            branch = 0;
            mem_read = 0;
            mem_to_reg = 0;
            mem_write = 0;
            alu_src = 1;
            reg_write = 1;
            reg_dst = 0;
        end
        'h0: begin
            jump = 0;
            branch = 0;
            mem_read = 0;
            mem_to_reg = 0;
            mem_write = 0;
            alu_src = 0;
            reg_write = 1;
            reg_dst = 1;
            case (funct_in)
                'h14: begin
                    alu_op = 1;
                end
                'h16: begin
                    alu_op = 2;
                end
                'h26: begin
                    alu_op = 3;
                end
                'h25: begin
                    alu_op = 4;
                end
                'h24: begin
                    alu_op = 5;
                end
                'h0: begin
                    alu_op = 6;
                end
                'h2: begin
                    alu_op = 7;
                end
                'h27: begin
                    alu_op = 8;
                end
                'h2a: begin
                    alu_op = 9;
                end
            endcase
        end
    endcase
end

endmodule
