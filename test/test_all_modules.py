# CS3339-265, Team White Group Project
# Main Test Driver

""" Run all cosimulation unit tests. """

import unittest

tester = unittest.defaultTestLoader


def suite():
    # TODO: test some stuff
    print("Not implemented yet...")


def main():
    unittest.main(defaultTest='suite',
                  testRunner=unittest.TextTestRunner(verbosity=2))


if __name__ == '__main__':
    main()
