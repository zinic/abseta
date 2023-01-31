import unittest

from model import parse_roll
from model.core import Dice


class TestRollParsing(unittest.TestCase):
    def test_parse_roll(self):
        roll = parse_roll("1d2")

        self.assertEqual(Dice, type(roll))
        self.assertEqual(1, roll.num_dice)
        self.assertEqual(2, roll.sides)


if __name__ == '__main__':
    unittest.main()
