from polymer import *
import math
import random
from datetime import datetime
import sys
import traceback
import pickle
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from counter import Counter
import numpy as np
import pandas as pd

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler('trials.log')
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

env = pd.DataFrame()

def most_common(lst):
    """return a tuple (most_common_element, count_of_element_in_list)
    """
    data = Counter(lst)
    return data.most_common(1)[0]

# def perfect_path(pol, end, size):
#     path = [0]
#     if end > 0:
#         om = discretize(pol.spacevar[size:size+end])

#     while path[-1] < end:
#         sigma = next_run(om, path[-1]+1)
#         if sigma <= next_run(pol.timevar, len(path)-1):
#             # path += [path[-1]+next_run(om, path[-1]+next_run(om, path[-1]+1))]*
#             pass
#         pass

def discretize(l):
    ret = []
    for e in l:
        if e > 0:
            ret.append(1)
        else:
            ret.append(-1)
    return ret

def next_run(l, i):
    j = i+1
    while l[j] == l[i]:
        j+=1
    return j-i

def trial(pol, size, j):

    global env

    pol.timevar = None
    pol.make_environment()
    pol.compute_actions()

    path = pol.compute_path()
    tau = path.index(path[-1])

    plt.plot(range(tau), path[:tau])

    missed_sign = 0
    bad_spots = []

    for i in range(tau):
        if pol.spacevar[path[i]+size]*pol.timevar[i] < 0:
            missed_sign += 1
            bad_spots.append(path[i])
            # plt.annotate('bad'+str(path[i])+','+str(pol.spacevar[path[i]+size]), xy = (i, path[i]), xytext = (i, path[i]))
            # plt.annotate(str(pol.timevar[i])[0], xy = ( i, 1), xytext = (i, 1) )

    # plt.annotate('', xy=(2, 1), xytext=(3, 1.5),
    #         arrowprops=dict(facecolor='black', shrink=0.05),
    #         )


    df = pd.DataFrame([ (pol.timevar[i], path[i], pol.spacevar[size+path[i]] ) for i in range(tau)], 
                        columns = ['time-%s' % (j+1), 'path-%s' % (j+1), 'space-%s' % (j+1) ]  )

    if j == 1:
        env = df
    else:
        env = pd.concat([env, df])

    # if path[-1] >= 0:
    #     space_series = pd.Series(pol.spacevar[size:path[-1]+size], name = "space")
    # else:
    #     space_series = pd.Series(pol.spacevar[size - path[-1]:size:-1], name = "space")
    # time_series = pd.DataFrame(pol.timevar[:tau], columns = ["time"])
    # path_series = pd.Series(path[:tau], name = "path")

    # env = pd.concat([env, spacevars], ignore_index=True)
    # env = time_series
    # env['path'] = path_series
    # env['space'] = space_series

    # logger.info("omega: %s", pol.spacevar[size:20])

    
    # This is to find the best entry point to the ending edge:
    a = max( [ ( pol.action_field[i][size+path[-1]] - i, i ) for i in range(size) ] )[1]
    logger.info("Tau = %s, Maximizing arrival = %s", tau, a )



    return tau/float(path[-1]), missed_sign, bad_spots

def runtrials(trials, size):
    runs = 1

    startTime = datetime.now()

    logger.info("Trials initiated.")

    polymer = Polymer(size, logger)

    # Use just plus or minus 1 as space variables for clearer picture
    polymer.spacevar = [(-1)**((i % (2*runs)) / runs) * random.uniform(0,1) for i in xrange(2 * size + 1)] 
    taus = []
    missed_signs = []
    bad_spots = []

    for j in range(trials):
        t, m, b = trial(polymer, size, j)
        taus.append(t)
        missed_signs.append(m)
        bad_spots += b
        bad_spots.sort()

    env.to_csv('./plots/env.csv')

    plt.legend(range(1, trials+1), loc='upper left')
    plt.savefig('./plots/taus:'+str(size)+'-'+str(datetime.now())+'.pdf')


    avg =  sum(taus)/float(len(taus))
    var = variance(taus, avg)

    email_message = ("Program: Variance of taus up to ending edge" +'\n' 
                     "Start: " + str(startTime) + '\n' 
                     "Finish: " + str(datetime.now()) + '\n' 
                     "Runtime: " + str(datetime.now() - startTime) + '\n' 
                     "Size: " + str(size) + '\n' 
                     "Number of Trials: " + str(trials) + '\n' 
                     "Avg for taus: " + str(avg) +'\n' 
                     "variance for taus: " + str(var) + '\n' 
                     "missed_signs: " + str(missed_signs) + '\n'
                     # "Bad sites: " + str(bad_spots)
                     )

    logger.info("Test of string %s, %s", 3, 4)

    logger.info(email_message)

def variance(l, avg):
    return sum([(e - avg) ** 2 for e in l])/float(len(l))

if __name__ == '__main__':
    try:
        runtrials(eval(sys.argv[1]), eval(sys.argv[2]))
    except:
        logger.warning(traceback.format_exc())

# cProfile.run(script)
