import os
from myhdl import always_comb, Cosimulation, block

@block
def branch_adder(pc_in, imm_in, addr_out):
    """
    calculate addresses for branches
    :param pc_in: PC+4.  from id_ex
    :param imm_in: 32 bit immediate from shift_unit
    :param addr_out: 32 bit jump address. to ex_mem
    :return: module logic
    """

    @always_comb
    def logic():
        addr_out.next = pc_in + imm_in  
       
    return logic


def branch_adder_v(pc_in, imm_in, addr_out):
    """
    calculate addresses for branches verilog
    :param pc_in:
    :param imm_in:
    :param addr_out:
    :return:
    """

    cmd = "iverilog -o bin/branch_adder.out src/verilog/branch_adder.v src/verilog/branch_adder_tb.v"
    os.system(cmd)

    return Cosimulation ("vvp -m lib/myhdl.vpi bin/branch_adder.out",
                         pc_in=pc_in,
                         imm_in=imm_in, 
                         addr_out=addr_out)
