"""Main ALU unit tests"""
import unittest
from unittest import TestCase
from myhdl import Simulation, StopSimulation, intbv, Signal

from src.python.alu import alu, alu_v
from src.commons.settings import settings as sf
from src.commons.clock import half_period
from src.commons.signal_generator import signed_signal_set, unsigned_signal_set, random_signed_intbv, \
    rand_signed_signal_set


@unittest.skip("ALU not implemented")
class TestALU(TestCase):
    """Test main ALU functionality"""

    def setUp(self):
        self.result, self.result_v = signed_signal_set(2)
        self.op_1, self.op_2 = rand_signed_signal_set(2)
        self.alu_op = Signal(intbv()[sf['ALU_CODE_SIZE']:])
        self.z, self.z_v = unsigned_signal_set(2, width=1)
        self.dut = alu(op_1=self.op_1,
                       op_2=self.op_2,
                       alu_op=self.alu_op,
                       z=self.z,
                       result=self.result)

    def getVerilog(self):
        """Return Verilog design under test"""
        return alu_v(op_1=self.op_1,
                     op_2=self.op_2,
                     alu_op=self.alu_op,
                     z=self.z_v,
                     result=self.result_v)

    def check_zero(self, zero_flag, result):
        if result == 0:
            self.assertEqual(1, zero_flag)
        else:
            self.assertEqual(0, zero_flag)

    def add_test(self, python=False, verilog=False):
        """Stim for addition"""
        self.alu_op.next = intbv(0b0001)
        self.op_1.next = self.op_1 // 2
        self.op_2.next = self.op_2 // 2
        result = self.op_1 + self.op_2
        yield half_period()
        if python:
            self.assertEqual(self.result, result)
            self.check_zero(self.z, result)
        if verilog:
            self.assertEqual(self.result_v, result)
            self.check_zero(self.z_v, result)
        raise StopSimulation

    def sub_test(self, python=False, verilog=False):
        """Stim for subtraction"""
        self.alu_op.next = intbv(0b0010)
        self.op_1.next = self.op_1 // 2
        self.op_2.next = self.op_2 // 2
        result = self.op_1 - self.op_2
        yield half_period()
        if python:
            self.assertEqual(result, self.result)
            self.check_zero(self.z, result)
        if verilog:
            self.assertEqual(result, self.result_v)
            self.check_zero(self.z_v, result)
        raise StopSimulation

    def xor_test(self, python=False, verilog=False):
        """Stim for XOR"""
        self.alu_op.next = intbv(0b0011)
        result = self.op_1 ^ self.op_2
        yield half_period()
        if python:
            self.assertEqual(result, self.result)
            self.check_zero(self.z, result)
        if verilog:
            self.assertEqual(result, self.result_v)
            self.check_zero(self.z_v, result)
        raise StopSimulation

    def or_test(self, python=False, verilog=False):
        """Stim for OR"""
        self.alu_op.next = intbv(0b0100)
        result = self.op_1 | self.op_2
        yield half_period()
        if python:
            self.assertEqual(result, self.result)
            self.check_zero(self.z, result)
        if verilog:
            self.assertEqual(result, self.result_v)
            self.check_zero(self.z_v, result)
        raise StopSimulation

    def and_test(self, python=False, verilog=False):
        """Stim for AND"""
        self.alu_op.next = intbv(0b0101)
        result = self.op_1 & self.op_2
        yield half_period()
        if python:
            self.assertEqual(result, self.result)
            self.check_zero(self.z, result)
        if verilog:
            self.assertEqual(result, self.result_v)
            self.check_zero(self.z_v, result)
        raise StopSimulation

    @unittest.skip("SHIFT NOT IMPLEMENTED")
    def shift_left_test(self):
        pass

    @unittest.skip("SHIFT NOT IMPLEMENTED")
    def shift_right_test(self):
        pass

    def nor_test(self, python=False, verilog=False):
        """Stim for NOR"""
        self.alu_op.next = intbv(0b1000)
        result = ~ (self.op_1 | self.op_2)
        yield half_period()
        if python:
            self.assertEqual(result, self.result)
            self.check_zero(self.z, result)
        if verilog:
            self.assertEqual(result, self.result_v)
            self.check_zero(self.z_v, result)
        raise StopSimulation


if __name__ == '__main__':
    unittest.main()
