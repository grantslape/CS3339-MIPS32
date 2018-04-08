"""Unit tests for Register file"""
import unittest
from unittest import TestCase
from random import randint
from myhdl import intbv, Simulation, Signal, StopSimulation, ResetSignal, negedge, posedge

from src.python.rfile import rfile, rfile_v
from src.commons.settings import settings as sf
from src.commons.clock import clock_gen
from src.commons.signal_generator import signed_intbv_set, random_signed_intbv


# TODO: ADD TEST OF RESET FUNCTION
# TODO: use signal_generator functions
@unittest.skip("Rfile not implemented")
class TestRfile(TestCase):
    """Test Register File"""
    # TODO: These tests are interdependent and not completely valid
    def setUp(self):
        self.clock, self.reg_write = [Signal(intbv()[1:]) for i in range(2)]
        self.r_addr1, self.r_addr2, self.w_addr, self.reg_addr = [
            Signal(intbv()[5:]) for i in range(4)
        ]
        self.w_data, self.r_data1, self.r_data2, self.r_data1_v, self.r_data2_v \
            = signed_intbv_set(5)
        self.reset = ResetSignal(0, active=sf['ACTIVE_LOW'], async=True)
        self.reg_1 = random_signed_intbv()
        self.expected = []
        for i in range(sf['WIDTH']):
            self.expected.append(intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE'])))
        self.dut = rfile(self.clock,
                         self.reset,
                         self.reg_write,
                         self.r_addr1,
                         self.r_addr2,
                         self.w_addr,
                         self.w_data,
                         self.r_data1,
                         self.r_data2)

    def write_test(self, r_data):
        """Stim for read tests"""
        self.reset.next = sf['ACTIVE_LOW']
        yield posedge(self.clock)
        self.reset.next = sf['INACTIVE_HIGH']
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.reg_1 = random_signed_intbv()
            self.reg_addr = intbv(randint(0, sf['WIDTH'] - 1))[5:0]
            yield posedge(self.clock)
            self.reg_write.next = 1
            self.w_addr.next = self.reg_addr
            self.w_data.next = self.reg_1
            # Unsure about ordering here for sample on neg edge
            self.r_addr1.next = self.reg_addr
            yield negedge(self.clock)
            self.assertEqual(r_data, self.reg_1)
        raise StopSimulation

    def read_test(self, r_data1, r_data2):
        """Stim for Read tests"""
        count = 0
        self.reset.next = sf['ACTIVE_LOW']
        yield posedge(self.clock)
        self.reset.next = sf['INACTIVE_HIGH']
        self.reg_write.next = 1
        self.w_addr.next = intbv(0)[5:]
        for value in self.expected:
            self.w_addr.next = count
            self.w_data.next = value
            count = count + 1
            yield posedge(self.clock)
            self.reg_write.next = 0
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.r_addr1.next = intbv(randint(0, sf['WIDTH'] - 1))
            self.r_addr2.next = intbv(randint(0, sf['WIDTH'] - 1))
            yield negedge(self.clock)
            self.assertEqual(r_data1, self.expected[self.r_addr1])
            self.assertEqual(r_data2, self.expected[self.r_addr2])
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
        dut_v = rfile_v(self.clock,
                        self.reset,
                        self.reg_write,
                        self.r_addr1,
                        self.r_addr2,
                        self.w_addr,
                        self.w_data,
                        self.r_data1_v,
                        self.r_data2_v)
        Simulation(CLK, dut_v, stim_1).run(quiet=1)

    def testRfileWriteTogether(self):
        """Test Rfiles writes correctly and reads back together """
        CLK = clock_gen(self.clock)
        stim_1 = self.write_test(self.r_data1)
        stim_v = self.write_test(self.r_data1_v)
        dut_v = rfile_v(self.clock,
                        self.reset,
                        self.reg_write,
                        self.r_addr1,
                        self.r_addr2,
                        self.w_addr,
                        self.w_data,
                        self.r_data1_v,
                        self.r_data2_v)
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
        dut_v = rfile_v(self.clock,
                        self.reset,
                        self.reg_write,
                        self.r_addr1,
                        self.r_addr2,
                        self.w_addr,
                        self.w_data,
                        self.r_data1_v,
                        self.r_data2_v)
        Simulation(CLK, stim, dut_v).run(quiet=1)

    def testRfileReadTogether(self):
        """Test correct values are read from register together"""
        CLK = clock_gen(self.clock)
        stim = self.read_test(self.r_data1, self.r_data2)
        stim_v = self.read_test(self.r_data1_v, self.r_data2_v)
        dut_v = rfile_v(self.clock,
                        self.reset,
                        self.reg_write,
                        self.r_addr1,
                        self.r_addr2,
                        self.w_addr,
                        self.w_data,
                        self.r_data1_v,
                        self.r_data2_v)
        Simulation(CLK, stim, self.dut, dut_v, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()