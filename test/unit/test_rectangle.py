
import unittest
from sikuli import Rectangle, Location

class TestRectangle(unittest.TestCase):
    def test_rect(self):
        r = Rectangle(0, 10, 20, 30)
        self.assertEqual(
            (r.x, r.y, r.w, r.h),
            (0, 10, 20, 30)
        )

    def test_moveTo(self):
        r = Rectangle(0, 10, 20, 30)
        r.moveTo(Location(5, 15))
        self.assertEqual(
            (r.x, r.y, r.w, r.h),
            (5, 15, 20, 30)
        )

    def test_getCenter(self):
        r = Rectangle(0, 10, 20, 30)
        self.assertEqual(
            r.getCenter(),
            Location(10, 25)
        )
