"""Main ALU unit tests"""
import unittest
from random import randint
from unittest import TestCase
from myhdl import Simulation, StopSimulation, intbv, Signal, bin

from src.python.alu import alu, alu_v
from src.commons.settings import settings as sf
from src.commons.clock import half_period
from src.commons.signal_generator import signed_signal_set, unsigned_signal_set, \
    rand_signed_signal_set, signed_intbv


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
        """Check if zero flag is set"""
        if result == 0:
            self.assertEqual(1, zero_flag)
        else:
            self.assertEqual(0, zero_flag)

    def add_test(self, python=False, verilog=False):
        """Stim for addition"""
        self.alu_op.next = intbv(0b0001)
        first = signed_intbv(randint(sf['16_SIGNED_MIN_VALUE'], sf['16_SIGNED_MAX_VALUE']))
        second = signed_intbv(randint(sf['16_SIGNED_MIN_VALUE'], sf['16_SIGNED_MAX_VALUE']))
        result = first + second
        self.op_1.next = first
        self.op_2.next = second
        yield half_period()
        if python:
            self.assertEqual(bin(self.result), bin(result))
            self.check_zero(self.z, result)
        if verilog:
            self.assertEqual(bin(self.result_v), bin(result))
            self.check_zero(self.z_v, result)
        raise StopSimulation

    def sub_test(self, python=False, verilog=False):
        """Stim for subtraction"""
        self.alu_op.next = intbv(0b0010)
        first = signed_intbv(randint(sf['16_SIGNED_MIN_VALUE'], sf['16_SIGNED_MAX_VALUE']))
        second = signed_intbv(randint(sf['16_SIGNED_MIN_VALUE'], sf['16_SIGNED_MAX_VALUE']))
        result = first - second
        self.op_1.next = first
        self.op_2.next = second
        yield half_period()
        if python:
            self.assertEqual(bin(result), bin(self.result))
            self.check_zero(self.z, result)
        if verilog:
            self.assertEqual(bin(result), bin(self.result_v))
            self.check_zero(self.z_v, result)
        raise StopSimulation

    def xor_test(self, python=False, verilog=False):
        """Stim for XOR"""
        self.alu_op.next = intbv(0b0011)
        result = self.op_1 ^ self.op_2
        yield half_period()
        if python:
            self.assertEqual(bin(result), bin(self.result))
            self.check_zero(self.z, result)
        if verilog:
            self.assertEqual(bin(result), bin(self.result_v))
            self.check_zero(self.z_v, result)
        raise StopSimulation

    def or_test(self, python=False, verilog=False):
        """Stim for OR"""
        self.alu_op.next = intbv(0b0100)
        result = self.op_1 | self.op_2
        yield half_period()
        if python:
            self.assertEqual(bin(result), bin(self.result))
            self.check_zero(self.z, result)
        if verilog:
            self.assertEqual(bin(result), bin(self.result_v))
            self.check_zero(self.z_v, result)
        raise StopSimulation

    def and_test(self, python=False, verilog=False):
        """Stim for AND"""
        self.alu_op.next = intbv(0b0101)
        result = self.op_1 & self.op_2
        yield half_period()
        if python:
            self.assertEqual(bin(result), bin(self.result))
            self.check_zero(self.z, result)
        if verilog:
            self.assertEqual(bin(result), bin(self.result_v))
            self.check_zero(self.z_v, result)
        raise StopSimulation

    @unittest.skip("SHIFT NOT IMPLEMENTED")
    def shift_left_test(self):
        """stim for SLL"""
        pass

    @unittest.skip("SHIFT NOT IMPLEMENTED")
    def shift_right_test(self):
        """stim for SRL"""
        pass

    def nor_test(self, python=False, verilog=False):
        """Stim for NOR"""
        self.alu_op.next = intbv(0b1000)
        result = ~ (self.op_1 | self.op_2)
        yield half_period()
        if python:
            self.assertEqual(bin(result), bin(self.result))
            self.check_zero(self.z, result)
        if verilog:
            self.assertEqual(bin(result), bin(self.result_v))
            self.check_zero(self.z_v, result)
        raise StopSimulation

    def slt_test(self, python=False, verilog=False):
        """Stim for SLT"""
        for _ in range(sf['DEFAULT_TEST_LENGTH']):
            self.alu_op.next = intbv(0b1001)
            result = 1 if self.op_1 < self.op_2 else 0
            yield half_period()
            if python:
                self.assertEqual(bin(result), bin(self.result))
            if verilog:
                self.assertEqual(bin(result), bin(self.result_v))
        raise StopSimulation

    def testAddOpPython(self):
        """Test Add operations Python"""
        stim = self.add_test(python=True)
        Simulation(stim, self.dut).run(quiet=1)

    def testAddOpVerilog(self):
        """test Add operations Verilog"""
        stim = self.add_test(verilog=True)
        dut_v = self.getVerilog()
        Simulation(stim, dut_v).run(quiet=1)

    def testAddOpTogether(self):
        """test add operations Together"""
        stim = self.add_test(verilog=True, python=True)
        dut_v = self.getVerilog()
        Simulation(stim, self.dut, dut_v).run(quiet=1)

    def testSubOpPython(self):
        """Test Sub operations Python"""
        stim = self.sub_test(python=True)
        Simulation(stim, self.dut).run(quiet=1)

    def testSubOpVerilog(self):
        """test Sub operations Verilog"""
        stim = self.sub_test(verilog=True)
        dut_v = self.getVerilog()
        Simulation(stim, dut_v).run(quiet=1)

    def testSubOpTogether(self):
        """test Sub operations Together"""
        stim = self.sub_test(verilog=True, python=True)
        dut_v = self.getVerilog()
        Simulation(stim, self.dut, dut_v).run(quiet=1)

    def testXorOpPython(self):
        """Test Xor operations Python"""
        stim = self.xor_test(python=True)
        Simulation(stim, self.dut).run(quiet=1)

    def testXorOpVerilog(self):
        """test Xor operations Verilog"""
        stim = self.xor_test(verilog=True)
        dut_v = self.getVerilog()
        Simulation(stim, dut_v).run(quiet=1)

    def testXorOpTogether(self):
        """test Xor operations Together"""
        stim = self.xor_test(verilog=True, python=True)
        dut_v = self.getVerilog()
        Simulation(stim, self.dut, dut_v).run(quiet=1)

    def testOrOpPython(self):
        """Test Or operations Python"""
        stim = self.or_test(python=True)
        Simulation(stim, self.dut).run(quiet=1)

    def testOrOpVerilog(self):
        """test Or operations Verilog"""
        stim = self.or_test(verilog=True)
        dut_v = self.getVerilog()
        Simulation(stim, dut_v).run(quiet=1)

    def testOrOpTogether(self):
        """test Or operations Together"""
        stim = self.or_test(verilog=True, python=True)
        dut_v = self.getVerilog()
        Simulation(stim, self.dut, dut_v).run(quiet=1)

    def testAndOpPython(self):
        """Test And operations Python"""
        stim = self.and_test(python=True)
        Simulation(stim, self.dut).run(quiet=1)

    def testAndOpVerilog(self):
        """test And operations Verilog"""
        stim = self.and_test(verilog=True)
        dut_v = self.getVerilog()
        Simulation(stim, dut_v).run(quiet=1)

    def testAndOpTogether(self):
        """test And operations Together"""
        stim = self.and_test(verilog=True, python=True)
        dut_v = self.getVerilog()
        Simulation(stim, self.dut, dut_v).run(quiet=1)

    def testNorOpPython(self):
        """Test Nor operations Python"""
        stim = self.nor_test(python=True)
        Simulation(stim, self.dut).run(quiet=1)

    def testNorOpVerilog(self):
        """test Nor operations Verilog"""
        stim = self.nor_test(verilog=True)
        dut_v = self.getVerilog()
        Simulation(stim, dut_v).run(quiet=1)

    def testNorOpTogether(self):
        """test Nor operations Together"""
        stim = self.nor_test(verilog=True, python=True)
        dut_v = self.getVerilog()
        Simulation(stim, self.dut, dut_v).run(quiet=1)

    def testSltOpPython(self):
        """Test Slt operations Python"""
        stim = self.slt_test(python=True)
        Simulation(stim, self.dut).run(quiet=1)

    def testSltOpVerilog(self):
        """test Slt operations Verilog"""
        stim = self.slt_test(verilog=True)
        dut_v = self.getVerilog()
        Simulation(stim, dut_v).run(quiet=1)

    def testSltOpTogether(self):
        """test Slt operations Together"""
        stim = self.slt_test(verilog=True, python=True)
        dut_v = self.getVerilog()
        Simulation(stim, self.dut, dut_v).run(quiet=1)


if __name__ == '__main__':
    unittest.main()
