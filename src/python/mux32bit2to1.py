import os

from myhdl import always_comb, Cosimulation

def mux32bit2to1(ctrl_line, input1, input2, output):
	"""
	32_bit_2_to_1_mux

	:param ctrl_line: Which input should be output. If 1 input2 else input1
	:param input1: first 32-bit input
	:param input2: second 32-bit input
	:param output: 32-bit output
	:return: generator logic
	"""

	@always_comb
	def logic():
		if ctrl_line == 0:
			output.next = input1
		else:
			output.next = input2
	return

def mux32bit2to1_v(ctrl_line, input1, input2, output):
	"""
	Instantiate Vefilog module

	:param ctrl_line: Which input should be output. If 1 input2 else input1
	:param input1: first 32-bit input
	:param input2: second 32-bit input
	:param output: 32-bit output
	:return: Cosimulation 
	"""
	cmd = "iverilog -o 32_bit_2_to_1_mux.out src/verilog/32_bit_2_to_1_mux.v src/verilog/32_bit_2_to_1_mux_tb.v"
	os.system(cmd)

	return Cosimulation("vvp -m lib/myhdl.vpi 32_bit_2_to_1_mux.out",
			ctrl_line = ctrl_line,
			input1 = input1,
			input2 = input2,
			output = output)	
