import random
import math
from itertools import izip
from array import *


# import numpy as np
# import pandas as pd

argmax = lambda array: max(izip(array, xrange(len(array))))[1]


class Polymer(object):

    def __init__(self, n, logger=None):
        self.size = n
        self.action_field = []
        self.spacevar = []
        self.timevar = []
        self.environment = [[] * (2 * n + 1)] * (n + 1)
        self.records = []
        self.choices = []
        self.max_path = []
        self.endpoint = None
        self.max_action = None
        self.logger = logger


    def log(self, s):
        """Log a message if a logger has been initialized"""
        if self.logger:
            self.logger.info(s)


    def compute_actions(self, make_path=True):
        """Generate a triangle of best actions to each point in environment,
        along with the choices made to obtain the best action.
        This is by far the most computationally challenging algorithm,
        and can require a large amount of memory."""

        n = self.size
        env = self.environment

        triangle = []
        triangle.append(array('f', [-n] * n + [env[0][n]] + [-n] * n))
        if make_path:
            choices = []
            choices.append(array('i', [0] * (2 * n - 1)))

        for i in xrange(1, n + 1):
            new_triangle_col = []
            old_triangle_col = triangle[i - 1]

            if make_path:
                new_choices_col = []

            for j in xrange(n - i, n + i + 1):
                bestparent = max([(old_triangle_col[j + k], k)
                                  for k in [-1, 0, 1] if k + j > n - i and k + j < n + i])
                if make_path:
                    new_choices_col.append(bestparent[1])
                new_triangle_col.append(bestparent[0] + env[i][j])

            if make_path:
                choices.append(
                    array('i', [0] * (n - i) + new_choices_col + [0] * (n - i)))
            triangle.append(
                array('f', [-n] * (n - i) + new_triangle_col + [-n] * (n - i)))

        self.log("Actions and choices computed.")
        self.action_field = triangle
        if make_path:
            self.choices = choices
        a, e = max([(triangle[n][x], x) for x in xrange(2 * n + 1)])
        self.max_action = a
        self.endpoint = e - n


    def make_environment(self, time_distr = "bernoulli"):
        """Generate an environment grid of size n x (2n+1),
        shifted up by n (so the origin is at (0,n)). """

        n = self.size
        if not self.spacevar:
            omega = array('f', [random.uniform(-1, 1)
                          for _ in xrange(2 * n + 1)])
            self.spacevar = omega
        else:
            omega = self.spacevar

        if not self.timevar and time_distr == "uniform":
            self.timevar = [random.uniform(-1, 1) for _ in xrange(n + 1)]
            self.log("Uniform (-1,1) time variables initialized")

        # for the default case of bernoulli -1/2,
        # or for any other distribution erroneously given
        elif not self.timevar:
            self.timevar = [random.choice([-1, 1]) for _ in xrange(n + 1)]
            self.log("Bernoulli(1/2) time variables initialized")

        nomega = array('f', [-x for x in omega])

        for i in xrange(n + 1):
            if self.timevar[i] == -1:
                self.environment[i] = nomega
            elif self.timevar[i] == 1:
                self.environment[i] = omega
            else:
                self.environment[i] = array(
                    'f', [self.timevar[i] * x for x in omega])
        self.log("Environment completed.")

    def compute_path(self, n=None):
        """ Return the best path of length n given the triangle of best 
        actions at each point and the choices made to obtain it."""
        N = self.size
        if n is None or n == 0 or n > N:
            n = N
        if not self.choices:
            Exception("Enable make_path in triangle method")

        end = argmax(self.action_field[n]) - N
        path = [0] * (n + 1)
        path[n] = end
        for i in xrange(n):
            path[n - i - 1] = path[n - i] + \
                self.choices[n - i][path[n - i] + N]
        if n == N:
            self.max_path = path
        return path

    # def stabilization((triangle, choices), step):
    #     """Return a boolean as to whether the beginning of the path determined by triangle and choices stabilizes,
    #     looking at path lengths which are multiples of step, and if paths differ, return a list of the disagreeing paths """
    #     if len(choices) == 0:
    #         Exception("Enable make_path in triangle method")
    #     stab = True
    #     disagreements = []
    #     for i in range(len(triangle) / 2, len(triangle), step):
    #         if path((triangle, choices), i)[0][:(i - step) / 2] != path((triangle, choices), (i - step))[0][:(i - step) / 2]:
    #             disagreements.append(path((triangle, choices), i - step)[0])
    #             disagreements.append(path((triangle, choices), i)[0])
    #             stab = False
    #     return stab, disagreements

#     def derivative(self):
#         """Return a list of secants of the best action at endpoints near 0,
#          starting near 0 and moving outward to a distance of the size of triangle to the 2/3 power"""
#         N = len(self.action_field) - 1
#         secants = [(self.action_field[N][i + N] - self.action_field[N][N]) / float(i)
#                    for i in xrange(1, int(math.floor(math.pow(N, 2 / float(3)))))]
#         return secants

