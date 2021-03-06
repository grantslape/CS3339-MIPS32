`timescale 1ns/10ps

module mem_wb (
    clk,
    w_reg_ctl_in,
    mem_to_reg_in,
    mem_data_in,
    alu_result_in,
    pc_value_in,
    w_reg_addr_in,
    w_reg_ctl_out,
    mem_to_reg_out,
    mem_data_out,
    alu_result_out,
    w_reg_addr_out,
    pc_value_out
);
// mem_wb: Memory/Writeback pipeline latch
// :param clk: clock (input)
// :param mem_to_reg_(in/out): ctrl signal to select data to write (input 3) to 32bit 3:1 mux
// :param w_reg_ctl_(in/out): write register control signal
// :param mem_data_(in/out): data from mem stage
// :param alu_result_(in/out): result from ex stage
// :param w_reg_addr_(in/out): write register address
// :param pc_value_(in/out): pc value
// :return: module latch

input [0:0] clk;
input [0:0] w_reg_ctl_in;
input [1:0] mem_to_reg_in;
input signed [31:0] mem_data_in;
input signed [31:0] alu_result_in;
input signed [31:0] pc_value_in;
input [4:0] w_reg_addr_in;
output [0:0] w_reg_ctl_out;
reg [0:0] w_reg_ctl_out;
output [1:0] mem_to_reg_out;
reg [1:0] mem_to_reg_out;
output signed [31:0] mem_data_out;
reg signed [31:0] mem_data_out;
output signed [31:0] alu_result_out;
reg signed [31:0] alu_result_out;
output [4:0] w_reg_addr_out;
reg [4:0] w_reg_addr_out;
output [31:0] pc_value_out;
reg [31:0] pc_value_out;

always @(posedge clk) begin: MEM_WB_LATCH
    begin
        w_reg_ctl_out <= w_reg_ctl_in;
        mem_data_out <= mem_data_in;
        pc_value_out <= pc_value_in;
        alu_result_out <= alu_result_in;
        w_reg_addr_out <= w_reg_addr_in;
        mem_to_reg_out <= mem_to_reg_in;
    end
end

endmodule
