`timescale lns/10ps
`timescale 1ns/10ps

module shift_unit(
	imm_in, imm_out
);

input [31:0] imm_in;
output [31:0] imm_out;
reg [31:0] imm_out; 
 
//shift_unit logic
always @(imm_in) begin: SHIFT_UNIT_LOGIC
   imm_out = imm_in << 2; //shift imm_in by 2 bits, to the left
 end
 
 endmodule
