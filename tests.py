import unittest
import random
from polymer import Polymer

def test_pinned_path(n):
    poly = Polymer(n)
    poly.make_environment()
    poly.compute_actions()
    for i in range(n+1):
        j = random.randint(-i,i)
        try:
            poly.pinned_path(j, i)
        except IndexError:
            print "failure at ", j, i

def test__path(n):
    poly = Polymer(n)
    poly.make_environment()
    poly.compute_actions()
    poly.compute_path()
    poly.compute_record_locations()
    poly.records
    for i in range(n+1):
        try:
            poly.compute_path(i)
        except IndexError:
            print "failure at ", i


class PolymerTests(unittest.TestCase):

    def test_action(self):
        poly = Polymer(1000)
        poly.make_environment()
        poly.compute_actions()
        poly.compute_path()
        self.assertEqual(poly.action_range(1, 1000)+poly.environment[0][1000], poly.max_action)

def main():
    unittest.main()

if __name__ == '__main__':
    test__path(100)
    test_pinned_path(100)
    main()
