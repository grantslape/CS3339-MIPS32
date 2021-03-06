`timescale 1ns/10ps


module data_mem (
    clk,
    address,
    write_wire,
    read_wire,
    write_data,
    read_data
);
// main data memory
// :param clk: clock (input)
// :param address: 32-bit memory address to access
// :param write_data: data to write to address
// :param read_data: data to read from address
// :param read_wire: activate read from mem
// :param write_wire: activate write to mem
// :return: module logic

input [0:0] clk;
input [31:0] address;
input [0:0] write_wire;
input [0:0] read_wire;
input signed [31:0] write_data;
output reg signed [31:0] read_data;

reg signed [31:0] mem_array [0:1048576];

always @(posedge clk)
begin
  if (read_wire == 1)
  begin
    read_data = mem_array[address];
  end
  else if (write_wire == 1)
  begin
    mem_array[address] = write_data;
  end
end
endmodule



