#
# Copyright (c) 2009 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 2 (GPLv2). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv2
# along with this software; if not, see
# http://www.gnu.org/licenses/old-licenses/gpl-2.0.txt.
#

""" Unit tests for CLI """

from rho.clicommands import *

import unittest
import os
import sys


class HushUpStderr(object):
    def write(self, s):
        pass


class CliCommandsTests(unittest.TestCase):
    conffile = "test/rho.conf.test"

    def setUp(self):
        if os.path.exists(self.conffile):
            os.remove(self.conffile)

        # Temporarily disable stderr for these tests, CLI errors clutter up
        # nosetests command.
        self.orig_stderr = sys.stderr
        sys.stderr = HushUpStderr()

    def tearDown(self):
        # Restore stderr
        sys.stderr = self.orig_stderr

    def _run_test(self, cmd, args):
        os.environ[RHO_PASSPHRASE] = "blerg"

        sys.argv = ["bin/rho" ]  + args + ["--config", self.conffile]
        cmd.main()

    def test_scan(self):
        try:
            self._run_test(ScanCommand(), ["scan"])
        except SystemExit:
            pass

    def test_profile_show(self):
        self._run_test(ProfileShowCommand(), ["profile", "show"])

    def test_profile_add(self):
        self._run_test(ProfileAddCommand(), ["profile", "add", "--name", "profilename"])

    def test_auth_show(self):
        self._run_test(AuthShowCommand(), ["auth", "show"])

    def test_auth_add(self):
        try:
            self._run_test(AuthAddCommand(), ["auth", "add"])
        except SystemExit:
            # we expect this to throw a optparse.parse.error
            pass

    def test_dumpconfig(self):
        try:
            self._run_test(DumpConfigCommand(), ['dumpconfig',
                                                 '--config', 
                                                 'test/data/encrypted.data'])
        except SystemExit:
            pass

    def test_scan_bad_range_options(self):
        # Should fail scanning range without a username:
        self.assertRaises(SystemExit, self._run_test, ScanCommand(),
                ['scan', '--range=192.168.1.1'])
