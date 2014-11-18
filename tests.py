#!/usr/bin/python

import unittest
import random
from polymer import Polymer
from tau_variance import runtrials

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
        size = 1000
        poly = Polymer(size)
        poly.make_environment()
        poly.compute_actions()
        poly.compute_path()
        self.assertEqual(poly.action_range(1, size)+poly.environment[0][size], poly.max_action)

    def test_runtrials(self):
        runtrials(2, 1000)

    def test_endpoint(self):
        size = 1000
        poly = Polymer(size)
        poly.make_environment()
        poly.compute_actions()
        path = poly.compute_path()
        end = poly.compute_endpoint()
        self.assertTrue(abs(path[-1] - end) <= 1)

    def test_tau(self):
        size = 1000
        poly = Polymer(size)
        poly.make_environment()
        poly.compute_actions()
        path = poly.compute_path()
        end = poly.compute_endpoint()
        tau = poly.compute_tau()
        self.assertTrue(abs(end) > abs(path[tau-1])) 

    def test_end_discrepancy(self):
        size = 1000
        exponent = 1/2
        poly = Polymer(size)
        poly.make_environment()
        poly.compute_actions()
        path = poly.compute_path()
        end = poly.compute_endpoint()
        self.assertTrue(poly.discrepancy(end) < pow(float(end), -exponent) )


    # Write tests for computing path, endpoint, and tau in wrong orders

    # Write test for paths ending at the same spot in multiple trials

def main():
    unittest.main()

if __name__ == '__main__':
    test__path(100)
    test_pinned_path(100)
    main()
