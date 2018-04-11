"""Unit tests for Register file"""
import unittest
from unittest import TestCase
from myhdl import Simulation, StopSimulation, ResetSignal, negedge, posedge

from src.python.rfile import rfile, rfile_v
from src.commons.settings import settings as sf
from src.commons.clock import clock_gen
from src.commons.signal_generator import random_signed_intbv, unsigned_signal_set, \
    signed_signal_set, random_unsigned_intbv, unsigned_intbv


# TODO: ADD TEST OF RESET FUNCTION
# TODO: use signal_generator functions
@unittest.skip("Rfile not implemented")
class TestRfile(TestCase):
    """Test Register File"""
    # These tests are interdependent and therefore not completely valid
    # They should be fixed at some point
    def setUp(self):
        self.clock, self.reg_write = unsigned_signal_set(2, width=1)
        self.r_addr1, self.r_addr2, self.w_addr, self.reg_addr = unsigned_signal_set(4, width=5)
        self.w_data, self.r_data1, self.r_data2, self.r_data1_v, self.r_data2_v \
            = signed_signal_set(5)
        self.reset = ResetSignal(0, active=sf['ACTIVE_LOW'], async=True)
        self.reg_1 = random_signed_intbv()
        self.expected = []
        for i in range(sf['WIDTH']):
            self.expected.append(random_signed_intbv())
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

    def write_test(self, r_data):
        """Stim for read tests"""
        self.reset.next = sf['ACTIVE_LOW']
        yield posedge(self.clock)
        self.reset.next = sf['INACTIVE_HIGH']
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.reg_1 = random_signed_intbv()
            self.reg_addr = random_unsigned_intbv(width=5)
            yield posedge(self.clock)
            self.reg_write.next = 1
            self.w_addr.next = self.reg_addr
            self.w_data.next = self.reg_1
            # Unsure about ordering here for sample on neg edge
            self.r_addr1.next = self.reg_addr
            yield negedge(self.clock)
            self.assertEqual(bin(r_data), bin(self.reg_1))
        raise StopSimulation

    def read_test(self, r_data1, r_data2):
        """Stim for Read tests"""
        count = 0
        self.reset.next = sf['ACTIVE_LOW']
        yield posedge(self.clock)
        self.reset.next = sf['INACTIVE_HIGH']
        self.reg_write.next = 1
        self.w_addr.next = unsigned_intbv(width=5)
        for value in self.expected:
            self.w_addr.next = count
            self.w_data.next = value
            count = count + 1
            yield posedge(self.clock)
            self.reg_write.next = 0
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.r_addr1.next = random_unsigned_intbv(width=5)
            self.r_addr2.next = random_unsigned_intbv(width=5)
            yield negedge(self.clock)
            self.assertEqual(bin(r_data1), bin(self.expected[self.r_addr1]))
            self.assertEqual(bin(r_data2), bin(self.expected[self.r_addr2]))
        raise StopSimulation

    def testRfileWritePython(self):
        """Test Rfiles writes correctly and reads back Python """
        CLK = clock_gen(self.clock)
        stim_1 = self.write_test(self.r_data1)
        Simulation(CLK, self.dut, stim_1).run(quiet=1)

    def testRfileWriteVerilog(self):
        """Test Rfiles writes correctly and reads back Verilog """
        CLK = clock_gen(self.clock)
        stim_1 = self.write_test(self.r_data1_v)
        dut_v = self.getVerilog()
        Simulation(CLK, dut_v, stim_1).run(quiet=1)

    def testRfileWriteTogether(self):
        """Test Rfiles writes correctly and reads back together """
        CLK = clock_gen(self.clock)
        stim_1 = self.write_test(self.r_data1)
        stim_v = self.write_test(self.r_data1_v)
        dut_v = self.getVerilog()
        Simulation(CLK, self.dut, dut_v, stim_1, stim_v).run(quiet=1)

    def testRfileReadPython(self):
        """Test correct values are read from register Python"""
        CLK = clock_gen(self.clock)
        stim = self.read_test(self.r_data1, self.r_data2)
        Simulation(CLK, stim, self.dut).run(quiet=1)

    def testRfileReadVerilog(self):
        """Test correct values are read from register Verilog"""
        CLK = clock_gen(self.clock)
        stim = self.read_test(self.r_data1_v, self.r_data2_v)
        dut_v = self.getVerilog()
        Simulation(CLK, stim, dut_v).run(quiet=1)

    def testRfileReadTogether(self):
        """Test correct values are read from register together"""
        CLK = clock_gen(self.clock)
        stim = self.read_test(self.r_data1, self.r_data2)
        stim_v = self.read_test(self.r_data1_v, self.r_data2_v)
        dut_v = self.getVerilog()
        Simulation(CLK, stim, self.dut, dut_v, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
