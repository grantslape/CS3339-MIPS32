import unittest
from random import randint
from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal

import sys
sys.path.append("src/python")

from pc_mux_a import pc_mux_a, pc_mux_a_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


class TestPcMuxAHoldValue(TestCase):
    """Test that pc_mux_a holds state"""

    def setup(self):
        pc_src = Signal(intbv(0)[1:])
        nxt_pc = Signal(intbv(0x00000060)[32:])
        nxt_inst = Signal(intbv(0x00000060)[32:])
        imm_jmp_addr = Signal(intbv(0x00000faf)[32:])
        return pc_src, nxt_pc, nxt_inst, imm_jmp_addr

    def bench(self, pc_src, imm_jmp_addr, nxt_pc, nxt_inst, nxt_inst_v=intbv(0x00000060)):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.assertEqual(bin(pc_src ^ 0), bin(0))
            self.assertEqual(bin(nxt_pc ^ 0x00000060), bin(0))
            self.assertEqual(bin(nxt_inst ^ 0x00000060), bin(0))
            self.assertEqual(bin(nxt_inst_v ^ 0x00000060), bin(0))
            self.assertEqual(bin(imm_jmp_addr ^ 0x00000faf), bin(0))
            yield HALF_PERIOD

    def testHoldValuePython(self):
        """ Checking that module holds value when no input changes from Python """

        pc_src, nxt_pc, nxt_inst, imm_jmp_addr = self.setup()
        dut = pc_mux_a(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        stim = self.bench(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testHoldValueVerilog(self):
        """ Checking that module holds value when no input changes from Verilog """
        pc_src, nxt_pc, nxt_inst, imm_jmp_addr = self.setup()
        dut = pc_mux_a_v(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        stim = self.bench(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testHoldValueTogether(self):
        """ Checking that modules hold value when no input changes from Cosimulation """
        pc_src, nxt_pc, nxt_inst, imm_jmp_addr = self.setup()
        nxt_inst_v = Signal(intbv(0x00000060)[32:])
        dut = pc_mux_a(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        dut_v = pc_mux_a_v(pc_src, imm_jmp_addr, nxt_pc, nxt_inst_v)
        stim = self.bench(pc_src, imm_jmp_addr, nxt_pc, nxt_inst, nxt_inst_v)

        sim = Simulation(dut, dut_v, stim)
        sim.run(quiet=1)


class TestPcMuxACorrectOutput(TestCase):
    """ Test correct output of pc_mux_a """

    def setup(self):
        pc_src = Signal(intbv(0)[1:])
        nxt_pc, nxt_inst, imm_jmp_addr, nxt_inst = [Signal(intbv(0)[32:]) for i in range(4)]
        return pc_src, imm_jmp_addr, nxt_pc, nxt_inst

    def bench(self, pc_src, imm_jmp_addr, nxt_pc, nxt_inst):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            pc_src.next = ~pc_src
            nxt_pc.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))[32:]
            imm_jmp_addr.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))[32:]
            if pc_src == 1:
                self.assertEqual(bin(nxt_inst ^ imm_jmp_addr), bin(0))
            else:
                self.assertEqual(bin(nxt_inst ^ nxt_pc), bin(0))
            yield HALF_PERIOD

    def testCorrectOutputPython(self):
        """ Checking correct PC address is outputted from Python """
        pc_src, imm_jmp_addr, nxt_pc, nxt_inst = self.setup()
        dut = pc_mux_a(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        stim = self.bench(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testCorrectOutputVerilog(self):
        """ Checking correct PC address is outputted from Verilog """
        pc_src, imm_jmp_addr, nxt_pc, nxt_inst = self.setup()
        dut = pc_mux_a_v(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        stim = self.bench(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testCorrectOutputTogether(self):
        """ Checking correct PC address is outputted from Cosimulation """

        def test():
            for i in range(sf['DEFAULT_TEST_LENGTH']):
                if pc_src == 1:
                    self.assertEqual(bin(nxt_inst_v ^ imm_jmp_addr), bin(0))
                else:
                    self.assertEqual(bin(nxt_inst_v ^ nxt_pc), bin(0))
                yield HALF_PERIOD

        pc_src, imm_jmp_addr, nxt_pc, nxt_inst = self.setup()
        nxt_inst_v = Signal(intbv(0)[32:])
        dut = pc_mux_a(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        dut_v = pc_mux_a_v(pc_src, imm_jmp_addr, nxt_pc, nxt_inst_v)
        stim = self.bench(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)

        sim = Simulation(dut, dut_v, stim, test())
        sim.run(quiet=1)


if __name__ == '__main__':
    unittest.main()
