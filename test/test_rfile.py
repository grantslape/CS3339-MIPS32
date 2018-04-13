"""Unit tests for Register file"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import Simulation, StopSimulation, ResetSignal, negedge, posedge, Signal, intbv

from src.python.rfile import rfile, rfile_v
from src.commons.settings import settings as sf
from src.commons.clock import clock_gen
from src.commons.signal_generator import random_signed_intbv, unsigned_signal_set, \
    signed_signal_set, random_unsigned_intbv, unsigned_intbv, signed_intbv


class TestRfile(TestCase):
    """Test Register File"""
    # These tests are interdependent and therefore not completely valid
    # They should be fixed at some point
    def setUp(self):
        self.clock, self.reg_write = unsigned_signal_set(2, width=1)
        self.r_addr1, self.r_addr2, self.w_addr, self.reg_addr = unsigned_signal_set(4, width=5)
        self.w_data, self.r_data1, self.r_data2, self.r_data1_v, self.r_data2_v \
            = signed_signal_set(5)
        self.reset = ResetSignal(sf['INACTIVE_HIGH'], active=sf['ACTIVE_LOW'], async=True)

        self.dut = rfile(self.clock,
                         self.reset,
                         self.reg_write,
                         self.r_addr1,
                         self.r_addr2,
                         self.w_addr,
                         self.w_data,
                         self.r_data1,
                         self.r_data2)

    def getVerilog(self):
        """return verilog module under test"""
        return rfile_v(self.clock,
                       self.reset,
                       self.reg_write,
                       self.r_addr1,
                       self.r_addr2,
                       self.w_addr,
                       self.w_data,
                       self.r_data1_v,
                       self.r_data2_v)

    def write_test(self, python=False, verilog=False):
        """Stim for testing write and single-register read tests"""
        register = randint(0, 31)
        value = random_signed_intbv()
        prev_reg = register
        prev_data = value
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.w_data.next = value
            self.w_addr.next = register
            self.reg_write.next = 1
            self.r_addr1.next = register
            self.r_addr2.next = prev_reg
            yield self.clock.negedge
            self.reg_write.next = 0
            yield self.clock.posedge
            if python:
                print "python: register: {}, prev_reg: {}".format(register, prev_reg)
                self.assertEqual(self.r_data1, value)
                self.assertEqual(self.r_data2, prev_data)
            if verilog:
                self.assertEqual(self.r_data1_v, value)
                self.assertEqual(self.r_data2_v, prev_data)
            prev_reg = register
            prev_data = value
            while register == prev_reg:
                register = randint(0, 31)
            while value == prev_data:
                value = random_signed_intbv()
        raise StopSimulation

    def reset_test(self, python=False, verilog=False):
        """Stim for testing reset"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            value = random_signed_intbv()
            register = randint(0, 31)
            self.reset.next = Signal(signed_intbv(0))  # activate reset
            self.w_data.next = value
            self.w_addr.next = register
            self.reg_write.next = 1
            self.r_addr1.next = register
            yield self.clock.negedge
            self.reg_write.next = 0
            self.reset.next = Signal(signed_intbv(1))  # deactivate reset
            yield self.clock.posedge
            if python:
                self.assertEqual(self.r_data1, intbv(0))
                self.assertEqual(self.r_data2, intbv(0))
            if verilog:
                self.assertEqual(self.r_data1_v, intbv(0))
                self.assertEqual(self.r_data2_v, intbv(0))
        raise StopSimulation

    def simultaneous_read_test(self, python=False, verilog=False):
        """Stim to test simultaneously reading both registers """
        count = 0
        expected = [random_signed_intbv() for i in range(sf['WIDTH'])]
        self.reg_write.next = 1
        self.w_addr.next = unsigned_intbv(width=5)
        for value in expected:
            self.w_addr.next = count
            self.w_data.next = value
            count = count + 1
            yield self.clock.negedge
            self.reg_write.next = 0
            yield self.clock.posedge
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.r_addr1.next = random_unsigned_intbv(width=5)
            self.r_addr2.next = random_unsigned_intbv(width=5)
            yield self.clock.negedge
            if python:
                self.assertEqual(bin(self.r_data1), bin(expected[self.r_addr1]))
                self.assertEqual(bin(self.r_data2), bin(expected[self.r_addr2]))
            if verilog:
                self.assertEqual(bin(self.r_data1_v), bin(expected[self.r_addr1]))
                self.assertEqual(bin(self.r_data2_v), bin(expected[self.r_addr2]))
        raise StopSimulation

    def testRfileWritePython(self):
        """Test rfile writes correctly and reads back Python """
        CLK = clock_gen(self.clock)
        stim_1 = self.write_test(python=True)
        Simulation(CLK, self.dut, stim_1).run(quiet=1)
        print ""

    def testRfileWriteVerilog(self):
        """Test rfile writes correctly and reads back Verilog """
        CLK = clock_gen(self.clock)
        stim_1 = self.write_test(verilog=True)
        dut_v = self.getVerilog()
        Simulation(CLK, dut_v, stim_1).run(quiet=1)

    def estRfileWriteTogether(self):
        """Test rfile writes correctly and reads back together """
        CLK = clock_gen(self.clock)
        stim_1 = self.write_test(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(CLK, self.dut, dut_v, stim_1).run(quiet=1)

    def testResetPython(self):
        """Test Reset works as expected Python """
        CLK = clock_gen(self.clock)
        stim_1 = self.reset_test(python=True)
        Simulation(CLK, self.dut, stim_1).run(quiet=1)

    def testResetVerilog(self):
        """Test Reset works as expected Verilog """
        CLK = clock_gen(self.clock)
        stim_1 = self.reset_test(verilog=True)
        dut_v = self.getVerilog()
        Simulation(CLK, dut_v, stim_1).run(quiet=1)

    def testResetTogether(self):
        """Test Reset works as expected Together """
        CLK = clock_gen(self.clock)
        stim_1 = self.reset_test(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(CLK, self.dut, dut_v, stim_1).run(quiet=1)

    def estSimultaneousReadPython(self):
        """Test correct values are read from register Python"""
        CLK = clock_gen(self.clock)
        stim = self.simultaneous_read_test(python=True)
        Simulation(CLK, stim, self.dut).run(quiet=1)

    def estSimultaneousReadVerilog(self):
        """Test correct values are read from register Verilog"""
        CLK = clock_gen(self.clock)
        stim = self.read_test(verilog=True)
        dut_v = self.getVerilog()
        Simulation(CLK, stim, dut_v).run(quiet=1)

    def estSimultaneousReadTogether(self):
        """Test correct values are read from register together"""
        CLK = clock_gen(self.clock)
        stim = self.read_test(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(CLK, stim, self.dut, dut_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
