`timescale 1ns/10ps

module mux32bit2to1 (
    ctrl_line,
    input1,
    input2,
    out
);
// 32_bit_2_to_1_mux
// 
// :param ctrl_line: Which input should be output. If 1 input2 else input1
// :param input1: first 32-bit input
// :param input2: second 32-bit input
// :param output: 32-bit output
// :return: generator logic

input ctrl_line;
input [31:0] input1;
input [31:0] input2;
output [31:0] out;
reg [31:0] out;






always @(input2, ctrl_line, input1) begin: MUX32BIT2TO1_LOGIC
    if ((ctrl_line == 0)) begin
        out = input1;
    end
    else begin
        out = input2;
    end
end

endmodule
