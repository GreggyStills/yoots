import time
import unittest

from yoots import moratorium


class TestMoratorium(unittest.TestCase):

    def test_make_day_julian(self):
        nyd = moratorium.make_day_julian("2018-01-01")
        self.assertTrue(nyd == 1)
        thx = moratorium.make_day_julian("2018-11-22")
        self.assertTrue(thx == 326)

    def test_make_month_julian(self):
        mcal = moratorium.make_month_julian(2000, 1)
        self.assertTrue(mcal == range(1, 32))

    def test_get_nth_day(self):
        # Thanksgiving 2018 (4th Thurs of Nov):  Nov 22 (Julian day: 326)
        jday = moratorium.get_nth_day("Thursday", 4, 2018, 11)
        self.assertTrue(jday == 326)

    def test_is_holiday(self):
        total_holidays = len(moratorium.holidays)
        found = 0
        for j in range(1, 366):
            dt = time.strptime("{} {}".format(2018, j), "%Y %j")
            if moratorium.is_holiday(dt):
                found += 1
        self.assertTrue(found == total_holidays)

    def test_is_eom(self):
        mdays = []
        for d in range(1, 32):
            dt = time.strptime("{} {} {}".format(2000, 1, d), "%Y %m %d")
            if moratorium.is_eom(dt, end_days=2):
                mdays.append(d)
        self.assertTrue(mdays == [30, 31])

    def test_is_eoy(self):
        # Thanksgiving 2018 (4th Thurs of Nov):  Nov 22 (Julian day: 326)
        for j in range(1, 366):
            dt = time.strptime("{} {}".format(2018, j), "%Y %j")
            if j < 326:
                self.assertFalse(moratorium.is_eoy(dt))
            else:
                self.assertTrue(moratorium.is_eoy(dt))


if __name__ == '__main__':
    unittest.main(exit=False)
