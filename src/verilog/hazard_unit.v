`timescale 1ns/10ps

module hazard_unit (
    if_id_rs,
    if_id_rt,
    id_ex_rt,
    mem_read,
    pc_write,
    if_id_write,
    ex_stall
);
// Hazard detection unit
// :param if_id_rs: current Rs, from if_id.rs
// :param if_id_rt: current Rt, from if_id.rt
// :param id_ex_rt: previous Rt, from id_ex.rt_out
// :param mem_read: previous mem_read ctrl signal. from id_ex.mem_read_out
// :param pc_write: activate to stall (nop). to pc_mux_c
// :param if_id_write: stall if_id stage by setting control signals to 0.
// :param ex_stall: Insert bubble into pipeline by setting ctrl signals to 0. to ctrl_mux
// :return: generator logic

input [4:0] if_id_rs;
input [4:0] if_id_rt;
input [4:0] id_ex_rt;
input mem_read;
output pc_write;
reg pc_write;
output if_id_write;
reg if_id_write;
output ex_stall;
reg ex_stall;

always @(if_id_rt, id_ex_rt, mem_read, if_id_rs) begin: HAZARD_UNIT_LOGIC
    if ((mem_read == 1)) begin
        if ((id_ex_rt == if_id_rs)) begin
            pc_write = 1;
            if_id_write = 1;
            ex_stall = 1;
        end
        else if ((id_ex_rt == if_id_rt)) begin
            pc_write = 1;
            if_id_write = 1;
            ex_stall = 1;
        end
        else begin
            pc_write = 0;
            if_id_write = 0;
            ex_stall = 0;
        end
    end
    else begin
        pc_write = 0;
        if_id_write = 0;
        ex_stall = 0;
    end
end

endmodule
