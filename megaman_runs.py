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

def getWRs() -> Speedrun:
    result = []

    result.extend(_getNewWRs(1))
    result.extend(_getNewWRs(2))
    result.extend(_getNewWRs(3))
    result.extend(_getNewWRs(4))
    result.extend(_getNewWRs(5))
    result.extend(_getNewWRs(6))

    return result;

def _getNewWRs(gameNum):
    url = "https://megamanleaderboards.net/api/records.php?game=" + str(gameNum)
    response = requests.get(url)
    if response.status_code != 200:
      raise Exception("Failed to get response from: " + url)

    result = []

    for record in response.json()["records"]:
        try:
            runId = str(record["id"])
            game = "Megaman " + str(record["game_id"])
            runners = [_getUsername(record["user_id"])]
            category = record["category"]
            time = _timeToString(record["time"])
            link = "https://megamanleaderboards.net/index.php?game=" + str(gameNum)
            video = record["video"]
            

            speedrun = Speedrun(runId, runners, game, category, time, link, video)
            print("Adding src gameid: " + str(gameNum) + ",  run: " + str(speedrun))
            result.append(speedrun)
        except Exception as err:
            # This is semi expected for a couple categories, but ok with skipping them
            print("Parsing Error: {0} for run {1}".format(err, record))

    return result

#lots of records are held by the same folks and this api is already flaky so save some calls
userCache = {}
def _getUsername(userId):
    if userId in userCache:
        return userCache[userId]

    url = "https://megamanleaderboards.net/api/users.php?user=" + str(userId)

    response = requests.get(url)
    if response.status_code != 200:
      raise Exception("Failed to get response from: " + url)

    user = response.json()["users"][0]["name"]
    userCache[userId] = user
    return user


def _timeToString(time):
    totalSeconds = math.floor(time/100)
    return time_to_string.fromTotalSeconds(totalSeconds)
