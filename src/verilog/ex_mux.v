`timescale 1ns/10ps

module ex_mux (
    reg_dst,
    rt_in,
    rd_in,
    dest
);
// 2:1 Mux to select write address
// :param reg_dst: 2 bit selector from id_ex.reg_dst_out 0 for rt, 1 for rd, 2 for ra
// :param rt_in: rt, sent from id_ex
// :param rd_in: rd, sent from id_ex
// :param dest: destination register address, sent to ex_mem
// :return: module logic

input [4:0] rt_in;
input [4:0] rd_in;
input [1:0] reg_dst;
output reg [4:0] dest;
reg [4:0] registerRA;

initial registerRA = 5'b11111;


always @(rd_in, rt_in, reg_dst) begin: EX_MUX_LOGIC
    if (reg_dst == 0) begin
        dest = rt_in;
    end
    else if (reg_dst == 1) begin
        dest = rd_in;
    end
    else if (reg_dst == 2) begin
        dest = registerRA;
    end
end

endmodule
