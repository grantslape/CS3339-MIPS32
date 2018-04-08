import os
from myhdl import always_comb,Cosimulation

def if_id(nxt_pc, top4, inst_in, funct_out, rs, rt, imm, rd, top4_out):
    """
    IF/ID state register
    :param nxt_pc: next sequential instruction address
    :param top4: top 4 bits of nxt_pc. From pc_adder
    :param inst_in: Instruction input from inst_mem.inst_out
    :param funct_out: Forward inst_in to id_ex, ctrl.funct_in
    :param rs: sliced from inst_in, sent to rfile.r_addr1, id_ex, hazard_unit.if_id_rs
    :param rt: sliced from inst_in, sent to rfile.r_addr2, id_ex, hazard_unit.if_id_rt
    :param imm: sliced from inst_in, sent to sign_extender
    :param rd: sliced from inst_in, sent to id_ex
    :param top4_out: top 4 bits of nxt_pc.  to id_ex
    :return: generator logic
    """

    @always_comb
    def logic():
        pass
    return logic


def if_id_v(nxt_pc, top4, inst_in, funct_out, rs, rt, imm, rd, top4_out):
    """
    IF/ID state register
    :param nxt_pc: next sequential instruction address
    :param top4: top 4 bits of nxt_pc. From pc_adder
    :param inst_in: Instruction input from inst_mem.inst_out
    :param funct_out: Forward inst_in to id_ex, ctrl.funct_in
    :param rs: sliced from inst_in, sent to rfile.r_addr1, id_ex, hazard_unit.if_id_rs
    :param rt: sliced from inst_in, sent to rfile.r_addr2, id_ex, hazard_unit.if_id_rt
    :param imm: sliced from inst_in, sent to sign_extender
    :param rd: sliced from inst_in, sent to id_ex
    :param top4_out: top 4 bits of nxt_pc.  to id_ex
    :return: generator logic
    """

    cmd = "iverilog -o bin/if_id.out src/verilog/if_id.v src/verilog/if_id_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/if_id.out",
                        nxt_pc=nxt_pc,
                        top4=top4,
                        inst_in=inst_in,
                        funct_out=funct_out,
                        rs=rs,
                        rt=rt,
                        imm=imm,
                        rd=rd,
                        top4_out=top4_out)
