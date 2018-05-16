module data_mem_tb;

    reg [0:0] clk;
    reg [31:0] address;
    reg [0:0] write_wire;
    reg [0:0] read_wire;
    reg [31:0] write_data;
    wire [31:0] read_data;

    initial begin
        $from_myhdl(
                    clk,
                    address,
                    write_wire,
                    read_wire,
                    write_data
        );
        $to_myhdl(
                  read_data
	);
    end

    data_mem dut(
                 clk, 
                 address, 
                 write_wire, 
                 read_wire, 
                 write_data, 
                 read_data
    );

endmodule
