`timescale 1ns/10ps

module mux32bit3to1 (
    ctrl_line,
    data1,
    data2,
    data3,
    out
);
// 3:1 Mux for forwarding results from 2 cycles ago
// :param ctrl: two bit input selector from fwd_unit
// :param data1: rs data received from id_ex 0
// :param mem_rd: rd from the previous cycle, received from ex_mem 01
// :param wb_rd: rd from two cycles ago, received from wb_mux 10
// :param output: Output for rs/op1.  Sent to ALU
// :return: module logic

input [1:0] ctrl_line;
input signed [31:0] data1;
input signed [31:0] data2;
input signed [31:0] data3;
output [31:0] out;
reg signed [31:0] out;






always @(data2, data1, data3, ctrl_line) begin: MUX32BIT3TO1_LOGIC
    case (ctrl_line)
        'h2: begin
            out = data3;
        end
        'h1: begin
            out = data2;
        end
        'h0: begin
            out = data1;
        end
    endcase
end

endmodule
