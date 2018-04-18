"""Test Sign Extender module"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import Simulation, StopSimulation, Signal, intbv

from src.commons.clock import half_period
from src.commons.signal_generator import signed_signal_set
from src.commons.settings import settings as sf
from src.python.sign_extender import sign_extender, sign_extender_v


class TestSignExtender(TestCase):
    """Testing 16=>32bit sign extension module"""
    def setUp(self):
        self.imm_in = Signal(intbv(min=sf['16_SIGNED_MIN_VALUE'], max=sf['16_SIGNED_MAX_VALUE']))
        self.imm_out, self.imm_out_v = signed_signal_set(2)
        self.dut = sign_extender(imm_in=self.imm_in, imm_out=self.imm_out)

    def deassert(self, python=False, verilog=False):
        """Testing nothing happens with zero input"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            yield half_period()
            if python:
                self.assertEqual(bin(self.imm_out), bin(0x00000000))
            if verilog:
                self.assertEqual(bin(self.imm_out_v), bin(0x00000000))
        raise StopSimulation

    def dynamic(self, python=False, verilog=False):
        """Testing dynamic functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.imm_in.next = Signal(intbv(randint(sf['16_SIGNED_MIN_VALUE'], sf['16_SIGNED_MAX_VALUE']),
                                       min=sf['16_SIGNED_MIN_VALUE'],
                                       max=sf['16_SIGNED_MAX_VALUE']))
            yield half_period()
            if python:
                self.assertEqual(bin(self.imm_in), bin(self.imm_out))
            if verilog:
                self.assertEqual(bin(self.imm_in), bin(self.imm_out_v))
        raise StopSimulation

    def testSignExtenderDeassertPython(self):
        """Testing sign extension deasserted Python"""
        stim = self.deassert(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testSignExtenderDeassertVerilog(self):
        """Testing sign extension deasserted Verilog"""
        stim = self.deassert(verilog=True)
        dut_v = sign_extender_v(imm_in=self.imm_in, imm_out=self.imm_out_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testSignExtenderDeassertTogether(self):
        """Testing sign extension deasserted together"""
        stim = self.deassert(python=True, verilog=True)
        dut_v = sign_extender_v(imm_in=self.imm_in, imm_out=self.imm_out_v)
        Simulation(self.dut, stim, dut_v).run(quiet=1)

    def testSignExtenderDynamicPython(self):
        """testing sign extension dynamically Python"""
        stim = self.dynamic(python=True)
        Simulation(self.dut, stim).run(quiet=1)

    def testSignExtenderDynamicVerilog(self):
        """testing sign extension dynamically Verilog"""
        stim = self.dynamic(verilog=True)
        dut_v = sign_extender_v(imm_in=self.imm_in, imm_out=self.imm_out_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testSignExtenderDynamicTogether(self):
        """testing sign extension dynamically Together"""
        stim = self.dynamic(python=True, verilog=True)
        dut_v = sign_extender_v(imm_in=self.imm_in, imm_out=self.imm_out_v)
        Simulation(self.dut, stim, dut_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
