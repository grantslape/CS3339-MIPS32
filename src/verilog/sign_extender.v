
module sign_extender(imm_in, imm_out);

input [15:0] imm_in; // 16-bit input
output [31:0] imm_out; // 32-bit output

assign imm_out = { 16{imm_in[15]}, imm_in };

endmodule