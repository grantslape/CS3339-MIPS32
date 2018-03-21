# MIPS 32 VERILOG SIMULATION

cpu:
	reg clock: this is the system clock
	program_counter: This is a simple module that is always set by pc_mux:
		input clock: system clock
		input [31:0] nxt_inst: next instruction address
		output [31:0] cur_pc: next instruction address goes to inst_mem
	pc_mux: Mux for program_counter input:
		input pc_src: which input to use.  From EX/MEM register
		input [31:0] jmp_addr: a new PC value from the EX/MEM register
		input [31:0] nxt_pc: sequential next PC from pc_adder
		output [31:0] nxt_inst: actual next instruction address to program_counter
	pc_adder: Increments to next sequential instruction address:
		input [31:0] cur_pc: current instruction address
		output [31:0] nxt_pc: next sequential instruction address to pc_mux
	inst_mem: Instruction Read unit and register:
		input [31:0] inst_reg: address to read from, from nxt_inst
		output [31:0] inst_out: instruction output to IF/ID state register
		[31:0] raw_mem [SIZE-1:0]: Instruction memory from a text file.  This should be an array of 32 bit regs
