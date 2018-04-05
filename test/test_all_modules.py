# CS3339-265, Team White Group Project
# Main Test Driver

""" Run all cosimulation unit tests. """
import sys
import unittest
sys.path.append("test")
import test_pc_mux_a
import test_pc_mux_b
import test_fwd_unit
import test_shift_unit
import test_alu_mux_a
import test_alu_mux_b
import test_ex_mux
import test_pc_adder
import test_program_counter
import test_rfile
import test_wb_mux

modules = (test_alu_mux_a,
           test_alu_mux_b,
           test_ex_mux,
           test_fwd_unit,
           test_pc_adder,
           test_pc_mux_a,
           test_pc_mux_b,
           test_program_counter,
           test_rfile,
           test_shift_unit,
           test_wb_mux,)
tester = unittest.defaultTestLoader


def suite():
    all_tests = unittest.TestSuite()
    for m in modules:
        all_tests.addTest(tester.loadTestsFromModule(m))
    return all_tests


def main():
    unittest.main(defaultTest='suite',
                  testRunner=unittest.TextTestRunner(verbosity=2))


if __name__ == '__main__':
    main()
