#!/usr/bin/env python3

import argparse
import json
import random
from bottle import route, run, response, static_file
from functools import wraps
from time import time
import asyncio
import websockets
import threading

start_time = 1492355640.0
flags = [
  {
    "ts": 1492355645.59566,
    "victim_id": 17,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355645.60073,
    "victim_id": 3,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355645.60391,
    "victim_id": 13,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355645.60836,
    "victim_id": 19,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355645.89361,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355646.02667,
    "victim_id": 7,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355646.03474,
    "victim_id": 2,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355646.859,
    "victim_id": 16,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355650.62703,
    "victim_id": 11,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355651.34727,
    "victim_id": 23,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355653.54947,
    "victim_id": 22,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355655.65216,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 6
  },
  {
    "ts": 1492355656.14673,
    "victim_id": 20,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355656.21752,
    "victim_id": 20,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355656.34694,
    "victim_id": 20,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355660.1727,
    "victim_id": 22,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355675.24517,
    "victim_id": 22,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355675.41654,
    "victim_id": 5,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355676.50444,
    "victim_id": 7,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355676.53112,
    "victim_id": 7,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355677.46321,
    "victim_id": 23,
    "attacker_id": 14,
    "service_id": 4
  },
  {
    "ts": 1492355679.60602,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355683.11875,
    "victim_id": 22,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355683.90285,
    "victim_id": 22,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355689.99004,
    "victim_id": 22,
    "attacker_id": 5,
    "service_id": 6
  },
  {
    "ts": 1492355691.79022,
    "victim_id": 22,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355704.32467,
    "victim_id": 16,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355704.56383,
    "victim_id": 3,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355704.56971,
    "victim_id": 7,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355704.80662,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355705.76905,
    "victim_id": 3,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355705.77355,
    "victim_id": 17,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355705.77791,
    "victim_id": 13,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355705.78124,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355706.60954,
    "victim_id": 2,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355706.61558,
    "victim_id": 21,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355709.45599,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355711.08812,
    "victim_id": 23,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355716.25365,
    "victim_id": 22,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355718.16189,
    "victim_id": 23,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355718.16813,
    "victim_id": 23,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355720.75153,
    "victim_id": 23,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355722.11672,
    "victim_id": 22,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355722.12275,
    "victim_id": 23,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355725.86249,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 6
  },
  {
    "ts": 1492355727.4079,
    "victim_id": 20,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355728.80866,
    "victim_id": 22,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355739.28259,
    "victim_id": 22,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355744.94147,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355747.63438,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355749.16248,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355749.9134,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355750.02098,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355750.17814,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355750.25403,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355750.36779,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355750.42307,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355755.99018,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355760.10274,
    "victim_id": 5,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355760.85058,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355763.79513,
    "victim_id": 15,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355765.41319,
    "victim_id": 16,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355766.03151,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355766.03415,
    "victim_id": 3,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355766.17479,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355766.78347,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355767.37046,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355767.83827,
    "victim_id": 6,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355769.59161,
    "victim_id": 23,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355771.07041,
    "victim_id": 9,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.07503,
    "victim_id": 7,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.07688,
    "victim_id": 13,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.07837,
    "victim_id": 3,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.07885,
    "victim_id": 17,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.08284,
    "victim_id": 23,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.08524,
    "victim_id": 21,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.08838,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.08954,
    "victim_id": 12,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.09201,
    "victim_id": 6,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.09392,
    "victim_id": 15,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.09963,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.09985,
    "victim_id": 18,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355771.10581,
    "victim_id": 16,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355772.03081,
    "victim_id": 22,
    "attacker_id": 15,
    "service_id": 6
  },
  {
    "ts": 1492355773.11681,
    "victim_id": 23,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355774.92285,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355774.92676,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355774.93156,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355776.15438,
    "victim_id": 10,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355776.15689,
    "victim_id": 5,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355776.15803,
    "victim_id": 8,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355776.16459,
    "victim_id": 20,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355776.16846,
    "victim_id": 11,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355779.26164,
    "victim_id": 22,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355786.20308,
    "victim_id": 22,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355794.89313,
    "victim_id": 19,
    "attacker_id": 20,
    "service_id": 4
  },
  {
    "ts": 1492355794.92968,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355794.93325,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355794.93708,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355794.94436,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355796.29298,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 6
  },
  {
    "ts": 1492355799.92643,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355801.02756,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355801.03606,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355801.04618,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355802.50487,
    "victim_id": 22,
    "attacker_id": 19,
    "service_id": 6
  },
  {
    "ts": 1492355803.30258,
    "victim_id": 22,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355803.74883,
    "victim_id": 23,
    "attacker_id": 14,
    "service_id": 4
  },
  {
    "ts": 1492355805.70755,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355807.34981,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355807.40339,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355807.44497,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355807.49139,
    "victim_id": 23,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355811.24205,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355811.4736,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355811.70733,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355811.8151,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355811.89125,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355813.60179,
    "victim_id": 22,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355815.04155,
    "victim_id": 22,
    "attacker_id": 5,
    "service_id": 6
  },
  {
    "ts": 1492355815.04235,
    "victim_id": 22,
    "attacker_id": 5,
    "service_id": 6
  },
  {
    "ts": 1492355815.42663,
    "victim_id": 4,
    "attacker_id": 18,
    "service_id": 4
  },
  {
    "ts": 1492355820.18086,
    "victim_id": 23,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355820.49816,
    "victim_id": 23,
    "attacker_id": 3,
    "service_id": 6
  },
  {
    "ts": 1492355824.77645,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355825.71299,
    "victim_id": 19,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355825.73541,
    "victim_id": 14,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355826.48061,
    "victim_id": 3,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355826.49416,
    "victim_id": 17,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355826.52334,
    "victim_id": 23,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355826.52696,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355826.53449,
    "victim_id": 20,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355831.56472,
    "victim_id": 8,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355832.78192,
    "victim_id": 23,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355833.87522,
    "victim_id": 23,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355836.10745,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355839.11471,
    "victim_id": 7,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355839.61943,
    "victim_id": 22,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355843.35665,
    "victim_id": 22,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355843.36288,
    "victim_id": 22,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355846.00021,
    "victim_id": 22,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355848.13576,
    "victim_id": 20,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355848.19866,
    "victim_id": 20,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355849.38818,
    "victim_id": 21,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355850.65232,
    "victim_id": 22,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355863.40543,
    "victim_id": 23,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355863.41092,
    "victim_id": 23,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355865.54504,
    "victim_id": 23,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355866.75695,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 6
  },
  {
    "ts": 1492355870.04874,
    "victim_id": 22,
    "attacker_id": 5,
    "service_id": 6
  },
  {
    "ts": 1492355880.80906,
    "victim_id": 22,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355882.28282,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355882.38308,
    "victim_id": 15,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355884.37524,
    "victim_id": 7,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355884.56109,
    "victim_id": 22,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355886.09971,
    "victim_id": 16,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355886.88952,
    "victim_id": 19,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355886.89285,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355886.89737,
    "victim_id": 20,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355886.90071,
    "victim_id": 11,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355886.90435,
    "victim_id": 13,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355887.27093,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355888.45383,
    "victim_id": 19,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355889.91699,
    "victim_id": 23,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355894.74212,
    "victim_id": 23,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355894.74731,
    "victim_id": 22,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355896.17037,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355897.26624,
    "victim_id": 22,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355897.49703,
    "victim_id": 22,
    "attacker_id": 15,
    "service_id": 4
  },
  {
    "ts": 1492355898.57668,
    "victim_id": 23,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355899.67188,
    "victim_id": 4,
    "attacker_id": 15,
    "service_id": 4
  },
  {
    "ts": 1492355900.63199,
    "victim_id": 22,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355900.63745,
    "victim_id": 23,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355900.84088,
    "victim_id": 3,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355906.10504,
    "victim_id": 8,
    "attacker_id": 20,
    "service_id": 4
  },
  {
    "ts": 1492355916.13084,
    "victim_id": 5,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355916.77843,
    "victim_id": 8,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355923.47292,
    "victim_id": 22,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355926.38375,
    "victim_id": 23,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355930.0527,
    "victim_id": 22,
    "attacker_id": 5,
    "service_id": 6
  },
  {
    "ts": 1492355935.16796,
    "victim_id": 22,
    "attacker_id": 19,
    "service_id": 6
  },
  {
    "ts": 1492355937.08938,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 6
  },
  {
    "ts": 1492355944.81885,
    "victim_id": 16,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355945.10977,
    "victim_id": 21,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355946.45984,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355947.13996,
    "victim_id": 19,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.14278,
    "victim_id": 3,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.14426,
    "victim_id": 8,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.14846,
    "victim_id": 21,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.1499,
    "victim_id": 11,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.1572,
    "victim_id": 17,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.16349,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 2
  },
  {
    "ts": 1492355947.16777,
    "victim_id": 2,
    "attacker_id": 11,
    "service_id": 2
  },
  {
    "ts": 1492355950.36374,
    "victim_id": 19,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355952.19206,
    "victim_id": 13,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.19248,
    "victim_id": 6,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.19462,
    "victim_id": 8,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.19732,
    "victim_id": 14,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.19918,
    "victim_id": 18,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.20012,
    "victim_id": 23,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.20316,
    "victim_id": 2,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.20538,
    "victim_id": 17,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.21118,
    "victim_id": 21,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.21149,
    "victim_id": 15,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.21199,
    "victim_id": 10,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.21925,
    "victim_id": 22,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355952.2204,
    "victim_id": 1,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355953.14309,
    "victim_id": 15,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355953.50286,
    "victim_id": 22,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355954.98811,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355954.99432,
    "victim_id": 23,
    "attacker_id": 6,
    "service_id": 6
  },
  {
    "ts": 1492355955.32994,
    "victim_id": 22,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355955.33507,
    "victim_id": 23,
    "attacker_id": 7,
    "service_id": 6
  },
  {
    "ts": 1492355957.256,
    "victim_id": 19,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355957.26105,
    "victim_id": 5,
    "attacker_id": 4,
    "service_id": 7
  },
  {
    "ts": 1492355957.82813,
    "victim_id": 22,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355958.17973,
    "victim_id": 22,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355959.59261,
    "victim_id": 23,
    "attacker_id": 14,
    "service_id": 6
  },
  {
    "ts": 1492355961.334,
    "victim_id": 23,
    "attacker_id": 11,
    "service_id": 6
  },
  {
    "ts": 1492355962.3008,
    "victim_id": 13,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355965.24907,
    "victim_id": 21,
    "attacker_id": 12,
    "service_id": 2
  },
  {
    "ts": 1492355967.32028,
    "victim_id": 22,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355970.87162,
    "victim_id": 8,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355971.06446,
    "victim_id": 21,
    "attacker_id": 15,
    "service_id": 3
  },
  {
    "ts": 1492355971.16376,
    "victim_id": 17,
    "attacker_id": 19,
    "service_id": 2
  },
  {
    "ts": 1492355975.491,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.50017,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.50834,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.51665,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.52421,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.53255,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.53942,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.54689,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.55546,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.56232,
    "victim_id": 23,
    "attacker_id": 16,
    "service_id": 6
  },
  {
    "ts": 1492355975.64781,
    "victim_id": 13,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355975.65142,
    "victim_id": 7,
    "attacker_id": 5,
    "service_id": 2
  },
  {
    "ts": 1492355978.52762,
    "victim_id": 23,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355978.53716,
    "victim_id": 23,
    "attacker_id": 13,
    "service_id": 6
  },
  {
    "ts": 1492355981.76577,
    "victim_id": 23,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355981.84075,
    "victim_id": 22,
    "attacker_id": 20,
    "service_id": 6
  },
  {
    "ts": 1492355982.28565,
    "victim_id": 23,
    "attacker_id": 12,
    "service_id": 6
  },
  {
    "ts": 1492355990.06411,
    "victim_id": 22,
    "attacker_id": 5,
    "service_id": 6
  },
  {
    "ts": 1492355996.70448,
    "victim_id": 22,
    "attacker_id": 3,
    "service_id": 6
  }
]


