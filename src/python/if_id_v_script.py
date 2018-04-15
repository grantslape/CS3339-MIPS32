from myhdl import toVerilog, Signal, intbv
from if_id import if_id

if_id_write = Signal(bool(0))
nxt_pc = Signal(intbv(0)[31:0])
inst_in = Signal(intbv(0)[31:0])
op_code = Signal(intbv(0)[5:0])
rs = Signal(intbv(0)[4:0])
rt = Signal(intbv(0)[4:0])
imm = Signal(intbv(0)[16:0])
rd = Signal(intbv(0)[4:0])
funct_out = Signal(intbv(0)[6:0])
pc_out = Signal(intbv(0)[31:0])
top4 = Signal(intbv(0)[4:0])
target_out = Signal(intbv(0)[26:0])

toVerilog(if_id, if_id_write, nxt_pc, inst_in, op_code, rs, rt, imm, rd, funct_out, pc_out, top4, target_out)

# count = Signal(intbv(0)[m:])
# enable = Signal(bool(0))
# clock, reset = [Signal(bool()) for i in range(2)]
#
# if_id: IF/ID state register
# 		input if_id_write: from hazard unit.  activate to stall by by keeping same outputs as last cycle
# 		input [31:0] nxt_pc: next sequential instruction address
# 		input [31:0] inst_in: Instruction input from inst_mem.inst_out
# 		output [31:26] op_code: sliced from inst_in, Forward to ctrl.funct_in
# 		output [25:21] rs: sliced from inst_in, sent to rfile.r_addr1, id_ex, hazard_unit.if_id_rs
# 		output [20:16] rt: sliced from inst_in, sent to rfile.r_addr2, id_ex, hazard_unit.if_id_rt
# 		output [15:0] imm: sliced from inst_in, sent to sign_extender
# 		output [15:11] rd: sliced from inst_in, sent to id_ex
# 		output [5:0] funct_out: function code sliced from inst_in to ctrl
# 		output [31:0] pc_out: nxt_pc.  to id_ex
# 		output [3:0] top4: top 4 bits of nxt_pc
# 		output [25:0] target_out: 26 bit jump immediate
