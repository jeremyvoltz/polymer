#!/usr/bin/python

import unittest
import random
from polymer import Polymer
from tau_variance import runtrials, variance, spacevar_typical

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
    poly.compute_record_discrepancies()
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
        exponent = 0.5
        constant = 10
        poly = Polymer(size)
        poly.make_environment()
        poly.compute_actions()
        path = poly.compute_path()
        end = poly.compute_endpoint()
        self.assertTrue(poly.discrepancy(end) < constant*pow(abs(float(end)), -exponent) )

    def test_typical_omega(self):
        size = 1000
        trials = 100
        threshold = .9
        count_typical = 0
        for i in range(trials):
            poly = Polymer(size)
            poly.make_environment()
            count_typical += spacevar_typical(poly)
        # print count_typical
        self.assertTrue(count_typical > threshold*trials)


    # def test_variance_method(self):
    #     trials = 1000
    #     error = .1
    #     mu = random.uniform(-10,10)
    #     sigma = random.uniform(0,10)
    #     var = variance([random.gauss(mu, sigma) for _ in range(trials)])
    #     self.assertAlmostEqual(sigma, pow(var, 0.5), delta = error)

    # def test_variance_known(self):
    #     values = [random.choice([-1,1]) for _ in range(30)]
    #     self.assertAlmostEqual(variance(values, 0), 1)

    # Write tests for computing path, endpoint, and tau in wrong orders

    # Write test for paths ending at the same spot in multiple trials

def main():
    unittest.main()

if __name__ == '__main__':
    test__path(100)
    test_pinned_path(100)
    main()