#     def rolling_averages(self, values, gap):
#         """Return a list of the averages from values, where the first entry is the average of the first gap values, 
#         the second entry is the average of the first 2*gap values, and so on """
#         N = len(values)
#         sum = 0
#         averages = []
#         for i in xrange(N):
#             sum += values[i]
#             if (i + 1) % gap == 0:
#                 averages.append(sum / float(i + 1))
#         return averages

    def pinned_path(self, site, n = None):
        """Return the best path determined by triangle and choices,
        ending at site, of length n"""
        if len(self.choices) == 0:
            Exception("Enable make_path in triangle method")
        N = self.size
        if n is None:
            n = N
        if n > N: 
            self.log("length exceeds polymer size in pinned path class method, defaulting to max size")
            n = N
        path = [0]*(n + 1)
        path[n] = site
        for i in xrange(n):
            path[n - i - 1] = path[n - i] + self.choices[n - i][path[n - i] + N]
        return path, self.action_field[n][site+N]

#     def linearity((triangle, choices), step):
#         """Return """
#         if len(choices) == 0:
#             Exception("Enable choice array in triangle method")
#         N = len(triangle) - 1
#         return [(i, triangle[i][int(math.floor(float(i) / 2)) + N],
#                  last_edge_time(path((triangle, choices), i)[0])[0]) for i in range(step, N + 1, step)]

#     def last_edge_time(self):
#         n = len(self.max_path) - 1
#         time = n - 1
#         while self.max_path[time] == self.max_path[n]:
#             time -= 1
#             if time == 0:
#                 break
#         final_edge = min(self.max_path[time], self.max_path[n])
#         if abs(float(final_edge)) == 0:
#             return 1
#         else:
#             final_time = self.max_path.index(final_edge)
#             return final_time / abs(float(final_edge)), final_edge, final_time

#     def traps(path, env):
#         n = len(env) - 1
#         count = 0
#         for i in range(len(path)):
#             m = path[i] + n
#             if env[i][m] < 0:
#                 count += 1
#         return count

    def occupation(path):
        n = len(path) - 1
        occupation = [0 for _ in range(max(path) + n + 1)]
        for i in range(n):
            occupation[path[i] + n] += 1

        siterange = len(occupation)

        negsiterange = 0
        while occupation[negsiterange] == 0:
            negsiterange += 1

        self.log("Previous record occupation time: " +
                    str(max(occupation[negsiterange + 5: siterange - 5])))
        return zip(range(-n, siterange), occupation)


    def compute_record_locations(self):
        n = self.size
        recs = []
        min = 1
        for i in range(n - 1):
            if 2 - abs(self.environment[0][i + n] - self.environment[0][i + 1 + n]) < min:
                recs.append((i, 2 - abs(self.environment[0][i + n] - self.environment[0][i + 1 + n])))
                min = 2 - abs(self.environment[0][i + n] - self.environment[0][i + 1 + n])
            if 2 - abs(self.environment[0][-i + n] - self.environment[0][-i + 1 + n]) < min:
                recs.append(
                    (-i, 2 - abs(self.environment[0][-i + n] - self.environment[0][-i + 1 + n])))
                min = 2 - abs(self.environment[0][-i + n] - self.environment[0][-i + 1 + n])
        self.records = recs
        return recs

#     def discrepancies(occupation, env):
#         n = len(env) - 1
#         discrepancies = []
#         for j in range(len(occupation) - 1):
#             occ1 = occupation[j]
#             occ2 = occupation[j + 1]
#             if occ1[1] > 1 and occ2[1] > 1:
#                 disc = 2 - abs(env[0][n + occ1[0]] - env[0][n + occ2[0]])
#                 occ = occ1[1] + occ2[1]
#                 discrepancies.append((occ1[0], disc, occ, occ * pow(disc, 2)))
#         return discrepancies

#     def constant((grid, n)):
#         triang, choices = triangle((grid, n))
#         gamma = path((triang, choices))
#         ln = last_edge_time(gamma[0])[1]
#         n = len(triang)
#         dn = 2 - abs(grid[0][n + ln] - grid[0][n + ln + 1])
#         return (gamma[2] - n + dn * n) / float(ln)

#     def functional(omega, const):
#         n = (len(omega) - 1) / 2
#         functs = [(const * abs(i - n) / pow(n, 2 / float(3)) - (1 - (abs(omega[i] - omega[i + 1]) / 2)) * pow(n, 1 / float(3)), i - n)
#                   for i in range(len(omega) - 1)]
#         return max(functs)

#     def functional_range(omega, end):
#         step = 0.1
#         lower_bound = -10
#         upper_bound = 0
#         min = upper_bound
#         max = lower_bound
#         match_end = []
#         for c in (lower_bound + i * step for i in range(int((upper_bound - lower_bound) / step))):
#             if functional(omega, c)[1] == end:
#                 match_end.append(1)
#             else:
#                 match_end.append(0)
#         try:
#             min = lower_bound + match_end.index(1) * step
#             max = upper_bound - step * (match_end[::-1].index(1) + 1)
#         except:
#             pass
#         return min, max

    def action_range(self, a, b):
        n = self.size
        if not self.max_path:
            self.compute_path()
        if a > 0:
            return self.action_field[b][self.max_path[b]+n] - self.action_field[a-1][self.max_path[a-1]+n]
        else: 
            return self.action_field[b][self.max_path[b]+n]

