"""WB stage multiplexer unit tests"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import intbv, Simulation, Signal, StopSimulation
from src.python.wb_mux import wb_mux, wb_mux_v
from src.commons.settings import settings as sf
from src.commons.signal_generator import signed_signal_set, random_signed_intbv
from src.commons.clock import half_period

class TestWBMux(TestCase):
    """ Test WB mux sel wire asserted/deasserted """
    def setUp(self):
        self.sel = Signal(intbv(0)[1:])
        self.rdata_in, self.result_in, self.wb_out, self.wb_out_v = signed_signal_set(4)
        self.dut = wb_mux(self.sel, self.wb_out, self.rdata_in, self.result_in)

    def deassert(self, wb_out):
        """Deassertion stimulus"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.sel.next = Signal(intbv(0, min=0, max=2))
            self.rdata_in.next = random_signed_intbv()
            self.result_in.next = random_signed_intbv()
            while self.result_in.next == self.rdata_in.next:
                self.result_in.next = random_signed_intbv()
            yield half_period()
            #print "wb_out: {}, result_in: {}".format(wb_out, self.result_in)
            self.assertEqual(wb_out, self.result_in)
            self.assertNotEquals(wb_out, self.rdata_in)
        raise StopSimulation

    def asserted(self, wb_out):
        """Assertion stimulus"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.sel.next = Signal(intbv(1, min=0, max=2))
            self.rdata_in.next = random_signed_intbv()
            self.result_in.next = random_signed_intbv()
            while self.result_in.next == self.rdata_in.next:
                self.result_in.next = random_signed_intbv()
            yield half_period()
            #print "wb_out: {}, result_in: {}".format(wb_out, self.result_in)
            self.assertEqual(wb_out, self.rdata_in)
            self.assertNotEquals(wb_out, self.result_in)
        raise StopSimulation

    def dynamic(self, wb_out):
        """Test Dynamic functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.sel.next = Signal(intbv(randint(0, 1))[1:])
            self.rdata_in.next = random_signed_intbv()
            self.result_in.next = random_signed_intbv()
            while self.result_in.next == self.rdata_in.next:
                self.result_in.next = random_signed_intbv()
            yield half_period()
            if self.sel == 0:
                self.assertEqual(wb_out, self.result_in)
                self.assertNotEquals(wb_out, self.rdata_in)
            else:
                self.assertEqual(self.sel, 1)
                self.assertEqual(wb_out, self.rdata_in)
                self.assertNotEquals(wb_out, self.result_in)
        raise StopSimulation

    def testWBMuxDeassertedPython(self):
        """Check that ALU result is returned when sel deasserted Python"""
        stim = self.deassert(self.wb_out)
        Simulation(self.dut, stim).run(quiet=1)

    def testWBMuxDeassertedVerilog(self):
        """Check that ALU result is returned when sel deasserted Verilog"""
        dut_v = wb_mux_v(self.sel, self.wb_out_v, self.rdata_in, self.result_in)
        stim = self.deassert(self.wb_out_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testWBMuxDeassertedTogether(self):
        """Check that ALU result is returned when sel deasserted Together"""
        dut_v = wb_mux_v(self.sel, self.wb_out_v, self.rdata_in, self.result_in)
        stim = self.deassert(self.wb_out)
        stim_v = self.deassert(self.wb_out_v)
        Simulation(self.dut, dut_v, stim, stim_v).run(quiet=1)

    def testWBMuxAssertedPython(self):
        """Check that rdata is returned when sel Asserted Python"""
        stim = self.asserted(self.wb_out)
        Simulation(self.dut, stim).run(quiet=1)

    def testWBMuxAssertedVerilog(self):
        """Check that rdata is returned when sel Asserted Verilog"""
        dut_v = wb_mux_v(self.sel, self.wb_out_v, self.rdata_in, self.result_in)
        stim = self.asserted(self.wb_out_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testWBMuxAssertedTogether(self):
        """Check that rdata is returned when sel Asserted Together"""
        dut_v = wb_mux_v(self.sel, self.wb_out_v, self.rdata_in, self.result_in)
        stim = self.asserted(self.wb_out)
        stim_v = self.asserted(self.wb_out_v)
        Simulation(self.dut, dut_v, stim, stim_v).run(quiet=1)

    def testWBMuxDynamicPython(self):
        """Check dynamic behavior Python"""
        stim = self.dynamic(self.wb_out)
        Simulation(self.dut, stim).run(quiet=1)

    def testWBMuxDynamicVerilog(self):
        """Check dynamic behavior Verilog"""
        dut_v = wb_mux_v(self.sel, self.wb_out_v, self.rdata_in, self.result_in)
        stim = self.dynamic(self.wb_out_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testWBMuxDynamicTogether(self):
        """Check dynamic behavior Together"""
        dut_v = wb_mux_v(self.sel, self.wb_out_v, self.rdata_in, self.result_in)
        stim = self.dynamic(self.wb_out)
        stim_v = self.dynamic(self.wb_out_v)
        Simulation(self.dut, dut_v, stim, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main(testRunner=unittest.TextTestRunner(verbosity=2))
