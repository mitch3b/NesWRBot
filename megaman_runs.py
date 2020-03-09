#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is incomplete. There's an issue with the megaman leaderboards api so until
    that is resolved, I'm leaving this unfinished.
"""
import requests
import json
import math
import time_to_string
from speedrun import Speedrun

def getWRs():
    result = []
    result.extend(getNewWRs(1))
    #result.extend(getNewWRs(2))
    #result.extend(getNewWRs(3))
    #result.extend(getNewWRs(4))
    #result.extend(getNewWRs(5))
    #result.extend(getNewWRs(6))
    return result;

def getNewWRs(gameNum):
    url = "http://megamanleaderboards.net/api/records.php?game=" + str(gameNum)
    response = requests.get(url)
    if response.status_code != 200:
      raise Exception("Failed to get response from: " + url)

    result = []

    for record in response.json()["records"]:
        try:
            runId = str(record["id"])
            game = "Megaman " + str(record["game_id"])
            runners = [getUsername(record["user_id"])]
            category = record["category"]
            time = timeToString(record["time"])
            link = record["video"]

            speedrun = Speedrun(runId, runners, game, category, time, link)
            print("Adding src gameid: " + str(gameNum) + ",  run: " + str(speedrun))
            result.append(speedrun)
        except Exception as err:
            # This is semi expected for a couple categories, but ok with skipping them
            print("Parsing Error: {0} for run {1}".format(err, record))

    return result

#lots of records are held by the same folks and this api is already flaky so save some calls
userCache = {}
def getUsername(userId):
    return "fakeUser" + st(userId)
    if userId in userCache:
        return userCache[userId]

    print("fetching username for id: " + userId)
    url = "http://megamanleaderboards.net/api/users.php?user=" + str(userId)

    response = requests.get(url)
    if response.status_code != 200:
      raise Exception("Failed to get response from: " + url)

    user = response.json()["users"][0]["name"]
    userCache[userId] = user
    return user


def timeToString(time):
    totalSeconds = math.floor(time/100)
    return time_to_string.fromTotalSeconds(totalSeconds)
