// File: rfile.v
// Generated by MyHDL 0.10
// Date: Fri Apr 13 01:43:36 2018


`timescale 1ns/10ps

module rfile (
    clock,
    reset,
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
// :param reset: ResetSignal, async
// :param reg_write: write control signal
// :param r_addr1: read address of rs. from if_id
// :param r_addr2: read address of rt. from if_id
// :param w_addr: write address of "rd". from mem_wb
// :param w_data: write data.  From write_mux
// :param r_data1: rs data read from regs[r_addr1].  sent to id_ex
// :param r_data2: data read from regs[r_addr2].  sent to id_ex
// :return: module logic

input [0:0] clock;
input reset;
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



always @(negedge clock, negedge reset) begin: RFILE_LOGIC
    if (reset == 0) begin
        reg_file[0] <= 0;
        reg_file[1] <= 0;
        reg_file[2] <= 0;
        reg_file[3] <= 0;
        reg_file[4] <= 0;
        reg_file[5] <= 0;
        reg_file[6] <= 0;
        reg_file[7] <= 0;
        reg_file[8] <= 0;
        reg_file[9] <= 0;
        reg_file[10] <= 0;
        reg_file[11] <= 0;
        reg_file[12] <= 0;
        reg_file[13] <= 0;
        reg_file[14] <= 0;
        reg_file[15] <= 0;
        reg_file[16] <= 0;
        reg_file[17] <= 0;
        reg_file[18] <= 0;
        reg_file[19] <= 0;
        reg_file[20] <= 0;
        reg_file[21] <= 0;
        reg_file[22] <= 0;
        reg_file[23] <= 0;
        reg_file[24] <= 0;
        reg_file[25] <= 0;
        reg_file[26] <= 0;
        reg_file[27] <= 0;
        reg_file[28] <= 0;
        reg_file[29] <= 0;
        reg_file[30] <= 0;
        reg_file[31] <= 0;
        r_data1 <= 0;
        r_data2 <= 0;
    end
    else begin
        if ((reg_write == 1)) begin
            reg_file[w_addr] = w_data;
        end
        r_data1 <= reg_file[r_addr1];
        r_data2 <= reg_file[r_addr2];

    end
end

endmodule
