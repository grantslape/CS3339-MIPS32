import os, array

from myhdl import always_comb, intbv, Cosimulation


def inst_mem(inst_reg, inst_out):
    """
    Instruction Memory.  Stores the instructions that will be executed
    :param inst_reg: address to read from, from nxt_inst. This is an index of raw_mem
    :param raw_mem: (Internal REG) Instruction memory from a text file
    :return: inst_out: Inst_mem logic to inst_mem_mux
    """
    reg_inst_reg = 0
    raw_mem = []
    f = open('instructions.bin', 'rb')
    try:
        raw_mem = array.fromfile(f, 1000)
    except EOFError:
        #EOF exception is thrown when there are less than n elements to read from the file
        #the contents are still read into the array. Do nothing

    @always_comb
    def logic():
        reg_inst_reg.next = intbv(inst_reg)[32:]
        inst_out.next = raw_mem[reg_inst_reg]       
    return logic


def inst_mem_v(inst_reg, inst_out):
    """
    Verilog Instruction Memory. Stores the instructions that will be executed
    :param inst_reg: address to read from, from nxt_inst. This is an index of raw_mem
    :param raw_mem: (Internal REG) Instruction memory from a text file
    :return: inst_out: Inst_mem logic to inst_mem_mux
    """
    cmd = "iverilog -o bin/inst_mem.out src/verilog/inst_mem.v src/verilog/inst_mem_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/inst_mem.out",
                        inst_reg=inst_reg,
                        inst_out=inst_out)
