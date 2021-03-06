`timescale 1ns/10ps

module branch_adder (
    pc_in,
    imm_in,
    addr_out
);
// calculate addresses for branches
// :param pc_in: PC+4.  from id_ex
// :param imm_in: 32 bit immediate from shift_unit
// :param addr_out: 32 bit jump address. to ex_mem
// :return: module logic

input [31:0] pc_in;
input [31:0] imm_in;
output [31:0] addr_out;
wire [31:0] addr_out;







assign addr_out = (pc_in + imm_in);

endmodule
