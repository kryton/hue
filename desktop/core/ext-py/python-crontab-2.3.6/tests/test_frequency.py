#!/usr/bin/env python
#
# Copyright (C) 2013 Martin Owens
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3.0 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library.
#
"""
Test frequency calculations
"""

import os
import sys

sys.path.insert(0, '../')

import unittest
from crontab import CronTab, PY3
try:
    from test import test_support
except ImportError:
    from test import support as test_support

if PY3:
    unicode = str

START_TAB = """
"""

class FrequencyTestCase(unittest.TestCase):
    """Test basic functionality of crontab."""
    def setUp(self):
        self.crontab = CronTab(tab=START_TAB.strip())
        self.job = self.crontab.new(command='freq')

    def test_00_slice_frequency(self):
        """Each Slice Frequency"""
        # Make sure some of these overlap
        self.job.setall("13-16,14-15 6,*/3 2,3,4 * *")
        self.assertEqual(len(self.job[0]), 4)
        self.assertEqual(len(self.job[1]), 8)
        self.assertEqual(len(self.job[2]), 3)
        self.assertEqual(len(self.job[3]), 12)
        self.assertEqual(len(self.job[4]), 7)

    def test_01_per_day(self):
        """Frequency per Day"""
        self.job.setall("21-29 10-14 * * *")
        self.assertEqual(len(self.job[0]), 9)
        self.assertEqual(len(self.job[1]), 5)
        self.assertEqual(self.job.frequency_per_day(), 45)

    def test_02_days_per_year(self):
        """Frequency in Days per Year"""
        self.job.setall("* * * * *")
        self.assertEqual(self.job.frequency_per_year(year=2010), 365)
        self.assertEqual(self.job.frequency_per_year(year=2012), 366)
        self.job.setall("1 1 11-20 1,4,6,8 0,6")
        self.assertEqual(len(self.job[2]), 10)
        self.assertEqual(len(self.job[3]), 4)
        self.assertEqual(len(self.job[4]), 2)
        self.assertEqual(self.job.frequency_per_year(year=2013), 11)
        self.assertEqual(self.job.frequency_per_year(year=2010), 12)

    def test_03_job(self):
        """Once Yearly"""
        self.job.setall("0 0 1 1 *")
        self.assertEqual(self.job.frequency(year=2010), 1)

    def test_04_twice(self):
        """Twice Yearly"""
        self.job.setall("0 0 1 1,6 *")
        self.assertEqual(self.job.frequency(year=2010), 2)

    def test_05_thrice(self):
        """Thrice Yearly"""
        self.job.setall("0 0 1 1,3,6 *")
        self.assertEqual(self.job.frequency(year=2010), 3)

    def test_06_quart(self):
        """Four Yearly"""
        self.job.setall("0 0 1 */3 *")
        self.assertEqual(self.job.frequency(year=2010), 4)

    def test_07_monthly(self):
        """Once a month"""
        self.job.setall("0 0 1 * *")
        self.assertEqual(self.job.frequency(year=2010), 12)

    def test_08_six_monthly(self):
        """Six a month"""
        self.job.setall("0 0 1,2,3,4,5,6 * *")
        self.assertEqual(self.job.frequency(year=2010), 72)

    def test_09_every_day(self):
        """Every Day"""
        self.job.setall("0 0 * * *")
        self.assertEqual(self.job.frequency(year=2010), 365)

    def test_10_every_hour(self):
        """Every Hour"""
        self.job.setall("0 * * * *")
        self.assertEqual(self.job.frequency(year=2010), 8760)

    def test_11_every_other_hour(self):
        """Every Other Hour"""
        self.job.setall("0 */2 * * *")
        self.assertEqual(self.job.frequency(year=2010), 4380)

    def test_12_every_minute(self):
        """Every Minute"""
        self.job.setall("* * * * *")
        self.assertEqual(self.job.frequency(year=2010), 525600)

    def test_13_enum(self):
        """Enumerations"""
        self.job.setall("0 0 * * MON-WED")
        self.assertEqual(self.job.frequency(year=2010), 156)
        self.job.setall("0 0 * JAN-MAR *")
        self.assertEqual(self.job.frequency(year=2010), 90)

    def test_14_all(self):
        """Test Maximum"""
        self.job.setall("* * * * *")
        self.assertEqual(self.job.frequency(2010), 525600)
        self.assertEqual(self.job.frequency_per_year(year=2010), 365)
        self.assertEqual(self.job.frequency_per_day(), 1440)
        self.job.setall("*")
        self.assertEqual(self.job.frequency_per_day(), 1440)
        self.assertEqual(self.job.frequency_per_year(year=2010), 365)
        self.assertEqual(self.job.frequency(2010), 525600)

    def test_15_compare(self):
        """Compare Times"""
        job = self.crontab.new(command='match')
        job.setall("*/2 * * * *")
        self.assertEqual(job.slices, "*/2 * * * *")
        self.assertEqual(job.slices, ["*/2"])
        self.assertLess(job, ["*"])
        self.assertGreater(job, "*/3")

    def test_16_frequency_per_hour(self):
        """Count per hour"""
        job = self.crontab.new(command='per_hour')
        job.setall("*/2 * * * *")
        self.assertEqual(job.frequency_per_hour(), 30)

if __name__ == '__main__':
    test_support.run_unittest(
       FrequencyTestCase,
    )
