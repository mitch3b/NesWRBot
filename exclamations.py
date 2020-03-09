#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This util class will help pick an exclamation for posts.
"""
import math
import random

exclamations = [
  "Congratulations!",
  "Good Gracious!",
  "Holy Moly!",
  "Wowsers!",
  "I can't believe it!",
  "Did you hear?",
  "OMG!",
  "Are you kidding me?",
  "Good news everyone!"
];

def getExclamation():
    randomNumber = math.floor(random.random()*len(exclamations));

    return exclamations[randomNumber] + "! ";
