# MIPS 32 VERILOG SIMULATION

cpu:
	reg clock: this is the system clock
	program_counter: This is a simple module that is always set by pc_mux:
		input clock: inherit from system clock
		input new_pc: from pc_mux, assigned to nxt_inst
		output [31:0] nxt_inst: next instruction address
	pc_inc: simple incrementor for PC.  separated b/c we need this output in multiple places:
		input [31:0] cur_pc: current pc from nxt_inst
		output [31:0] nxt_pc: cur_pc + 4, to pc_mux
		output [3:0] sign_out: [31:28] nxt_pc to sign_extender
	inst_mem: Instruction Read unit and register:
		input clock: inherit from system clock
		input reg [31:0] inst_reg: address to read from, from nxt_inst
		output TODO: outputs to reg and jump unit?
		raw_mem: Instruction memory from a text file.  This could be it's own module, or an array of instructions.
	branch_pred: Branch Predictor / Jump Handler:
		input [31:0] nxt_inst: from program_counter
	pc_mux: Mux for program_counter input:
		input pc_src: which input to use.  from branch_pred 0: cur_pc, 1: jmp_addr.
		input [31:0] cur_pc: from pc_inc
		input [31:0] jmp_addr: A new PC address from the jump unit
		output [31:0] nxt_pc: Actual next PC value
	sign_extender: Sign Extension Unit
		input [15:0] imm_in: 16-bit immediate field from inst_mem
		input [3:0] pc_in: from pc_inc
		output [31:0] 

