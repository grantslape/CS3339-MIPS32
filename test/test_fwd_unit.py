import unittest
from unittest import TestCase
from myhdl import intbv, Simulation, Signal, StopSimulation
from src.python.fwd_unit import fwd_unit, fwd_unit_v
from src.commons.settings import settings as sf
from src.commons.clock import half_period


# TODO: Dynamically test this module over many iterations
class TestFwdUnitHoldValue(TestCase):
    """Test Fwd Unit"""
    def setUp(self):
        self.rt_in, self.rs_in, self.ex_rd, self.mem_rd = [Signal(intbv(0)[5:]) for i in range(4)]
        self.mem_reg_write, self.wb_reg_write = [Signal(intbv(0)[1:]) for i in range(2)]
        self.forward_a, self.forward_b, self.forward_a_v, self.forward_b_v = [
            Signal(intbv(0)[2:]) for i in range(4)
        ]
        self.dut = fwd_unit(self.rt_in,
                            self.rs_in,
                            self.ex_rd,
                            self.mem_rd,
                            self.mem_reg_write,
                            self.wb_reg_write,
                            self.forward_a,
                            self.forward_b)

    def hold_value(self, forward_a, forward_b):
        """test fwd unit holds value"""
        for i in range(sf['DEFAULT_TEST_LENGTH']):
            self.assertEqual(forward_a, 0)
            self.assertEqual(forward_b, 0)
            self.assertEqual(self.mem_reg_write, 0)
            self.assertEqual(self.wb_reg_write, 0)
            self.assertEqual(self.rt_in, 0)
            self.assertEqual(self.rs_in, 0)
            self.assertEqual(self.ex_rd, 0)
            self.assertEqual(self.mem_rd, 0)
            yield half_period()

    def no_forward_test(self, forward_a, forward_b):
        """Stim for no forwarding"""
        self.rt_in.next = 10
        self.rs_in.next = 11
        yield half_period()
        self.assertEqual(forward_b, 0)
        self.assertEqual(forward_a, 0)
        raise StopSimulation

    # TODO: Break this out into individual test cases
    def forward_a_test(self, forward_a, forward_b):
        """Stim for forward A cases.  See p310 of book"""
        self.rs_in.next = 11
        self.ex_rd.next = 11
        self.rt_in.next = 10
        self.mem_reg_write.next = 1
        self.wb_reg_write.next = 0
        yield half_period()
        self.assertEqual(forward_b, 0)
        self.assertEqual(bin(forward_a), bin(2))
        self.ex_rd.next = 12
        self.mem_rd.next = 11
        self.wb_reg_write.next = 1
        yield half_period()
        self.assertEqual(forward_b, 0)
        self.assertEqual(bin(forward_a), bin(1))
        self.mem_reg_write.next = 0
        self.wb_reg_write.next = 0
        yield half_period()
        self.assertEqual(forward_b, 0)
        self.assertEqual(forward_a, 0)
        self.rs_in.next = 11
        self.ex_rd.next = 11
        self.mem_rd.next = 11
        self.mem_reg_write.next = 1
        self.wb_reg_write.next = 0
        yield half_period()
        self.assertEqual(forward_b, 0)
        self.assertEqual(bin(forward_a), bin(2))

    # TODO: Break this out into individual test cases
    def forward_b_test(self, forward_a, forward_b):
        """Stim for forward A cases.  See p310 of book"""
        self.rt_in.next = 11
        self.ex_rd.next = 11
        self.rs_in.next = 13
        self.mem_reg_write.next = 1
        self.wb_reg_write.next = 0
        yield half_period()
        self.assertEqual(bin(forward_a), bin(0))
        self.assertEqual(bin(forward_b), bin(2))
        self.ex_rd.next = 12
        self.mem_rd.next = 11
        self.wb_reg_write.next = 1
        yield half_period()
        self.assertEqual(forward_a, 0)
        self.assertEqual(bin(forward_b), bin(1))
        self.mem_reg_write.next = 0
        self.wb_reg_write.next = 0
        yield half_period()
        self.assertEqual(forward_b, 0)
        self.assertEqual(forward_a, 0)
        self.rt_in.next = 11
        self.ex_rd.next = 11
        self.mem_rd.next = 11
        self.mem_reg_write.next = 1
        self.wb_reg_write.next = 0
        yield half_period()
        self.assertEqual(forward_a, 0)
        self.assertEqual(bin(forward_b), bin(2))

    def testHoldValuePython(self):
        """ Checking that module holds value when no input changes from Python """
        stim = self.hold_value(self.forward_a, self.forward_b)
        Simulation(self.dut, stim).run(quiet=1)

    def testHoldValueVerilog(self):
        """ Checking that module holds value when no input changes from Verilog """
        stim = self.hold_value(self.forward_a_v, self.forward_b_v)
        dut_v = fwd_unit_v(self.rt_in,
                           self.rs_in,
                           self.ex_rd,
                           self.mem_rd,
                           self.mem_reg_write,
                           self.wb_reg_write,
                           self.forward_a_v,
                           self.forward_b_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testHoldValueTogether(self):
        """ Checking that module holds value when no input changes from Cosimulation """
        stim = self.hold_value(self.forward_a, self.forward_b)
        stim_v = self.hold_value(self.forward_a_v, self.forward_b_v)
        dut_v = fwd_unit_v(self.rt_in,
                           self.rs_in,
                           self.ex_rd,
                           self.mem_rd,
                           self.mem_reg_write,
                           self.wb_reg_write,
                           self.forward_a_v,
                           self.forward_b_v)
        Simulation(self.dut, dut_v, stim, stim_v).run(quiet=1)

    def testNoForwardPython(self):
        """Test no forwarding Python"""
        stim = self.no_forward_test(self.forward_a, self.forward_b)
        Simulation(self.dut, stim).run(quiet=1)

    def testNoForwardVerilog(self):
        """Test no forwarding Verilog"""
        stim = self.no_forward_test(self.forward_a_v, self.forward_b_v)
        dut_v = fwd_unit_v(self.rt_in,
                           self.rs_in,
                           self.ex_rd,
                           self.mem_rd,
                           self.mem_reg_write,
                           self.wb_reg_write,
                           self.forward_a_v,
                           self.forward_b_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testNoForwardTogether(self):
        """Test no forwarding Verilog"""
        stim = self.no_forward_test(self.forward_a, self.forward_b)
        stim_v = self.no_forward_test(self.forward_a_v, self.forward_b_v)
        dut_v = fwd_unit_v(self.rt_in,
                           self.rs_in,
                           self.ex_rd,
                           self.mem_rd,
                           self.mem_reg_write,
                           self.wb_reg_write,
                           self.forward_a_v,
                           self.forward_b_v)
        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def testForwardACasesPython(self):
        """Test Forward A cases Python"""
        stim = self.forward_a_test(self.forward_a, self.forward_b)
        Simulation(self.dut, stim).run(quiet=1)

    def testForwardACasesVerilog(self):
        """Test Forward A cases Verilog"""
        stim_v = self.forward_a_test(self.forward_a_v, self.forward_b_v)
        dut_v = fwd_unit_v(self.rt_in,
                           self.rs_in,
                           self.ex_rd,
                           self.mem_rd,
                           self.mem_reg_write,
                           self.wb_reg_write,
                           self.forward_a_v,
                           self.forward_b_v)
        Simulation(dut_v, stim_v).run(quiet=1)

    def testForwardACasesTogether(self):
        """Test Forward A cases together"""
        stim = self.forward_a_test(self.forward_a, self.forward_b)
        stim_v = self.forward_a_test(self.forward_a_v, self.forward_b_v)
        dut_v = fwd_unit_v(self.rt_in,
                           self.rs_in,
                           self.ex_rd,
                           self.mem_rd,
                           self.mem_reg_write,
                           self.wb_reg_write,
                           self.forward_a_v,
                           self.forward_b_v)
        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)

    def testForwardBCasesPython(self):
        """Test Forward B cases Python"""
        stim = self.forward_b_test(self.forward_a, self.forward_b)
        Simulation(self.dut, stim).run(quiet=1)

    def testForwardBCasesVerilog(self):
        """Test Forward B cases Verilog"""
        stim = self.forward_b_test(self.forward_a_v, self.forward_b_v)
        dut_v = fwd_unit_v(self.rt_in,
                           self.rs_in,
                           self.ex_rd,
                           self.mem_rd,
                           self.mem_reg_write,
                           self.wb_reg_write,
                           self.forward_a_v,
                           self.forward_b_v)
        Simulation(dut_v, stim).run(quiet=1)

    def testForwardBCasesTogether(self):
        """Test Forward A cases together"""
        stim = self.forward_b_test(self.forward_a, self.forward_b)
        stim_v = self.forward_b_test(self.forward_a_v, self.forward_b_v)
        dut_v = fwd_unit_v(self.rt_in,
                           self.rs_in,
                           self.ex_rd,
                           self.mem_rd,
                           self.mem_reg_write,
                           self.wb_reg_write,
                           self.forward_a_v,
                           self.forward_b_v)
        Simulation(self.dut, stim, dut_v, stim_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
