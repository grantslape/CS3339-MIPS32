import unittest
import sys
from random import randint

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

sys.path.append("src/python")
from pc_mux_b import pc_mux_b, pc_mux_b_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


def setup():
    jmp_ctrl = Signal(intbv(0)[1:])
    nxt_inst_in, jmp_addr_in, next_address = [Signal(intbv(0)[32:]) for i in range(3)]
    return jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address


class TestPcMuxBDeasserted(TestCase):

    def bench(self, jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            jmp_ctrl.next = 0
            nxt_inst_in = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))
            jmp_addr_in = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(jmp_ctrl, 0)
            self.assertEqual(next_address, nxt_inst_in)
        raise StopSimulation

    def testPcMuxBDeassertedPython(self):
        """Checking that sequential address comes when deasserted Python"""
        jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address = setup()
        dut = pc_mux_b(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)
        stim = self.bench(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testPcMuxBDeassertedVerilog(self):
        """Checking that sequential address comes when deasserted Verilog"""
        jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address = setup()
        dut = pc_mux_b_v(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)
        stim = self.bench(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testPcMuxBDeassertedTogether(self):
        """Checking that sequential address comes when deasserted Cosimulation"""
        def test():
            yield HALF_PERIOD
            self.assertEqual(next_address_v, nxt_inst_in)

        jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address = setup()
        next_address_v = Signal(intbv(0)[32:])
        dut = pc_mux_b(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)
        dut_v = pc_mux_b_v(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address_v)
        stim = self.bench(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)

        sim = Simulation(dut, dut_v, stim, test())
        sim.run(quiet=1)


class TestPcMuxBAsserted(TestCase):

    def bench(self, jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            jmp_ctrl.next = 1
            nxt_inst_in = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))
            jmp_addr_in = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))
            yield HALF_PERIOD
            self.assertEqual(jmp_ctrl, 0)
            self.assertEqual(next_address, jmp_addr_in)
        raise StopSimulation

    def testPcMuxBDeassertedPython(self):
        """Checking that sequential address comes when asserted Python"""
        jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address = setup()
        dut = pc_mux_b(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)
        stim = self.bench(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testPcMuxBDeassertedVerilog(self):
        """Checking that sequential address comes when asserted Verilog"""
        jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address = setup()
        dut = pc_mux_b_v(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)
        stim = self.bench(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testPcMuxBDeassertedTogether(self):
        """Checking that sequential address comes when asserted Cosimulation"""
        def test():
            yield HALF_PERIOD
            self.assertEqual(next_address_v, jmp_addr_in)

        jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address = setup()
        next_address_v = Signal(intbv(0)[32:])
        dut = pc_mux_b(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)
        dut_v = pc_mux_b_v(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address_v)
        stim = self.bench(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)

        sim = Simulation(dut, dut_v, stim, test())
        sim.run(quiet=1)


class TestPcMuxBDynamic(TestCase):

    def bench(self, jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            jmp_ctrl.next = randint(0, 1)
            nxt_inst_in = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))
            jmp_addr_in = intbv(randint(0, sf['UNSIGNED_MAX_VALUE']))
            yield HALF_PERIOD
            if jmp_ctrl == 0:
                self.assertEqual(next_address, nxt_inst_in)
            else:
                self.assertEqual(jmp_ctrl, 1)
                self.assertEqual(next_address, jmp_addr_in)
        raise StopSimulation

    def testPcMuxBDynamicPython(self):
        """Checking dynamic PC Mux B Python"""
        jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address = setup()
        dut = pc_mux_b(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)
        stim = self.bench(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testPcMuxBDeassertedVerilog(self):
        """Checking dynamic PC Mux B Verilog"""
        jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address = setup()
        dut = pc_mux_b_v(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)
        stim = self.bench(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testPcMuxBDeassertedTogether(self):
        """Checking dynamic PC Mux B Cosimulation"""
        def test():
            yield HALF_PERIOD
            if jmp_ctrl == 0:
                self.assertEqual(next_address_v, nxt_inst_in)
            else:
                self.assertEqual(next_address_v, jmp_addr_in)

        jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address = setup()
        next_address_v = Signal(intbv(0)[32:])
        dut = pc_mux_b(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)
        dut_v = pc_mux_b_v(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address_v)
        stim = self.bench(jmp_ctrl, nxt_inst_in, jmp_addr_in, next_address)

        sim = Simulation(dut, dut_v, stim, test())
        sim.run(quiet=1)


if __name__ == '__main__':
    unittest.main()
