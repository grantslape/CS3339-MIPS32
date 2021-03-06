`timescale 1ns/10ps

module id_shift_left (
    top4,
    target,
    jaddr_out
);
// early jump support shift target left 2, then concat with top4
// :param top4: top 4 bits of PC.  from if_id
// :param target: 26 bit immediate jump target.  from if_id
// :param jaddr_out: jump address. to pc_mux_b
// :return: module logic

input [3:0] top4; // 4 bits
input [25:0] target; // 26 bits
output [31:0] jaddr_out; // 32 bits
wire [31:0] jaddr_out;

assign jaddr_out[31:28] = top4;
assign jaddr_out[27:2] = target;
assign jaddr_out[1:0] = 2'b00;

endmodule
