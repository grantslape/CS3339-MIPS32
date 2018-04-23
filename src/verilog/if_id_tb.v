module tb_if_id;

reg [0:0] clock;
reg [0:0] if_id_write;
reg [31:0] nxt_pc;
reg [31:0] inst_in;
wire [5:0] op_code;
wire [4:0] rs;
wire [4:0] rt;
wire [15:0] imm;
wire [4:0] rd;
wire [5:0] funct_out;
wire [31:0] pc_out;
wire [3:0] top4;
wire [25:0] target_out;
reg [0:0] reset;

initial begin
    $from_myhdl(
        clock,
        if_id_write,
        nxt_pc,
        inst_in,
        reset
    );
    $to_myhdl(
        op_code,
        rs,
        rt,
        imm,
        rd,
        funct_out,
        pc_out,
        top4,
        target_out
    );
end

if_id dut(
    clock,
    if_id_write,
    nxt_pc,
    inst_in,
    op_code,
    rs,
    rt,
    imm,
    rd,
    funct_out,
    pc_out,
    top4,
    target_out,
    reset
);

endmodule
