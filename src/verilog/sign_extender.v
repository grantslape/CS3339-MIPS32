`timescale 1ns/10ps

module sign_extender (
    imm_in,
    imm_out
);
// Sign Extend 16 bit immediate to 32 bit
// :param imm_in:
// :param imm_out:
// :return:

input signed [15:0] imm_in;
output signed [31:0] imm_out;
reg signed [31:0] imm_out;






always @(imm_in) begin: SIGN_EXTENDER_LOGIC
    if ((imm_in >= 32768)) begin
        imm_out = (imm_in | 33'hffff0000);
    end
    else begin
        imm_out = imm_in;
    end
end

endmodule
