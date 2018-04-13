"""Data Memory Unit Tests"""
import unittest
from unittest import TestCase
from myhdl import Simulation, StopSimulation, Signal

from src.python.data_mem import data_mem, data_mem_v
from src.commons.settings import settings as sf
from src.commons.clock import clock_gen
from src.commons.signal_generator import unsigned_signal_set, random_unsigned_intbv, \
    random_signed_intbv, unsigned_intbv, signed_signal_set


class TestDataMem(TestCase):
    """test data memory"""
    def setUp(self):
        self.clock, self.read_ctrl, self.write_ctrl = unsigned_signal_set(3, width=1)
        self.mem_addr = Signal(unsigned_intbv(width=sf['MEMORY_WIDTH']))
        self.rdata, self.rdata_v, self.wdata = signed_signal_set(3)
        self.dut = data_mem(clk=self.clock,
                            address=self.mem_addr,
                            write_wire=self.write_ctrl,
                            read_wire=self.read_ctrl,
                            write_data=self.wdata,
                            read_data=self.rdata)

    def getVerilog(self):
        """
        :return: Verilog design under test
        """
        return data_mem_v(clk=self.clock,
                          read_wire=self.read_ctrl,
                          write_wire=self.write_ctrl,
                          address=self.mem_addr,
                          write_data=self.wdata,
                          read_data=self.rdata_v)

    # TODO: Find a way to test read and write separately
    def dynamic(self, python=False, verilog=False):
        """test read/write functionality"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.read_ctrl.next = 0
            self.write_ctrl.next = 1
            expected_data = random_signed_intbv()
            self.mem_addr.next = random_unsigned_intbv(width=sf['MEMORY_WIDTH'])
            self.wdata.next = expected_data
            yield self.clock.posedge
            self.read_ctrl.next = 1
            self.write_ctrl.next = 0
            yield self.clock.posedge
            yield self.clock.negedge

            if python:
                self.assertEqual(bin(expected_data), bin(self.rdata))
            if verilog:
                self.assertEqual(bin(expected_data), bin(self.rdata_v))
        raise StopSimulation

    def testDataMemDynamicPython(self):
        """test data memory reads and writes correctly Python"""
        CLK = clock_gen(self.clock)
        stim = self.dynamic(python=True)
        Simulation(CLK, self.dut, stim).run(quiet=1)

    def testDataMemDynamicVerilog(self):
        """test data memory reads and writes correctly Verilog"""
        CLK = clock_gen(self.clock)
        stim_v = self.dynamic(verilog=True)
        dut_v = self.getVerilog()
        Simulation(CLK, stim_v, dut_v).run(quiet=1)

    def testDataMemDynamicTogether(self):
        """test data memory reads and writes correctly Together"""
        CLK = clock_gen(self.clock)
        stim = self.dynamic(python=True, verilog=True)
        dut_v = self.getVerilog()
        Simulation(CLK, dut_v, self.dut, stim).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
