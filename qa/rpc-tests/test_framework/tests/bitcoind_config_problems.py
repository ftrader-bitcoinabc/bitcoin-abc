#!/usr/bin/env python3
# Copyright (c) 2017 The Bitcoin developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

# Check that test reports an error to user if bitcoind binary cannot be
# found.

import os
import sys

from test_framework.test_framework import BitcoinTestFramework, ComparisonTestFramework
from test_framework.outputchecker import OutputChecker
from test_framework.util import (start_node,
                                 assert_equal)

#class ErrorBitcoindNotFound_Test (BitcoinTestFramework):
class ErrorBitcoindNotFound_Test (ComparisonTestFramework):

    def __init__(self):
        super(ErrorBitcoindNotFound_Test, self).__init__()
        self.num_nodes = 1
        self.setup_clean_chain = False
        # Standard help blurb that is attached to error messages.
        self.blurb = "\nTry specifying using --testbinary option, " + \
                     "or set BITCOIND environment variable."

    def setup_network(self):
        pass

    def test_startup_nonexistent_bitcoind(self):
        # Start node with non-existent binary
        # First make sure it really does not exist.
        nonexistent_binary = os.sep + 'thisdoesnotexist'
        assert(not os.path.exists(nonexistent_binary))
        try:
            self.extra_args = [["-debug"]]
            self.nodes[0] = start_node(0, self.options.tmpdir,
                                       self.extra_args[0],
                                       binary=[nonexistent_binary])
        except ValueError as e:
            assert_equal(str(e), "Unable to locate specified binary for " + \
                                 "this test (%s)." % nonexistent_binary + \
                                 self.blurb)
        else:
            raise AssertionError('Must raise an error message if specified'
                                 ' bitcoind does not exist.')

    def test_startup_no_bitcoind(self):
        # Start node with default binary (defaults to 'bitcoind')
        # Unset the BITCOIND environment variable first, if it has been set.
        old_bitcoind = ''
        try:
            # Save for later restoration
            old_bitcoind = os.environ['BITCOIND']
            # Remove it for this test if exists
            del os.environ['BITCOIND']
        except KeyError:
            # If it was not set, ignore
            pass
        # Now try to start the node with default binary.
        try:
            self.extra_args = [["-debug"]]
            self.nodes[0] = start_node(0, self.options.tmpdir,
                                       self.extra_args[0])
        except ValueError as e:
            assert_equal(str(e), "Unable to locate bitcoind for this test."
                                 + self.blurb)
        else:
            raise AssertionError('Must raise an error message if specified'
                                 ' bitcoind does not exist.')
        # Restore in case other test cases need it
        os.environ['BITCOIND'] = old_bitcoind


    def run_test(self):
        self.test_startup_nonexistent_bitcoind()
        self.test_startup_no_bitcoind()


if __name__ == '__main__':
    ErrorBitcoindNotFound_Test().main ()
