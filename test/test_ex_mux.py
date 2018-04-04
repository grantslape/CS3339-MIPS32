import unittest
import sys
from random import randint

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation

sys.path.append("src/python")
from ex_mux import ex_mux, ex_mux_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


def setup():
    reg_dst = Signal(intbv(0)[1:])
    rt_in, rd_in, dest = [Signal(intbv(0)[5:]) for i in range(3)]
    return reg_dst, rt_in, rd_in, dest


@unittest.skip("Ex Mux not implemented")
class TestExMuxDeasserted(TestCase):
    """Test when reg_dst is deasserted"""
    def bench(self, reg_dst, rt_in, rd_in, dest):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            reg_dst.next = 0
            rt_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            rd_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            while rd_in == rt_in:
                rd_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            yield HALF_PERIOD
            self.assertEqual(dest, rt_in)
            self.assertNotEquals(dest, rd_in)
        raise StopSimulation

    def testExMuxDeassertedPython(self):
        """Check that RT is returned when reg_dst deasserted Python"""
        reg_dst, rt_in, rd_in, dest = setup()
        dut = ex_mux(reg_dst, rt_in, rd_in, dest)
        stim = self.bench(reg_dst, rt_in, rd_in, dest)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testExMuxDeassertedVerilog(self):
        """Check that RT is returned when reg_dst deasserted Verilog"""
        reg_dst, rt_in, rd_in, dest = setup()
        dut = ex_mux_v(reg_dst, rt_in, rd_in, dest)
        stim = self.bench(reg_dst, rt_in, rd_in, dest)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testExMuxDeassertedTogether(self):
        """Check that RT is returned when reg_dst deasserted Together"""
        reg_dst, rt_in, rd_in, dest = setup()
        dest_v = Signal(intbv(0)[5:])
        dut = ex_mux(reg_dst, rt_in, rd_in, dest)
        dut_v = ex_mux_v(reg_dst, rt_in, rd_in, dest_v)
        stim = self.bench(reg_dst, rt_in, rd_in, dest)
        stim_v = self.bench(reg_dst, rt_in, rd_in, dest_v)

        sim = Simulation(dut, dut_v, stim, stim_v)
        sim.run(quiet=1)


@unittest.skip("Ex Mux not implemented")
class TestExMuxAsserted(TestCase):
    """Test when reg_dst is asserted"""
    def bench(self, reg_dst, rt_in, rd_in, dest):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            reg_dst.next = 1
            rt_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            rd_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            while rd_in == rt_in:
                rd_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            yield HALF_PERIOD
            self.assertEqual(dest, rd_in)
            self.assertNotEquals(dest, rt_in)
        raise StopSimulation

    def testExMuxAssertedPython(self):
        """Check that RT is returned when reg_dst Asserted Python"""
        reg_dst, rt_in, rd_in, dest = setup()
        dut = ex_mux(reg_dst, rt_in, rd_in, dest)
        stim = self.bench(reg_dst, rt_in, rd_in, dest)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testExMuxAssertedVerilog(self):
        """Check that RT is returned when reg_dst Asserted Verilog"""
        reg_dst, rt_in, rd_in, dest = setup()
        dut = ex_mux_v(reg_dst, rt_in, rd_in, dest)
        stim = self.bench(reg_dst, rt_in, rd_in, dest)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testExMuxAssertedTogether(self):
        """Check that RT is returned when reg_dst Asserted Together"""
        reg_dst, rt_in, rd_in, dest = setup()
        dest_v = Signal(intbv(0)[5:])
        dut = ex_mux(reg_dst, rt_in, rd_in, dest)
        dut_v = ex_mux_v(reg_dst, rt_in, rd_in, dest_v)
        stim = self.bench(reg_dst, rt_in, rd_in, dest)
        stim_v = self.bench(reg_dst, rt_in, rd_in, dest_v)

        sim = Simulation(dut, dut_v, stim, stim_v)
        sim.run(quiet=1)


@unittest.skip("Ex Mux not implemented")
class TestExMuxDynamic(TestCase):
    """Test dynamic behavior"""
    def bench(self, reg_dst, rt_in, rd_in, dest):
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            reg_dst.next = randint(0, 1)
            rt_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            rd_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            while rd_in == rt_in:
                rd_in.next = intbv(randint(0, sf['WIDTH']))[5:]
            yield HALF_PERIOD
            if reg_dst == 0:
                self.assertEqual(dest, rt_in)
                self.assertNotEquals(dest, rd_in)
            else:
                self.assertEqual(reg_dst, 1)
                self.assertEqual(dest, rd_in)
                self.assertNotEquals(dest, rt_in)
        raise StopSimulation

    def testExMuxDynamicPython(self):
        """Check dynamic behavior Python"""
        reg_dst, rt_in, rd_in, dest = setup()
        dut = ex_mux(reg_dst, rt_in, rd_in, dest)
        stim = self.bench(reg_dst, rt_in, rd_in, dest)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testExMuxDynamicVerilog(self):
        """Check dynamic behavior Verilog"""
        reg_dst, rt_in, rd_in, dest = setup()
        dut = ex_mux_v(reg_dst, rt_in, rd_in, dest)
        stim = self.bench(reg_dst, rt_in, rd_in, dest)

        sim = Simulation(dut, stim)
        sim.run(quiet=1)

    def testExMuxDynamicTogether(self):
        """Check dynamic behavior Together"""
        reg_dst, rt_in, rd_in, dest = setup()
        dest_v = Signal(intbv(0)[5:])
        dut = ex_mux(reg_dst, rt_in, rd_in, dest)
        dut_v = ex_mux_v(reg_dst, rt_in, rd_in, dest_v)
        stim = self.bench(reg_dst, rt_in, rd_in, dest)
        stim_v = self.bench(reg_dst, rt_in, rd_in, dest_v)

        sim = Simulation(dut, dut_v, stim, stim_v)
        sim.run(quiet=1)


if __name__ == '__main__':
    unittest.main()
