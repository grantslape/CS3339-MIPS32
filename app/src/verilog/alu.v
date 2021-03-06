`timescale 1ns/10ps

module alu (
    op_1,
    op_2,
    alu_op,
    z,
    result
);
// alu: The main ALU
// input [31:0] op_1: a 32 bit operand.  from alu_mux_1
// input [31:0] op_2: a 32 bit operand.  from alu_mux_imm
// input [3:0] alu_op: The 4-bit ALU op code.  See  OpCode table.
// output [31:0] result: a 32 bit result of operation.  to ex_mem
// output z: Zero flag.  to ex_mem

input signed [31:0] op_1;
input signed [31:0] op_2;
input [3:0] alu_op;
output [0:0] z;
reg [0:0] z;
output signed [31:0] result;
reg signed [31:0] result;






always @(alu_op, op_1, op_2) begin: ALU_LOGIC
    case (alu_op)
        'h1: begin
            result = (op_1 + op_2);
        end
        'h2: begin
            result = (op_1 - op_2);
        end
        'h3: begin
            result = (op_1 ^ op_2);
        end
        'h4: begin
            result = (op_1 | op_2);
        end
        'h5: begin
            result = (op_1 & op_2);
        end
        'h8: begin
            result = (~(op_1 | op_2));
        end
        'h9: begin
            if ((op_1 < op_2)) begin
                result = 1;
            end
            else begin
                result = 0;
            end
        end
    endcase
end


always @(result) begin: ALU_ZERO_DETECTE
    if ((result == 0)) begin
        z = 1;
    end
    else begin
        z = 0;
    end
end

endmodule
