""" Branch control unit """
from os import system
from myhdl import always_comb, Cosimulation, block

@block
def branch_unit(branch_ctrl, zero_in, pc_src):
    """
    Branch Unit - python
    :param branch_ctrl: Branch control signal.  from fwd_unit
    :param zero_in: zero flag.  From ex_mem.z_out
    :param pc_src: pc ctrl signal.  to pc_mux_a.pc_src
    :return: module logic
    """

    @always_comb
    def logic():
        pc_src.next = 1 if branch_ctrl == 1 and zero_in == 1 else 0

    return logic


def branch_unit_v(branch_ctrl, zero_in, pc_src):
    """
    Branch Unit - verilog
    :param branch_ctrl: Branch control signal.  from fwd_unit
    :param zero_in: zero flag.  From ex_mem.z_out
    :param pc_src: pc ctrl signal.  to pc_mux_a.pc_src
    :return: module logic
    """
    cmd = "iverilog -o bin/branch_unit.out src/verilog/branch_unit.v src/verilog/branch_unit_tb.v"
    system(cmd)

    return Cosimulation("vvp -m lib/myhdl.vpi bin/branch_unit.out",
                        branch_ctrl=branch_ctrl,
                        zero_in=zero_in,
                        pc_src=pc_src)
