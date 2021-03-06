`timescale 1ns/10ps

module rfile (
    clock,
    reg_write,
    r_addr1,
    r_addr2,
    w_addr,
    w_data,
    r_data1,
    r_data2
);
// 32-bit Register File of 32 registers
// :param clock: Input from system clock
// :param reg_write: write control signal
// :param r_addr1: read address of rs. from if_id
// :param r_addr2: read address of rt. from if_id
// :param w_addr: write address of "rd". from mem_wb
// :param w_data: write data.  From write_mux
// :param r_data1: rs data read from regs[r_addr1].  sent to id_ex
// :param r_data2: data read from regs[r_addr2].  sent to id_ex
// :return: module logic

input [0:0] clock;
input [0:0] reg_write;
input [4:0] r_addr1;
input [4:0] r_addr2;
input [4:0] w_addr;
input signed [31:0] w_data;
output signed [31:0] r_data1;
reg signed [31:0] r_data1;
output signed [31:0] r_data2;
reg signed [31:0] r_data2;

reg signed [31:0] reg_file [0:32-1];



always @(negedge clock) begin: RFILE_LOGIC
    if ((reg_write == 1)) begin
        reg_file[w_addr] = w_data;
    end
    r_data1 <= reg_file[r_addr1];
    r_data2 <= reg_file[r_addr2];
end

endmodule
