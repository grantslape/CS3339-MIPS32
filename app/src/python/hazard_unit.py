import os
from myhdl import always_comb, Cosimulation, block


@block
def hazard_unit(if_id_rs, if_id_rt, id_ex_rt, mem_read, pc_write, if_id_write, ex_stall):
    """
    Hazard detection unit
    :param if_id_rs: current Rs, from if_id.rs
    :param if_id_rt: current Rt, from if_id.rt
    :param id_ex_rt: previous Rt, from id_ex.rt_out
    :param mem_read: previous mem_read ctrl signal. from id_ex.mem_read_out
    :param pc_write: activate to stall (nop). to pc_mux_c
    :param if_id_write: stall if_id stage by setting control signals to 0.
    :param ex_stall: Insert bubble into pipeline by setting ctrl signals to 0. to ctrl_mux
    :return: generator logic
    """

    # check for load instruction and check to see if the destination
    # register is the source register of the previous stage
    # if so then set all flags to true
    @always_comb
    def logic():
        if mem_read == 1:
            if id_ex_rt == if_id_rs:
                pc_write.next = 1
                if_id_write.next = 1
                ex_stall.next = 1
            elif id_ex_rt == if_id_rt:
                pc_write.next = 1
                if_id_write.next = 1
                ex_stall.next = 1
            else:
                pc_write.next = 0
                if_id_write.next = 0
                ex_stall.next = 0
        else:
            pc_write.next = 0
            if_id_write.next = 0
            ex_stall.next = 0
    return logic


def hazard_unit_v(if_id_rs, if_id_rt, id_ex_rt, mem_read, pc_write, if_id_write, ex_stall):
    """
    Verilog Hazard detection unit
    :param if_id_rs: current Rs, from if_id.rs
    :param if_id_rt: current Rt, from if_id.rt
    :param id_ex_rt: previous Rt, from id_ex.rt_out
    :param mem_read: previous mem_read ctrl signal. from id_ex.mem_read_out
    :param pc_write: activate to stall (nop). to pc_mux_c
    :param if_id_write: stall if_id stage by setting control signals to 0.
    :param ex_stall: Insert bubble into pipeline by setting ctrl signals to 0. to ctrl_mux
    :return: generator logic
    """

    cmd = "iverilog -o bin/hazard_unit.out src/verilog/hazard_unit.v src/verilog/hazard_unit_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/hazard_unit.out",
                        if_id_rs=if_id_rs,
                        if_id_rt=if_id_rt,
                        id_ex_rt=id_ex_rt,
                        mem_read=mem_read,
                        pc_write=pc_write,
                        if_id_write=if_id_write,
                        ex_stall=ex_stall)
