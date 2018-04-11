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
reg [31:0] reg_inst_reg; //address to raw_mem array
output [31:0] inst_out;
reg [31:0] inst_out; 

reg [31:0] raw_mem [0:1000];

//load the buffer with data from the .bin file
initial
    $readmemb("instructions.bin", raw_mem);

always @(inst_reg)
    begin
        reg_inst_reg = inst_reg;
        inst_out = raw_mem[reg_inst_reg];
    end
endmodule
