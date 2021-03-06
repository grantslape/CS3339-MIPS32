`timescale 1ns/10ps

module ex_mem (
    clock,
    branch_in,
    mem_read_in,
    mem_write_in,
    mem_to_reg_in,
    reg_write_in,
    jmp_addr,
    z_in,
    pc_value_in,
    result_in,
    rt_in,
    reg_dst_in,
    jmp_addr_out,
    z_out,
    result_out,
    rt_out,
    branch_out,
    mem_read_out,
    mem_write_out,
    reg_write_out,
    reg_dst_out,
    pc_value_out,
    mem_to_reg_out
);
// EX/MEM Pipeline register
// :param clock: system clock
// :param branch_in: branch ctrl signal from id_ex.branch_out
// :param mem_read_in: mem_read ctrl signal. from id_ex.mem_read_out
// :param mem_write_in: mem_write ctrl signal. from id_ex.mem_write_out
// :param mem_to_reg_in: mem_to_reg ctrl signal from id_ex
// :param reg_write_in: reg_write ctrl signal. from id_ex.reg_write_out
// :param mem_to_reg_in: mem_to_reg ctrl signal. from id_ex.mem_to_reg_out
// :param jmp_addr: jump address.  from branch_adder.addr_out
// :param z_in: zero flag.  from alu.
// :param pc_value_in: pc+4 value, from id_ex
// :param result_in: result input. from ALU
// :param rt_in: special rt input, for sw. from alu_mux_b
// :param reg_dst: destination reg address. from ex_mux
// :param jmp_addr_out: jump address. to pc_mux_a
// :param z_out: zero flag. to branch_unit
// :param result_out: read ALU result output. to data_mem, mem_wb, alu_mux_a
// :param rt_out: special rt output for sw. to data_mem.rt_in, fwd_unit.ex_rd
// :param branch_out: branch ctrl signal to branch_unit.branch_ctrl
// :param mem_read_out: mem_read ctrl signal to data_mem.read_ctrl
// :param mem_write_out: mem_write ctrl signal to data_mem.w_ctrl
// :param reg_write_out: reg_write ctrl signal to mem_wb.reg_write_in
// :param mem_to_reg_out: mem_to_reg ctrl signal to mem_wb.
// :param reg_dst_out: Destination Register for write back to mem_wb
// :param pc_value_out:
// :param mem_to_reg_out: mem_to_reg ctrl signal to mem_wb
// :return:

input clock;
input branch_in;
input mem_read_in;
input mem_write_in;
input [1:0] mem_to_reg_in;
input reg_write_in;
input [31:0] jmp_addr;
input z_in;
input [31:0] pc_value_in;
input [31:0] result_in;
input [31:0] rt_in;
input [4:0] reg_dst_in;
output [31:0] jmp_addr_out;
reg [31:0] jmp_addr_out;
output z_out;
reg z_out;
output [31:0] result_out;
reg [31:0] result_out;
output [31:0] rt_out;
reg [31:0] rt_out;
output branch_out;
reg branch_out;
output mem_read_out;
reg mem_read_out;
output mem_write_out;
reg mem_write_out;
output reg_write_out;
reg reg_write_out;
output [4:0] reg_dst_out;
reg [4:0] reg_dst_out;
output [31:0] pc_value_out;
reg [31:0] pc_value_out;
output [1:0] mem_to_reg_out;
reg [1:0] mem_to_reg_out;






always @(posedge clock) begin: EX_MEM_LOGIC
    branch_out <= branch_in;
    mem_read_out <= mem_read_in;
    mem_write_out <= mem_write_in;
    mem_to_reg_out <= mem_to_reg_in;
    reg_write_out <= reg_write_in;
    jmp_addr_out <= jmp_addr;
    z_out <= z_in;
    result_out <= result_in;
    rt_out <= rt_in;
    pc_value_out <= pc_value_in;
    reg_dst_out <= reg_dst_in;
end

endmodule
