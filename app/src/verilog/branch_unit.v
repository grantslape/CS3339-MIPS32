`timescale 1ns/10ps

module branch_unit (
    branch_ctrl,
    zero_in,
    pc_src
);
// Branch Unit - python
// :param branch_ctrl: Branch control signal.  from fwd_unit
// :param zero_in: zero flag.  From ex_mem.z_out
// :param pc_src: pc ctrl signal.  to pc_mux_a.pc_src
// :return: module logic

input [0:0] branch_ctrl;
input [0:0] zero_in;
output [0:0] pc_src;
wire [0:0] pc_src;





assign pc_src = ((branch_ctrl == 1) && (zero_in == 1)) ? 1 : 0;

endmodule
