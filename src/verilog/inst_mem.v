`timescale 1ns/10ps

module inst_mem(
        inst_reg, 
        inst_out
);

// Inst_Mem
// :param inst_reg: address to read from, from nxt_inst. This is an index of raw_mem
// :param raw_mem: (Internal REG) Instruction memory from a text file
// :return: inst_out: instruction output to inst_mem_mux

input [31:0] inst_reg;
output reg [31:0] inst_out;

reg [31:0] raw_mem [0:1048576];

//load the buffer with data from the .bin file
initial
    $readmemb("lib/instructions", raw_mem);

always @(inst_reg)
    begin
        inst_out <= raw_mem[inst_reg];
    end
endmodule
