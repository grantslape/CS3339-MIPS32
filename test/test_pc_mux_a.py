import unittest
from unittest import TestCase


class TestPcMuxA(TestCase):

    def testHoldValuePython(self):
        """ Check that module holds value when no input changes """

    def testHoldValueVerilog(self):
        """ Check that module holds value when no input changes """

    def testHoldValueTogether(self):
        """ Check that modules hold value when no input changes """

    def testCorrectOutputPython(self):
        """ Check that next sequential PC address is outputted when pc_src is deasserted
            and that the imm_jmp_addr value is outputted when pc_src is asserted."""

    def testCorrectOutputVerilog(self):
        """ Check that next sequential PC address is outputted when pc_src is deasserted
            and that the imm_jmp_addr value is outputted when pc_src is asserted."""

    def testCorrectOutputTogether(self):
        """ Check that next sequential PC address is outputted when pc_src is deasserted
            and that the imm_jmp_addr value is outputted when pc_src is asserted."""


if __name__ == '__main__':
    unittest.main()
