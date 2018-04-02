import os

from myhdl import always_comb, Cosimulation


def pc_mux_a(pc_src, imm_jmp_addr, nxt_pc, nxt_inst):
    """
    PC Mux A
    :param pc_src: Which instruction to use, 0 for nxt_pc, 1, for imm_jmp_addr.
    :param imm_jmp_addr: a new PC value from the EX/MEM register
    :param nxt_pc: sequential next PC from pc_adder
    :param nxt_inst: actual next instruction address to pc_mux_b
    :return: generator logic
    """

    @always_comb
    def logic():
        if pc_src == 1:
            nxt_inst.next = imm_jmp_addr
        else:
            nxt_inst.next = nxt_pc

    return logic


def pc_mux_a_v(pc_src, imm_jmp_addr, nxt_pc, nxt_inst):
    """
    Instantiate Verilog module
    :param pc_src: Which instruction to use, 0 for nxt_pc, 1, for imm_jmp_addr.
    :param imm_jmp_addr: a new PC value from the EX/MEM register
    :param nxt_pc: sequential next PC from pc_adder
    :param nxt_inst: actual next instruction address to pc_mux_b
    :return: Cosimulation
    """
    cmd = "iverilog -o pc_mux_a.out src/verilog/pc_mux_a.v pc_mux_a_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m lib/cosimulation/myhdl.vpi pc_mux_a.out",
                        pc_src=pc_src,
                        imm_jmp_addr=imm_jmp_addr,
                        nxt_pc=nxt_pc,
                        nxt_inst=nxt_inst)