ROUND_TIME = 60*1000
service_names = ["pool", "capter", "electrohub", "fooddispenser", "redbutton", "settings", "stargate"]
team_names = ["Honeypot", "Переподвысмотрит", "BSUIR", "Bushwhackers", "cookie@venice", "[censored]", "ENOFLAG",
              "Espacio", "girav", "keva", "LC↯BC", "Lights Out", "saarsec", "Shadow Servants", "SiBears",
              "TeamSpin", "VoidHack", "Tower Of Hanoi", "WE_0WN_Y0U", "Destructive Voice", "Гостевая 1",
              "Гостевая 2", "MSHP SSL: The Elite Firm", "Invisible"]
flags_i = 0



def team_(x): return x + 1
def service_(x): return x + 1

def gtime(): return int(time()*1000)
def cround(): return (gtime() - start)//ROUND_TIME + 1

connected = set()


@route('/<filepath:path>')
def main_page(filepath):
    response = static_file(filepath, root='./')
    response.set_header("Cache-Control", "no-cache")
    return response


def tojson(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        response.content_type = 'application/json'
        return fn(*args, **kwargs)

    return wrapper


@route('/api/info')
@tojson
def info_page():
    return {
        'teams': {team_(i): team_names[i] for i in range(args.teams)},
        'services': {service_(i): service_names[i] for i in range(args.services)},
        'start': 0
    }


@route('/api/scoreboard')
@tojson
def scores_page():
    return {
        'table': scores,
        'status': '1',
        'round': cround()
    }


def update_events():
    last_upd = events[-1][1] if events else start
    current = gtime()

    for x in range(args.frequency*((current - last_upd)//1000)):
        attacker = random.randint(0, args.teams - 1)
        victim = attacker
        while victim == attacker:
            victim = random.randint(0, args.teams - 1)

        evt_time = int(last_upd + (x/args.frequency)*1000)
        events.append([
            (evt_time - start)//ROUND_TIME + 1,
            evt_time,
            service_(random.randint(0, args.services - 1)),
            team_(attacker), team_(victim)
        ])
        scores[team_(attacker)] += 1



@route('/scoreboard.json')
@tojson
def scoreboard_page():
    return {
        "round": cround(),
        "scoreboard": [
            {
                "name": team_names[t],
                "score": str(scores[team_(t)]) + ".12",
                "services": [
                    {
                        "flags": cround()*2 + 1,
                        "status": random.choice((101, 102, 103, 104, 110)),
                        "id": service_(s)
                    }
                    for s in range(args.services)
                ]
            }
            for t in range(args.teams)
        ]
    }


async def websockets_handler(websocket, path):
    global connected, start ,flags_i
    connected.add(websocket)
    start = gtime()
    flags_i = 0
    await create_state()
    await create_start()
    while True:
        await asyncio.sleep(1)
        if websocket not in connected:
            break


async def write_to_websocket(text):
    for ws in connected.copy():
        try:
            await ws.send(text)
        except:
            connected.remove(ws)



def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--teams', type=int, help='teams count',
                        default=24)
    parser.add_argument('-s', '--services', type=int, help='services count',
                        default=7)
    parser.add_argument('-q', '--frequency', type=int, help='attack frequency',
                        default=30)
    return parser.parse_args()


def websocket_server_run():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(websockets_handler, '0.0.0.0', 8080)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    asyncio.ensure_future(create_states(), loop=loop)
    asyncio.ensure_future(create_attacks(), loop=loop)
    loop.run_forever()

async def create_start():
    event = {
        "type": "start",
    }
    json_str = json.dumps(event)
    await write_to_websocket(json_str)

async def create_attacks():
    global flags, start, flags_i
    step = 10  # ms
    while True:
        while flags_i < len(flags) and flags[flags_i]["ts"] * 1000 - start_time * 1000 < gtime() - start:
            event = {
                "type": "attack",
                "value": {
                    "service_id": flags[flags_i]["service_id"],
                    "attacker_id": team_(flags[flags_i]["attacker_id"]),
                    "victim_id": team_(flags[flags_i]["victim_id"])
                }
            }
            json_str = json.dumps(event)
            await write_to_websocket(json_str)
            flags_i += 1
        await asyncio.sleep(step/1000)

async def create_states():
    while True:
        await asyncio.sleep(10)
        await create_state()


async def create_state():
    update_events();
    container = {
        "type": "state",
        "value": gen_state()
    }
    json_str = json.dumps(container)
    await write_to_websocket(json_str)


def gen_state():
    return {
        "round": cround(),
        "scoreboard": [
            {
                "name": team_names[t],
                "score": str(scores[team_(t)]) + ".12",
                "services": [
                    {
                        "flags": random.choice((1, 2, 3)),
                        "status": random.choice((101, 102)),
                        "id": service_(s)
                    }
                    for s in range(args.services)
                    ]
            }
            for t in range(args.teams)
            ]
    }


if __name__ == '__main__':
    args = parse_args()
    start = gtime()
    events = []
    scores = {team_(i): 0 for i in range(args.teams)}

    thread = threading.Thread(target=websocket_server_run)
    thread.start()

    run(host='0.0.0.0', port=8000, debug=True, reloader=False)
