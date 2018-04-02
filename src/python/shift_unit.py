import os

from myhdl import always_comb, Cosimulation

def shift_unit(imm_in, imm_out):
	"""
	Shift Unit
	:param imm_in: The sign-extended 32 bit immediate values
	:return: The sign-extended value has been shifted left two bits.
	"""
	
	@always_comb
	def logic():
		imm_out = imm_in << 2
	
	return logic

def shift_unit_v(imm_in, imm_out):
	"""
	:param imm_in: The sign-extended 32 bit immediate values
	:return: The sign-extended value has been shifted left two bits.
	"""
        
	cmd = "iverilog -o shift_unit.out shift_unit.v shift_unit_tb.v"
	os.System(cmd)
	
	return Cosimulation("vvp -m ./myhdl.vpi shift_unit.out",
			imm_in=imm_in,
			imm_out=imm_out)
