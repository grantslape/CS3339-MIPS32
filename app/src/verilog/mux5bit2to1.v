`timescale 1ns/10ps

module mux5bit2to1 (
    ctrl_line,
    input1,
    input2,
    out
);
// 5_bit_2_to_1_mux
// 
// :param ctrl_line: Which input should be output. If 1 input2, if 0 input1,  if 2 then $ra
// :param input1: first 5-bit input
// :param input2: second 5-bit input
// :param output: 5-bit output
// :param registerRA: internal $ra value
// :return: generator logic

input [1:0] ctrl_line;
input [4:0] input1;
input [4:0] input2;
output [4:0] out;
reg [4:0] out;
reg [4:0] registerRA;

initial registerRA = 5'b11111;




always @(input2, ctrl_line, input1) begin: MUX32BIT2TO1_LOGIC
    if ((ctrl_line == 0)) begin
        out = input1;
    end
    else if ((ctrl_line == 1)) begin
        out = input2;
    end
    else begin
        out = registerRA;
    end
end

endmodule
