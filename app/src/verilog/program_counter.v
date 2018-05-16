`timescale 1ns/10ps

module program_counter (
    clock,
    pc_write,
    nxt_inst,
    cur_pc
);


input clock;
input pc_write;
input [31:0] nxt_inst;
output [31:0] cur_pc;
reg [31:0] cur_pc;






always @(posedge clock) begin: PROGRAM_COUNTER_SEQ_LOGIC
    if ((pc_write == 0)) begin
        cur_pc <= nxt_inst;
    end
    else begin
        cur_pc <= cur_pc;
    end
end

endmodule
