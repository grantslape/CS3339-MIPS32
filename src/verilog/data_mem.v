`timescale 1ns/10ps

module data_mem(
        clk, 
        address, 
        write_wire, 
        read_wire, 
        write_data, 
        read_data
);

  // main data memory
  // clk: clock (input)
  // address: 32-bit memory address to access
  // write_data: data to write to address
  // read_data: data to read from address
  // read_wire: activate read from mem
  // write_wire: activate write to mem
  // return: module logic

  input [0:0] clk;
  input [31:0] address;
  input [0:0] write_wire;
  input [0:0] read_wire;
  input [31:0] write_data;
  output reg [31:0] read_data;

  reg [31:0] mem_array [0:1048576];

  //load the buffer with data from the memory file
  initial
    $readmemb("memory_file", mem_array);

  always @(negedge clk)
  begin
    if ( write_wire == 1 )
    begin
      mem_array[address] = write_data;
    end
  end

  always @(posedge clk)
  begin
    if (read_wire == 1)
    begin
        read_data = mem_array[address];
    end
  end
endmodule
