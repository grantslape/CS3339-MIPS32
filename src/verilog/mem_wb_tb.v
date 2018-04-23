module mem_wb_tb;

reg clk;
reg reset;
reg [0:0] w_reg_ctl_in;
reg [1:0] mem_to_reg_in;
reg [31:0] mem_data_in;
reg [31:0] alu_result_in;
reg [31:0] pc_value_in;
reg [4:0] w_reg_addr_in;
wire [0:0] w_reg_ctl_out;
wire [1:0] mem_to_reg_out;
wire [31:0] mem_data_out;
wire [31:0] alu_result_out;
wire [4:0] w_reg_addr_out;
wire [31:0] pc_value_out;

initial begin
    $from_myhdl(
        clk,
        reset,
        w_reg_ctl_in,
        mem_to_reg_in,
        mem_data_in,
        alu_result_in,
        pc_value_in,
        w_reg_addr_in
    );
    $to_myhdl(
        w_reg_ctl_out,
        mem_to_reg_out,
        mem_data_out,
        alu_result_out,
        w_reg_addr_out,
        pc_value_out
    );
end

mem_wb dut(
    clk,
    reset,
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

endmodule
