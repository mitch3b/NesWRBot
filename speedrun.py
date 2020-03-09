#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This class holds the fields required to post about a given speedrun.
"""
class Speedrun:
    def __init__(self, runId, runners, game, category, time, link):
        self.runId = runId
        self.runners = runners
        self.game = game
        self.category = category
        self.time = time
        self.link = link


    def __str__(self):
        return "[ runId: " + self.runId + ", runners: " + str(self.runners) + ", game: " + self.game + " , category: " + self.category + ", time:" + self.time + ", link:" + self.link + "]";

    def getRunnersAsString(self):
        people = self.runners[0]

        if len(self.runners) > 1:
            i = 1

            while i < (len(self.runners) - 1):
                people += ", " + self.runners[i]
                i += 1

            people += " and " + self.runners[i]

        return people
