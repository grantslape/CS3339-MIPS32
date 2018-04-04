import unittest
import sys
from random import randint

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation, ResetSignal, negedge, posedge

sys.path.append("src/python")
from rfile import rfile, rfile_v
from settings import settings as sf
from clock import clock_gen

HALF_PERIOD = delay(sf['PERIOD'] / 2)


def setup():
    clock, reg_write = [Signal(intbv(0)[1:]) for i in range(2)]
    r_addr1, r_addr2, w_addr = [Signal(intbv(0)[5:]) for i in range(3)]
    w_data, r_data1, r_data2 = [Signal(intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE']))
                                for i in range(3)]
    reset = ResetSignal(0, active=sf['ACTIVE_LOW'], async=True)
    return clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2

# TODO: ADD TEST OF RESET FUNCTION


@unittest.skip("Rfile not implemented")
class TestRfileWrite(TestCase):
    # TODO: This test depends on successful reads, and therefore is not completely valid

    reg_1 = intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE'])

    def bench(self, clock, reset, reg_write, r_addr, w_addr, w_data, r_data):
        reset.next = sf['ACTIVE_LOW']
        yield posedge(clock)
        reset.next = sf['INACTIVE_HIGH']
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.reg_1 = intbv(randint(sf['SIGNED_MIN_VALUE'], sf['SIGNED_MAX_VALUE']),
                               min=sf['SIGNED_MIN_VALUE'],
                               max=sf['SIGNED_MAX_VALUE'])
            reg_addr = intbv(randint(0, sf['WIDTH'] - 1))[5:0]
            yield posedge(clock)
            reg_write.next = 1
            w_addr.next = reg_addr
            w_data.next = self.reg_1
            # Unsure about ordering here for sample on neg edge
            r_addr.next = reg_addr
            yield negedge(clock)
            self.assertEqual(r_data, self.reg_1)
        raise StopSimulation

    def testRfileWritePython(self):
        """Test Rfiles writes correctly and reads back Python """
        clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2 = setup()
        CLK = clock_gen(clock)
        stim_1 = self.bench(clock, reset, reg_write, r_addr1, w_addr, w_data, r_data1)
        stim_2 = self.bench(clock, reset, reg_write, r_addr2, w_addr, w_data, r_data2)
        dut = rfile(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2)

        Simulation(CLK, dut, stim_1, stim_2).run(quiet=1)

    def testRfileWriteVerilog(self):
        """Test Rfiles writes correctly and reads back Verilog """
        clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2 = setup()
        CLK = clock_gen(clock)
        stim_1 = self.bench(clock, reset, reg_write, r_addr1, w_addr, w_data, r_data1)
        stim_2 = self.bench(clock, reset, reg_write, r_addr2, w_addr, w_data, r_data2)
        dut = rfile_v(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2)

        Simulation(CLK, dut, stim_1, stim_2).run(quiet=1)

    def testRfileWriteTogether(self):
        """Test Rfiles writes correctly and reads back together """
        clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2 = setup()
        r_data1_v, r_data2_v = [Signal(intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE']))
                                for i in range(2)]
        CLK = clock_gen(clock)
        stim_1 = self.bench(clock, reset, reg_write, r_addr1, w_addr, w_data, r_data1)
        stim_2 = self.bench(clock, reset, reg_write, r_addr2, w_addr, w_data, r_data2)
        stim_1_v = self.bench(clock, reset, reg_write, r_addr1, w_addr, w_data, r_data1_v)
        stim_2_v = self.bench(clock, reset, reg_write, r_addr2, w_addr, w_data, r_data2_v)
        dut = rfile(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2)
        dut_v = rfile_v(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1_v, r_data2_v)

        Simulation(CLK, dut, dut_v, stim_1, stim_2, stim_1_v, stim_2_v).run(quiet=1)


@unittest.skip("Rfile not implemented")
class TestRfileRead(TestCase):
    """Test that Rfile reads correctly"""
    # TODO: This test depends on successful writes, and therefore is not completely valid
    # Dynamic expected read data
    expected = [intbv(randint(sf['SIGNED_MIN_VALUE'],sf['SIGNED_MAX_VALUE']),
                      min=sf['SIGNED_MIN_VALUE'],
                      max=sf['SIGNED_MAX_VALUE'])
                for i in range(sf['WIDTH'])]

    def bench(self, clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2):
        """Stim for Read tests"""
        count = 0
        reset.next = sf['ACTIVE_LOW']
        yield posedge(clock)
        reset.next = sf['INACTIVE_HIGH']
        reg_write.next = 1
        w_addr.next = intbv(0)[5:]
        for v in self.expected:
            w_addr.next = count
            w_data.next = v
            count = count + 1
            yield posedge(clock)
        reg_write.next = 0
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            r_addr1.next = intbv(randint(0, sf['WIDTH'] - 1))
            r_addr2.next = intbv(randint(0, sf['WIDTH'] - 1))
            yield negedge(clock)
            self.assertEqual(r_data1, self.expected[r_addr1])
            self.assertEqual(r_data2, self.expected[r_addr2])
        raise StopSimulation

    def testRfileReadPython(self):
        """Test correct values are read from register Python"""
        clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2 = setup()
        CLK = clock_gen(clock)
        stim = self.bench(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2)
        dut = rfile(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2)

        Simulation(CLK, stim, dut).run(quiet=1)

    def testRfileReadVerilog(self):
        """Test correct values are read from register Verilog"""
        clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2 = setup()
        CLK = clock_gen(clock)
        stim = self.bench(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2)
        dut = rfile_v(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2)

        Simulation(CLK, stim, dut).run(quiet=1)

    def testRfileReadTogether(self):
        """Test correct values are read from register together"""
        clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2 = setup()
        CLK = clock_gen(clock)
        r_data1_v, r_data2_v = [Signal(intbv(0)[5:]) for i in range(2)]
        stim = self.bench(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2)
        stim_v = self.bench(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1_v, r_data2_v)
        dut = rfile(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2)
        dut_v = rfile_v(clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1_v, r_data2_v)

        Simulation(CLK, stim, dut, dut_v, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
