from myhdl import always_comb


def pc_mux_a(pc_src, imm_jmp_addr, nxt_pc, nxt_inst):
    """
    !! TODO: IMPLEMENT !!
    PC Mux A
    :param pc_src: Which instruction to use, 0 for nxt_pc, 1, for imm_jmp_addr.
    :param imm_jmp_addr: a new PC value from the EX/MEM register
    :param nxt_pc: sequential next PC from pc_adder
    :param nxt_inst: actual next instruction address to pc_mux_b
    :return: generator logic
    """

    @always_comb
    def logic():
        if pc_src == 0:
            nxt_inst.next = nxt_pc
        else:
            nxt_inst.next = imm_jmp_addr

    return logic
