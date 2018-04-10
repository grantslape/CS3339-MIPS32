"""Data Memory Unit Tests"""
import unittest
from unittest import TestCase
from myhdl import Simulation, StopSimulation, posedge, Signal

from src.python.data_mem import data_mem, data_mem_v
from src.commons.settings import settings as sf
from src.commons.clock import clock_gen
from src.commons.signal_generator import unsigned_signal_set, random_unsigned_intbv, \
    random_signed_intbv, unsigned_intbv, signed_intbv


@unittest.skip("Data memory not implemented")
class TestDataMem(TestCase):
    """test data memory"""
    def setUp(self):
        self.clock, self.read_ctrl, self.w_ctrl = unsigned_signal_set(3, width=1)
        self.mem_addr = Signal(unsigned_intbv())
        self.rdata, self.rdata_v = unsigned_signal_set(2)
        self.wdata = Signal(signed_intbv())
        self.dut = data_mem(clk=self.clock,
                            address=self.read_ctrl,
                            write_wire=self.w_ctrl,
                            read_wire=self.mem_addr,
                            write_data=self.wdata,
                            read_data=self.rdata)

    def getVerilog(self):
        """
        :return: Verilog design under test
        """
        return data_mem_v(clk=self.clock,
                          read_wire=self.read_ctrl,
                          write_wire=self.w_ctrl,
                          address=self.mem_addr,
                          write_data=self.wdata,
                          read_data=self.rdata_v)

    # TODO: Find a way to test read and write separately
    def testDynamic(self, rdata):
        """test read/write functionality"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.read_ctrl.next = 0
            self.w_ctrl.next = 1
            expected_addr = random_unsigned_intbv()
            expected_data = random_signed_intbv()
            self.mem_addr.next = expected_addr
            self.wdata.next = expected_data
            yield posedge(self.clock)
            self.read_ctrl.next = 1
            self.w_ctrl.next = 0
            yield posedge(self.clock)
            self.assertEqual(bin(expected_data), bin(rdata))
        raise StopSimulation

    def testDataMemDynamicPython(self):
        """test data memory reads and writes correctly Python"""
        CLK = clock_gen(self.clock)
        stim = self.testDynamic(self.rdata)
        Simulation(CLK, self.dut, stim).run(quiet=1)

    def testDataMemDynamicVerilog(self):
        """test data memory reads and writes correctly Verilog"""
        CLK = clock_gen(self.clock)
        stim_v = self.testDynamic(self.rdata_v)
        dut_v = self.getVerilog()
        Simulation(CLK, stim_v, dut_v).run(quiet=1)

    def testDataMemDynamicTogether(self):
        """test data memory reads and writes correctly Verilog"""
        CLK = clock_gen(self.clock)
        stim = self.testDynamic(self.rdata)
        stim_v = self.testDynamic(self.rdata_v)
        dut_v = self.getVerilog()
        Simulation(CLK, stim_v, dut_v, self.dut, stim).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
