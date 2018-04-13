"""
# CS3339-265, Team White Group Project
# Main Test Driver for all unit tests
"""
import unittest

from test import test_fwd_unit, test_shift_unit, test_mux32bit2to1, test_pc_adder, \
    test_mux32bit3to1, test_ex_mux, test_program_counter, test_rfile, test_sign_extender, \
    test_id_ex, test_id_shift_left, test_branch_adder, test_mem_wb, test_ex_mem
#   test_data_mem, test_if_id, test_hazard_unit

MODULES = (test_mux32bit2to1,
           test_mux32bit3to1,
           test_ex_mux,
           test_fwd_unit,
           test_pc_adder,
           test_program_counter,
           test_rfile,
           test_shift_unit,
           test_sign_extender,
           test_id_ex,
           test_id_shift_left,
           test_branch_adder,
           test_mem_wb,
           test_ex_mem,)
TESTER = unittest.defaultTestLoader


def suite():
    """Build test suite from MODULES"""
    all_tests = unittest.TestSuite()
    for module in MODULES:
        all_tests.addTest(TESTER.loadTestsFromModule(module))
    return all_tests


def main():
    """ Run all cosimulation unit tests. """
    unittest.main(defaultTest='suite',
                  testRunner=unittest.TextTestRunner(verbosity=2))


if __name__ == '__main__':
    main()
