import unittest
from random import randint
from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, Cosimulation
import sys

sys.path.append("src/python")
from pc_mux_a import pc_mux_a, pc_mux_a_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


class TestPcMuxAHoldValue(TestCase):

    def testHoldValuePython(self):
        """ Check that module holds value when no input changes """
        def test():
            for i in range(sf['DEFAULT_TEST_LENGTH']):
                # TODO: Use a logger for this
                # print "pc_src: {0}, nxt_pc: {1}, imm_jmp_addr: {2}, nxt_inst: {3}".format(
                #     bin(pc_src), bin(nxt_pc), bin(imm_jmp_addr), bin(nxt_inst))
                self.assertEqual(bin(pc_src ^ 0), bin(0))
                self.assertEqual(bin(nxt_pc ^ 0x00000060), bin(0))
                self.assertEqual(bin(nxt_inst ^ 0x00000060), bin(0))
                self.assertEqual(bin(imm_jmp_addr ^ 0x00000faf), bin(0))
                yield HALF_PERIOD

        pc_src = Signal(intbv(0)[1:])
        nxt_pc = Signal(intbv(0x00000060)[32:])
        nxt_inst = Signal(intbv(0x00000060)[32:])
        imm_jmp_addr = Signal(intbv(0x00000faf)[32:])

        dut = pc_mux_a(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        stim = test()
        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testHoldValueVerilog(self):
        """ Check that module holds value when no input changes """
        def test():
                # TODO: Use a logger for this
                # print "pc_src: {0}, nxt_pc: {1}, imm_jmp_addr: {2}, nxt_inst: {3}".format(
                #     bin(pc_src), bin(nxt_pc), bin(imm_jmp_addr), bin(nxt_inst))
                self.assertEqual(bin(pc_src ^ 0), bin(0))
                self.assertEqual(bin(nxt_pc ^ 0x00000060), bin(0))
                self.assertEqual(bin(nxt_inst ^ 0x00000060), bin(0))
                self.assertEqual(bin(imm_jmp_addr ^ 0x00000faf), bin(0))
                yield HALF_PERIOD

        pc_src = Signal(intbv(0)[1:])
        nxt_pc = Signal(intbv(0x00000060)[32:])
        nxt_inst = Signal(intbv(0x00000060)[32:])
        imm_jmp_addr = Signal(intbv(0x00000faf)[32:])

        dut = pc_mux_a_v(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        stim = test()
        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testHoldValueTogether(self):
        """ Check that modules hold value when no input changes """
        def test():
            for i in range(sf['DEFAULT_TEST_LENGTH']):
                # TODO: Use a logger for this
                # print "pc_src: {0}, nxt_pc: {1}, imm_jmp_addr: {2}, nxt_inst: {3}".format(
                #     bin(pc_src), bin(nxt_pc), bin(imm_jmp_addr), bin(nxt_inst))
                self.assertEqual(bin(pc_src ^ 0), bin(0))
                self.assertEqual(bin(nxt_pc ^ 0x00000060), bin(0))
                self.assertEqual(bin(nxt_inst ^ 0x00000060), bin(0))
                self.assertEqual(bin(nxt_inst_v ^ 0x00000060), bin(0))
                self.assertEqual(bin(imm_jmp_addr ^ 0x00000faf), bin(0))
                yield HALF_PERIOD

        pc_src = Signal(intbv(0)[1:])
        nxt_pc = Signal(intbv(0x00000060)[32:])
        nxt_inst, nxt_inst_v = [Signal(intbv(0x00000060)[32:]) for i in range(2)]
        imm_jmp_addr = Signal(intbv(0x00000faf)[32:])

        dut = pc_mux_a(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        dut_v = pc_mux_a_v(pc_src, imm_jmp_addr, nxt_pc, nxt_inst_v)
        stim = test()
        sim = Simulation(dut, dut_v, stim)
        sim.run(quiet=1)


class TestPcMuxACorrectOutput(TestCase):

    def testCorrectOutputPython(self):
        """ Check that next sequential PC address is outputted when pc_src is deasserted
            and that the imm_jmp_addr value is outputted when pc_src is asserted."""
        def test():
            for i in range(sf['DEFAULT_TEST_LENGTH']):
                pc_src.next = ~pc_src
                nxt_pc.next = intbv(randint(0, 2**31))[32:]
                imm_jmp_addr.next = intbv(randint(0, 2**31))[32:]
                if pc_src == 1:
                    nxt_inst.next = imm_jmp_addr
                    self.assertEqual(bin(nxt_inst ^ imm_jmp_addr), bin(0))
                else:
                    nxt_inst.next = pc_src
                    self.assertEqual(bin(nxt_inst ^ nxt_pc), bin(0))
                yield HALF_PERIOD

        pc_src = Signal(intbv(0)[1:])
        nxt_pc, nxt_inst, imm_jmp_addr = [Signal(intbv(0)[32:]) for i in range(3)]
        dut = pc_mux_a(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        stim = test()
        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testCorrectOutputVerilog(self):
        """ Check that next sequential PC address is outputted when pc_src is deasserted
            and that the imm_jmp_addr value is outputted when pc_src is asserted."""
        def test():
            for i in range(sf['DEFAULT_TEST_LENGTH']):
                pc_src.next = ~pc_src
                nxt_pc.next = intbv(randint(0, 2**31))[32:]
                imm_jmp_addr.next = intbv(randint(0, 2**31))[32:]
                if pc_src == 1:
                    nxt_inst.next = imm_jmp_addr
                    self.assertEqual(bin(nxt_inst ^ imm_jmp_addr), bin(0))
                else:
                    nxt_inst.next = pc_src
                    self.assertEqual(bin(nxt_inst ^ nxt_pc), bin(0))
                yield HALF_PERIOD

        pc_src = Signal(intbv(0)[1:])
        nxt_pc, nxt_inst, imm_jmp_addr = [Signal(intbv(0)[32:]) for i in range(3)]
        dut = pc_mux_a_v(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        stim = test()
        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testCorrectOutputTogether(self):
        """ Check that next sequential PC address is outputted when pc_src is deasserted
            and that the imm_jmp_addr value is outputted when pc_src is asserted."""

        def test():
            for i in range(sf['DEFAULT_TEST_LENGTH']):
                pc_src.next = ~pc_src
                nxt_pc.next = intbv(randint(0, 2**31))[32:]
                imm_jmp_addr.next = intbv(randint(0, 2**31))[32:]
                if pc_src == 1:
                    nxt_inst.next = imm_jmp_addr
                    self.assertEqual(bin(nxt_inst ^ imm_jmp_addr), bin(0))
                    self.assertEqual(bin(nxt_inst_v ^ imm_jmp_addr), bin(0))
                else:
                    nxt_inst.next = pc_src
                    self.assertEqual(bin(nxt_inst ^ nxt_pc), bin(0))
                    self.assertEqual(bin(nxt_inst_v ^ nxt_pc), bin(0))
                yield HALF_PERIOD

        pc_src = Signal(intbv(0)[1:])
        nxt_pc, nxt_inst, nxt_inst_v, imm_jmp_addr = [Signal(intbv(0)[32:]) for i in range(4)]
        dut = pc_mux_a(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        dut_v = pc_mux_a_v(pc_src, imm_jmp_addr, nxt_pc, nxt_inst_v)
        stim = test()
        sim = Simulation(dut, dut_v, stim)
        sim.run(quiet=1)


if __name__ == '__main__':
    unittest.main()
