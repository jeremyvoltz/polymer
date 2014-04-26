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


alpha_one = 0.2
alpha_two = 0.3
alpha_three = 0.4

shape_one = []
shape_two = []
shape_three = []

shape = []

ORIGIN_CLOSENESS = 0.9
counted = 0


def trial(size):

    polymer = Polymer(size, logger)
    polymer.make_environment()
    polymer.compute_actions(make_path=False)
    shape_one.append(polymer.action_field[size]
                     [size + int(math.floor(alpha_one * size))] / size)
    shape_one.append(polymer.action_field[size]
                     [size + int(math.ceil(-alpha_one * size))] / size)
    shape_two.append(polymer.action_field[size]
                     [size + int(math.floor(alpha_two * size))] / size)
    shape_two.append(polymer.action_field[size]
                     [size + int(math.ceil(-alpha_two * size))] / size)
    shape_three.append(polymer.action_field[size]
                     [size + int(math.floor(alpha_three * size))] / size)
    shape_three.append(polymer.action_field[size]
                     [size + int(math.ceil(-alpha_three * size))] / size)



    global shape
    global counted

    if polymer.action_field[size][size] > ORIGIN_CLOSENESS*size:
        counted+=1
        shape = [a + b for a, b in zip(shape, polymer.action_field[size])]
        pickle.dump( shape, open( "actions.p", "wb" ) )


def runtrials(trials, size):
    startTime = datetime.now()

    logger.info("Trials initiated.")

    global shape
    shape = [0 for _ in range(2*size+1)]
    for _ in range(trials):
        trial(size)

    avg_one = sum(shape_one) / float(len(shape_one))
    avg_two = sum(shape_two) / float(len(shape_two))
    avg_three = sum(shape_three) / float(len(shape_three))

    var_one = variance(shape_one, avg_one)
    var_two = variance(shape_two, avg_two)
    var_three = variance(shape_three, avg_three)

    email_message = ("Start: " + str(startTime) + '\n'
                     "Finish: " + str(datetime.now()) + '\n'
                     "Runtime: " + str(datetime.now() - startTime) + '\n'
                     "Number of Trials: " + str(trials) + '\n'
                     "Number of Trials above origin threshold of " + str(ORIGIN_CLOSENESS) + ": " + str(counted) + '\n'
                     "mean and variance for alpha_1 = "+str(alpha_one)+": " +
                     str(avg_one) + ", " + str(var_one) + '\n'
                     "mean and variance for alpha_2 = "+str(alpha_two)+": " + str(avg_two) + ", " + str(var_two) +'\n'
                     "mean and variance for alpha_3 = "+str(alpha_three)+": " +
                     str(avg_three) + ", " + str(var_three))

    logger.info(email_message)

    shape = [i/(counted*size) for i in shape]

    plt.plot([(i - size)/float(size) for i in range(2*size+1)], shape)
    plt.savefig('./plots/shape-function-size:'+str(size)+'-trials:'+str(counted)+'-'+str(datetime.now())+'.pdf')


def variance(l, avg):
    return sum([(e - avg) ** 2 for e in l])


if __name__ == '__main__':
    try:
        runtrials(eval(sys.argv[1]), eval(sys.argv[2]))
    except:
        logger.warning(traceback.format_exc())

# cProfile.run(script)
