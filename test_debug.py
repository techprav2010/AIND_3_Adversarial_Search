###############################################################################
#                    YOU DO NOT NEED TO MODIFY THIS FILE                      #
###############################################################################
import argparse
import logging
import math
import os
import random
import textwrap

from collections import namedtuple
from multiprocessing.pool import ThreadPool as Pool

from isolation import Isolation, Agent, play
from sample_players import RandomPlayer, GreedyPlayer, MinimaxPlayer
from my_custom_player import CustomPlayer

