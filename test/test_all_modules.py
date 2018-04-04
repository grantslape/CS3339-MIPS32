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
import test_wb_mux

modules = (test_pc_mux_a,
           test_shift_unit,test_fwd_unit)
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
