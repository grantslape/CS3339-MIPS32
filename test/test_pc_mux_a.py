import unittest
from random import randint
from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal

import sys
sys.path.append("src/python")

from pc_mux_a import pc_mux_a, pc_mux_a_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


class TestPcMuxA(TestCase):
    """Test that pc_mux_a holds state"""

    def setUp(self):
        self.pc_src = Signal(intbv(0)[1:])
        self.nxt_pc = Signal(intbv(0x00000060)[32:])
        self.nxt_inst = Signal(intbv(0x00000060)[32:])
        self.nxt_inst_v = Signal(intbv(0x00000060)[32:])
        self.imm_jmp_addr = Signal(intbv(0x00000faf)[32:])
        self.dut = pc_mux_a(self.pc_src, self.imm_jmp_addr, self.nxt_pc, self.nxt_inst)

    def zero_test(self):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.assertEqual(bin(self.pc_src ^ 0), bin(0))
            self.assertEqual(bin(self.nxt_pc ^ 0x00000060), bin(0))
            self.assertEqual(bin(self.nxt_inst ^ 0x00000060), bin(0))
            self.assertEqual(bin(self.nxt_inst_v ^ 0x00000060), bin(0))
            self.assertEqual(bin(self.imm_jmp_addr ^ 0x00000faf), bin(0))
            yield HALF_PERIOD

    def output_test(self, nxt_inst):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.pc_src.next = ~self.pc_src
            self.nxt_pc.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))[32:]
            self.imm_jmp_addr.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))[32:]
            if self.pc_src == 1:
                self.assertEqual(bin(nxt_inst ^ self.imm_jmp_addr), bin(intbv(0)[32:]))
            else:
                self.assertEqual(bin(nxt_inst ^ self.nxt_pc), bin(intbv(0)[32:]))
            yield HALF_PERIOD

    def testHoldValuePython(self):
        """ Checking that module holds value when no input changes from Python """
        stim = self.zero_test()

        Simulation(self.dut, stim).run(quiet=1)

    def testHoldValueVerilog(self):
        """ Checking that module holds value when no input changes from Verilog """
        stim = self.zero_test()
        dut_v = pc_mux_a_v(self.pc_src, self.imm_jmp_addr, self.nxt_pc, self.nxt_inst_v)

        Simulation(dut_v, stim).run(quiet=1)

    def testHoldValueTogether(self):
        """ Checking that modules hold value when no input changes from Cosimulation """
        stim = self.zero_test()
        dut_v = pc_mux_a_v(self.pc_src, self.imm_jmp_addr, self.nxt_pc, self.nxt_inst_v)

        Simulation(self.dut, dut_v, stim).run(quiet=1)

    def testCorrectOutputPython(self):
        """ Checking correct PC address is outputted from Python """
        stim = self.output_test(self.nxt_inst)

        sim = Simulation(self.dut, stim)
        sim.run(quiet=1)

    def testCorrectOutputVerilog(self):
        """ Checking correct PC address is outputted from Verilog """
        stim = self.output_test(self.nxt_inst_v)
        dut_v = pc_mux_a_v(self.pc_src, self.imm_jmp_addr, self.nxt_pc, self.nxt_inst_v)

        sim = Simulation(dut_v, stim)
        sim.run(quiet=1)

    def testCorrectOutputTogether(self):
        """ Checking correct PC address is outputted from Cosimulation """
        dut_v = pc_mux_a_v(self.pc_src, self.imm_jmp_addr, self.nxt_pc, self.nxt_inst_v)
        stim = self.output_test(self.nxt_inst)
        stim_v = self.output_test(self.nxt_inst_v)

        sim = Simulation(self.dut, dut_v, stim, stim_v)
        sim.run(quiet=1)


if __name__ == '__main__':
    unittest.main()
