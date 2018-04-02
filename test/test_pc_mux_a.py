import unittest
from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal
import sys

sys.path.append("src")
from pc_mux_a import pc_mux_a
#import settings as sf


# TODO: Inject period and default test length
class TestPcMuxAPython(TestCase):

    def testHoldValuePython(self):
        """ Check that module holds value when no input changes """

        def test():
            for i in range(10000):
                pc_src.next = intbv(0)[1:]
                nxt_pc.next = intbv(0x00000060)[31:]
                nxt_inst.next = intbv(0x00000060)[31:]
                imm_jmp_addr.next = intbv(0x00000faf)[31:]
                print "pc_src: {0}, nxt_pc: {1}, imm_jmp_addr: {2}, nxt_inst: {3}".format(
                    bin(pc_src), bin(nxt_pc), bin(imm_jmp_addr), bin(nxt_inst))
                yield delay(10 / 2)

        pc_src = Signal(intbv(0)[1:])
        nxt_pc, nxt_inst, imm_jmp_addr = [Signal(intbv(0)[31:]) for i in range(3)]

        dut = pc_mux_a(pc_src, imm_jmp_addr, nxt_pc, nxt_inst)
        stim = test()
        sim = Simulation(dut, stim)
        sim.run(quiet=0)

        self.assertEqual(pc_src ^ 0, 0)
        self.assertEqual(bin(nxt_pc ^ 0x00000060), 0)
        self.assertEqual(bin(nxt_inst ^ 0x00000060), 0)
        self.assertEqual(bin(imm_jmp_addr ^ 0x00000faf), 0)

    def testCorrectOutputPython(self):
        """ Check that next sequential PC address is outputted when pc_src is deasserted
            and that the imm_jmp_addr value is outputted when pc_src is asserted."""


class TestPcMuxAVerilog(TestCase):

    def testHoldValueVerilog(self):
        """ Check that module holds value when no input changes """

    def testCorrectOutputVerilog(self):
        """ Check that next sequential PC address is outputted when pc_src is deasserted
            and that the imm_jmp_addr value is outputted when pc_src is asserted."""


class TestPCMuxATogether(TestCase):

    def testHoldValueTogether(self):
        """ Check that modules hold value when no input changes """

    def testCorrectOutputTogether(self):
        """ Check that next sequential PC address is outputted when pc_src is deasserted
            and that the imm_jmp_addr value is outputted when pc_src is asserted."""


if __name__ == '__main__':
    unittest.main()
