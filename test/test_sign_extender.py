"""Test Sign Extender module"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import Simulation, StopSimulation, Signal, intbv

from src.commons.clock import half_period
from src.commons.signal_generator import signed_signal_set
from src.commons.settings import settings as sf
from src.python.sign_extender import sign_extender, sign_extender_v


@unittest.skip("Sign Extender not implemented")
class TestSignExtender(TestCase):
    """Testing 16=>32bit sign extension module"""
    def setUp(self):
        self.imm_in = Signal(intbv(0, min=sf['16_SIGNED_MIN_VALUE'], max=sf['16_SIGNED_MAX_VALUE']))
        self.imm_out, self.imm_out_v = signed_signal_set(2)
        self.dut = sign_extender(imm_in=self.imm_in, imm_out=self.imm_out)

    def deassert(self, imm_out):
        """Testing nothing happens with zero input"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.assertEqual(bin(imm_out), bin(0x00000000))
        raise StopSimulation

    def dynamic(self, imm_out):
        """Testing dynamic functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.imm_in = Signal(intbv(randint(sf['16_SIGNED_MIN_VALUE'], sf['16_SIGNED_MAX_VALUE']),
                                       min=sf['16_SIGNED_MIN_VALUE'],
                                       max=sf['16_SIGNED_MAX_VALUE']))
            yield half_period()
            self.assertEqual(bin(self.imm_in), bin(imm_out))
        raise StopSimulation

    def testSignExtenderDeassertPython(self):
        """Testing sign extension deasserted Python"""
        stim = self.deassert(self.imm_out)
        Simulation(self.dut, stim).run(quiet=1)

    def testSignExtenderDeassertVerilog(self):
        """Testing sign extension deasserted Verilog"""
        stim = self.deassert(self.imm_out_v)
        dut_v = sign_extender_v(imm_in=self.imm_in, imm_out=self.imm_out_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testSignExtenderDeassertTogether(self):
        """Testing sign extension deasserted together"""
        stim = self.deassert(self.imm_out)
        stim_v = self.deassert(self.imm_out_v)
        dut_v = sign_extender_v(imm_in=self.imm_in, imm_out=self.imm_out_v)
        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def testSignExtenderDynamicPython(self):
        """testing sign extension dynamically Python"""
        stim = self.dynamic(self.imm_out)
        Simulation(self.dut, stim).run(quiet=1)

    def testSignExtenderDynamicVerilog(self):
        """testing sign extension dynamically Verilog"""
        stim = self.dynamic(self.imm_out_v)
        dut_v = sign_extender_v(imm_in=self.imm_in, imm_out=self.imm_out_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testSignExtenderDynamicTogether(self):
        """testing sign extension dynamically Together"""
        stim = self.dynamic(self.imm_out)
        stim_v = self.dynamic(self.imm_out_v)
        dut_v = sign_extender_v(imm_in=self.imm_in, imm_out=self.imm_out_v)
        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
