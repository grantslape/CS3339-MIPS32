`timescale 1ns/10ps

module pc_adder (
    cur_pc,
    next_pc
);


input [31:0] cur_pc;
output [31:0] next_pc;
reg [31:0] next_pc;

always @(cur_pc) begin: PC_ADDER_LOGIC
    next_pc = (cur_pc + 4);
end

endmodule
