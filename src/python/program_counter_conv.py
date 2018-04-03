from myhdl import Signal, intbv, toVerilog, ResetSignal

from program_counter import program_counter 

clock = Signal(bool(0))
cur_pc = Signal(intbv(0)[32:])
nxt_pc = Signal(intbv(0)[32:])

program_counter_inst = toVerilog(program_counter, clock, cur_pc, nxt_pc)

