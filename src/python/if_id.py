import os
from myhdl import always_comb, Cosimulation

def if_id(clock, if_id_write, nxt_pc, inst_in, op_code, rs, rt, imm, rd, funct_out, pc_out, top4, target_out):
    """
    IF/ID state register
    :param if_id_write: from hazard unit.  activate to stall by by keeping same outputs as last cycle
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
    # COULD NOT FIND SUBI IN THE MIPS OPCODE MAP ON A-50 IN BOOK
    @always_comb
    def PC_logic():
        if if_id_write == 1:
            # program counter logic
            pc_out.next = pc_out
            top4.next = top4
        else:
            # program counter logic
            pc_out.next = nxt_pc
            top4.next = nxt_pc[:28]


    @always_comb
    def INSTR_logic():
        # if if_id_write is true then do not update the state Register
        if if_id_write == 1:
            op_code.next = op_code
            # if r-type: add, sub, xor, jr
            if op_code == 0:
                rs.next = rs
                rt.next = rt
                rd.next = rd
                funct_out.next = funct_out
            # if i-type: addi, beq, lw, sw
            elif op_code == 8 or op_code == 4 or op_code == 35 or op_code == 43:
                rs.next = rs
                rt.next = rt
                imm.next = imm
            # if j-type: j, jal
            elif op_code == 2 or op_code == 3:
                target_out.next = target_out
            # don't know what to do when opcode not recognized
            # in this im going to assume mystery opcode is
            # the missing subi instruction B-)
            else:
                rs.next = rs
                rt.next = rt
                imm.next = imm
        # else update the register with the appropriate inputs
        else:
            op_code.next = op_code[:26]
            # if r-type: add, sub, xor, jr
            if op_code == 0:
                rs.next = inst_in[26:21]
                rt.next = inst_in[21:16]
                rd.next = inst_in[16:11]
                funct_out.next = inst_in[6:0]
            # if i-type: addi, beq, lw, sw
            elif op_code == 8 or op_code == 4 or op_code == 35 or op_code == 43:
                rs.next = inst_in[26:21]
                rt.next = inst_in[21:16]
                imm.next = inst_in[16:0]
            # if j-type: j, jal
            elif op_code == 2 or op_code == 3:
                target_out.next = inst_in[26:0]
            # don't know what to do when opcode not recognized
            # in this im going to assume mystery opcode is
            # the missing subi instruction
            else:
                rs.next = inst_in[26:21]
                rt.next = inst_in[21:16]
                imm.next = inst_in[16:0]

    return PC_logic, INSTR_logic


def if_id_v(clock, if_id_write, nxt_pc, inst_in, op_code, rs, rt, imm, rd, funct_out, pc_out, top4, target_out):
    """
    IF/ID state register
    :param if_id_write: from hazard unit.  activate to stall by by keeping same outputs as last cycle
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

    cmd = "iverilog -o bin/if_id.out src/verilog/if_id.v src/verilog/if_id_tb.v"
    os.system(cmd)

    return Cosimulation("vvp -m ./lib/myhdl.vpi bin/if_id.out",
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
                        target_out=target_out,
                        clock=clock)
