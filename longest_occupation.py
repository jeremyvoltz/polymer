from polymer import *
import math
import random
from datetime import datetime
import sys
import traceback
import pickle
# import matplotlib
# matplotlib.use('Agg')
# import matplotlib.pyplot as plt
from counter import Counter
import numpy as np

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


alpha_one = 0.3
alpha_two = 0.9

TEST_INTERVALS = 5

seq_one = []
seq_two = []
critical = []
critical_diff_sizes = [[] for _ in range(TEST_INTERVALS)]

def most_common(lst):
    """return a tuple (most_common_element, count_of_element_in_list)
    """
    data = Counter(lst)
    return data.most_common(1)[0]


def trial(size):

    polymer = Polymer(size, logger)
    polymer.make_environment()
    polymer.compute_actions()

    s_one = []
    s_two = []

    for i in range(1, TEST_INTERVALS + 1):
        j = i*size / TEST_INTERVALS
        p_1, a_1 = polymer.pinned_path(int(math.floor(alpha_one * j)), j)
        e_1, c_1 = most_common(p_1)
        s_one.append(c_1 / float(j))
        p_2, a_2 = polymer.pinned_path(int(math.floor(alpha_two * j)), j)
        s_two.append(most_common(p_2)[1] / float(j))
        critical_diff_sizes[i-1].append(float(abs(e_1)) / p_1.index(e_1))


    critical.append( float(abs(e_1)) / p_1.index(e_1) )

    seq_one.append(s_one)
    seq_two.append(s_two)

    pickle.dump( (seq_one, seq_two), open( "occs.p", "wb" ) )

    # plt.plot(range(size+1), p_1)
    # plt.savefig('./plots/pinned_path:'+str(size)+'-'+str(datetime.now())+'.pdf')
    # return None


def runtrials(trials, size):
    startTime = datetime.now()

    logger.info("Trials initiated.")

    global seq_one, seq_two

    for _ in range(trials):
        trial(size)

    array_one = np.array(seq_one)
    array_two = np.array(seq_two)

    seq_one = np.mean(array_one, axis=0)
    seq_two = np.mean(array_two, axis=0)

    avg_critical = sum(critical)/len(critical)
    var_critical = variance(critical, avg_critical)

    array_critical_diff_sizes = np.array(critical_diff_sizes)
    avg_critical_diff_sizes = np.mean(array_critical_diff_sizes, axis = 1)
    var_critical_diff_sizes = np.var(array_critical_diff_sizes, axis = 1)

    
    email_message = ("Program: Sequence of longest occupation divided by size" +'\n'
                     "Start: " + str(startTime) + '\n'
                     "Finish: " + str(datetime.now()) + '\n'
                     "Runtime: " + str(datetime.now() - startTime) + '\n'
                     "Size: " + str(size) + '\n'
                     "Number of Trials: " + str(trials) + '\n'
                     "Sequence avg for alpha_one: " + str(seq_one) +'\n'
                     "Sequence avg for alpha_two: " + str(seq_two) +'\n'
                     "Sequence avg for critical alpha: " + str(avg_critical_diff_sizes) + '\n'
                     "Sequence var for critical alpha: " + str(var_critical_diff_sizes) + '\n' 
                     "Critical alpha and variance: " + str(avg_critical) + ', ' + str(var_critical) 
                     )


    logger.info(email_message)

def variance(l, avg):
    return sum([(e - avg) ** 2 for e in l])/float(len(l))

if __name__ == '__main__':
    try:
        runtrials(eval(sys.argv[1]), eval(sys.argv[2]))
    except:
        logger.warning(traceback.format_exc())

# cProfile.run(script)
