from os import system

from myhdl import always_comb, intbv, Cosimulation
from src.commons.settings import settings as sf


def inst_mem(inst_reg, inst_out):
    """
    Instruction Memory.  Stores the instructions that will be executed
    :param inst_reg: address to read from, from nxt_inst. This is an index of raw_mem
    :      raw_mem: (Internal REG) Instruction memory from a text file
    :param inst_out: Inst_mem logic to inst_mem_mux
    :return: module logic
    """
    TB_SIZE = 0
    raw_mem = []
    mem_file = open('lib/instructions',)
    try:
        raw_mem = [intbv(line) for line in mem_file]
    except IOError:
        # EOF exception is thrown when there are less than n elements to read from the file
        # the contents are still read into the array. Do nothing
        pass
    mem_file.close()

    @always_comb
    def logic():
        inst_out.next = raw_mem[inst_reg%4]
    return logic


def inst_mem_v(inst_reg, inst_out):
    """
    Verilog Instruction Memory. Stores the instructions that will be executed
    :param inst_reg: address to read from, from nxt_inst. This is an index of raw_mem
           raw_mem: (Internal REG) Instruction memory from a text file
    :param inst_out: Inst_mem logic to inst_mem_mux
    :return Cosimulation
    """
    cmd = "iverilog -o bin/inst_mem.out -P inst_mem_tb.TBSIZE={} src/verilog/inst_mem.v src/verilog/inst_mem_tb.v".format(2 ** sf['MEMORY_WIDTH'])
    system(cmd)

    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/inst_mem.out",
                        inst_reg=inst_reg,
                        inst_out=inst_out)
