# CS3339-265, Team White Group Project
# Main Test Driver
import unittest
from test import test_fwd_unit, test_shift_unit,test_mux32bit2to1, test_pc_adder, \
    test_mux32bit3to1, test_ex_mux, test_program_counter, test_rfile, test_sign_extender

modules = (test_mux32bit2to1,
           test_mux32bit3to1,
           test_ex_mux,
           test_fwd_unit,
           test_pc_adder,
           test_program_counter,
           test_rfile,
           test_shift_unit,
           test_sign_extender,)
tester = unittest.defaultTestLoader


def suite():
    all_tests = unittest.TestSuite()
    for m in modules:
        all_tests.addTest(tester.loadTestsFromModule(m))
    return all_tests


def main():
    """ Run all cosimulation unit tests. """
    unittest.main(defaultTest='suite',
                  testRunner=unittest.TextTestRunner(verbosity=2))


if __name__ == '__main__':
    main()
