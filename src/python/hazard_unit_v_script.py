from myhdl import toVerilog, Signal, intbv
from hazard_unit import hazard_unit

if_id_rs = Signal(intbv(0)[4:0])
if_id_rt = Signal(intbv(0)[4:0])
id_ex_rt = Signal(intbv(0)[4:0])
mem_read = Signal(bool(0))
pc_write = Signal(bool(0))
if_id_write = Signal(bool(0))
ex_stall = Signal(bool(0))

hazard_unit_toV = toVerilog(hazard_unit,if_id_rs,if_id_rt,id_ex_rt, mem_read, pc_write, if_id_write, ex_stall)

# count = Signal(intbv(0)[m:])
# enable = Signal(bool(0))
# clock, reset = [Signal(bool()) for i in range(2)]
