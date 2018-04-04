import unittest
import sys
from random import randint

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

sys.path.append("src/python")
from pc_mux_b import pc_mux_b, pc_mux_b_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


@unittest.skip("PC Mux B not implemented")
class TestPcMuxB(TestCase):
    """Test PC Mux B"""
    def setUp(self):
        self.jmp_ctrl = Signal(intbv(0)[1:])
        self.nxt_inst_in, self.jmp_addr_in, self.next_address, self.next_address_v = [
            Signal(intbv(0)[32:]) for i in range(4)
        ]
        self.dut = pc_mux_b(self.jmp_ctrl, self.nxt_inst_in, self.jmp_addr_in, self.next_address)
        self.dut_v = pc_mux_b_v(self.jmp_ctrl, self.nxt_inst_in, self.jmp_addr_in, self.next_address_v)

    def deassert(self, next_address):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.jmp_ctrl.next = 0
            self.nxt_inst_in.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))
            self.jmp_addr_in.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(self.jmp_ctrl, 0)
            self.assertEqual(next_address, self.nxt_inst_in)
        raise StopSimulation

    def asserted(self, next_address):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.jmp_ctrl.next = 1
            self.nxt_inst_in.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))
            self.jmp_addr_in.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(self.jmp_ctrl, 0)
            self.assertEqual(next_address, self.jmp_addr_in)
        raise StopSimulation

    def dynamic(self, next_address):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.jmp_ctrl.next = randint(0, 1)
            self.nxt_inst_in.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))
            self.jmp_addr_in.next = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))
            yield HALF_PERIOD
            if self.jmp_ctrl == 0:
                self.assertEqual(next_address, self.nxt_inst_in)
            else:
                self.assertEqual(self.jmp_ctrl, 1)
                self.assertEqual(next_address, self.jmp_addr_in)
        raise StopSimulation

    def testPcMuxBDeassertedPython(self):
        """Checking that sequential address comes when deasserted Python"""
        stim = self.deassert(self.next_address)
        Simulation(self.dut, stim).run(quiet=1)

    def testPcMuxBDeassertedVerilog(self):
        """Checking that sequential address comes when deasserted Verilog"""
        stim = self.deassert(self.next_address_v)
        Simulation(self.dut_v, stim).run(quiet=1)

    def testPcMuxBDeassertedTogether(self):
        """Checking that sequential address comes when deasserted Cosimulation"""
        stim = self.deassert(self.next_address)
        stim_v = self.deassert(self.next_address_v)
        Simulation(self.dut, stim, self.dut_v, stim_v).run(quiet=1)

    def testPcMuxBAssertedPython(self):
        """Checking that sequential address comes when asserted Python"""
        stim = self.asserted(self.next_address)
        Simulation(self.dut, stim).run(quiet=1)

    def testPcMuxBAssertedVerilog(self):
        """Checking that sequential address comes when asserted Verilog"""
        stim = self.asserted(self.next_address_v)
        Simulation(self.dut_v, stim).run(quiet=1)

    def testPcMuxBAssertedTogether(self):
        """Checking that sequential address comes when asserted Cosimulation"""
        stim = self.asserted(self.next_address)
        stim_v = self.asserted(self.next_address_v)
        Simulation(self.dut, stim, self.dut_v, stim_v).run(quiet=1)

    def testPcMuxBDynamicPython(self):
        """Checking dynamic PC Mux B Python"""
        stim = self.dynamic(self.next_address)
        Simulation(self.dut, stim).run(quiet=1)

    def testPcMuxBDynamicVerilog(self):
        """Checking dynamic PC Mux B Verilog"""
        stim = self.dynamic(self.next_address_v)
        Simulation(self.dut_v, stim).run(quiet=1)

    def testPcMuxBDynamicTogether(self):
        """Checking dynamic PC Mux B Cosimulation"""
        stim = self.dynamic(self.next_address)
        stim_v = self.dynamic(self.next_address_v)
        Simulation(self.dut, stim, self.dut_v, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
