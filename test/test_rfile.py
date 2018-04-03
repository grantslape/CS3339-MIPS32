import unittest
import sys
from random import randint

from unittest import TestCase
from myhdl import intbv, delay, Simulation, Signal, StopSimulation, ResetSignal, negedge, posedge

sys.path.append("src/python")
from rfile import rfile, rfile_v
from settings import settings as sf

HALF_PERIOD = delay(sf['PERIOD'] / 2)


def clock_gen(clock):
    while 1:
        yield HALF_PERIOD
        clock.next = not clock


def setup():
    clock, reg_write = [Signal(intbv(0)[1:]) for i in range(2)]
    r_addr1, r_addr2, w_addr = [Signal(intbv(0)[5:]) for i in range(3)]
    w_data, r_data1, r_data2 = [Signal(intbv(0, min=sf['SIGNED_MIN_VALUE'], max=sf['SIGNED_MAX_VALUE']))
                                for i in range(3)]
    reset = ResetSignal(0, active=sf['ACTIVE_LOW'], async=True)
    return clock, reset, reg_write, r_addr1, r_addr2, w_addr, w_data, r_data1, r_data2


class TestRfileRead(TestCase):

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

        sim = Simulation(CLK, stim, dut)
        sim.run(quiet=1)


if __name__ == '__main__':
    unittest.main()
