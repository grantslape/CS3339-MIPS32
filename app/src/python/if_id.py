"""IF/ID state register"""
from os import system
from myhdl import always, Cosimulation, block


@block
def if_id(clock, if_id_write, nxt_pc, inst_in, op_code, rs, rt, imm, rd, funct_out, pc_out, top4,
          target_out):
    """
    IF/ID state register
    :param clock system clock
    :param if_id_write: from hazard unit.  activate to stall by keeping same outputs as last cycle
    :param reset: clear it all out (flush) from ctrl
    :param nxt_pc: next sequential instruction address
    :param inst_in: Instruction input from inst_mem.inst_out
    :param op_code: sliced from inst_in, Forward to ctrl.funct_in
    :param rs: sliced from inst_in, sent to rfile.r_addr1, id_ex, hazard_unit.if_id_rs
    :param rt: sliced from inst_in, sent to rfile.r_addr2, id_ex, hazard_unit.if_id_rt
    :param imm: sliced from inst_in, sent to sign_extender
    :param rd: sliced from inst_in, sent to id_ex
    :param funct_out: Forward inst_in to id_ex, ctrl.funct_in
    :param pc_out: nxt_pc.  to id_ex
    :param top4: top 4 bits of nxt_pc. From pc_adder
    :param target_out: 26 bit jump immediate
    """
    @always(clock.posedge)
    def logic():
        # if if_id_write is true then do not update the state Register
        if if_id_write == 1:
            pass
        else:
            # program counter logic
            pc_out.next = nxt_pc
            top4.next = nxt_pc[32:28]

            # instruction logic
            op_code.next = inst_in[32:26]
            rs.next = inst_in[26:21]
            rt.next = inst_in[21:16]
            rd.next = inst_in[16:11]
            funct_out.next = inst_in[6:0]
            imm.next = inst_in[16:0].signed()
            target_out.next = inst_in[26:0]

    return logic


def if_id_v(clock, if_id_write, nxt_pc, inst_in, op_code, rs, rt, imm, rd, funct_out, pc_out, top4,
            target_out):
    """
    IF/ID state register
    :param clock system clock
    :param if_id_write: from hazard unit.  activate to stall by keeping same outputs as last cycle
    :param nxt_pc: next sequential instruction address
    :param inst_in: Instruction input from inst_mem.inst_out
    :param op_code: sliced from inst_in, Forward to ctrl.funct_in
    :param rs: sliced from inst_in, sent to rfile.r_addr1, id_ex, hazard_unit.if_id_rs
    :param rt: sliced from inst_in, sent to rfile.r_addr2, id_ex, hazard_unit.if_id_rt
    :param imm: sliced from inst_in, sent to sign_extender
    :param rd: sliced from inst_in, sent to id_ex
    :param funct_out: Forward inst_in to id_ex, ctrl.funct_in
    :param pc_out: nxt_pc.  to id_ex
    :param top4: top 4 bits of nxt_pc. From pc_adder
    :param target_out: 26 bit jump immediate
    :param reset: clear it all out (flush) from ctrl
    """

    cmd = "iverilog -o bin/if_id.out src/verilog/if_id.v src/verilog/if_id_tb.v"
    system(cmd)

    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/if_id.out",
                        clock=clock,
                        if_id_write=if_id_write,
                        nxt_pc=nxt_pc,
                        inst_in=inst_in,
                        op_code=op_code,
                        rs=rs,
                        rt=rt,
                        imm=imm,
                        rd=rd,
                        funct_out=funct_out,
                        pc_out=pc_out,
                        top4=top4,
                        target_out=target_out)
