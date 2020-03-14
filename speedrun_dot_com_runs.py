#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is used to fetch recent world records from speedrun.com. It does some
    light filtering for categories/games that are dumb (in my opinion)
"""
import requests
import math
import time_to_string
from speedrun import Speedrun

batchSize = 20 # if you change this, you need to change the url to include a numResults
def getNewWRs(oldestDate) -> Speedrun:
    count = 0;
    result = []

    # Continue until we find a result that's older than older date or the count is less than 100 cos
    # Probably something is wrong
    while(len(result) < 100):
        response = _getJsonData("https://www.speedrun.com/api/v1/runs?platform=jm95z9ol&status=verified&orderby=verify-date&direction=desc&offset=" + str(count));

        print("processing src batch... " + str(count))

        for run in response:
            try:
                date = run["status"]["verify-date"]
                category = _getCategoryFromId(run["category"])

                if date is None:
                    raise RuntimeError("Run didn't have a date: " + playerJson);
                if category is None or "Lose" in category["name"] or category["miscellaneous"]:
                    continue #Don't process this, but move on to the next run
                elif date < oldestDate:
                    return result
                elif run["level"] is None: # only care about full game records
                    gameObj = _getGameFromId(run["game"])

                    if not gameObj["isCategoryExtensions"] and _isWorldRecord(run["game"], run["category"], run["id"]):
                        runId = run["id"]
                        runners = _parsePlayers(run["players"])
                        game = gameObj["name"]
                        time = time_to_string.fromTotalSeconds(run["times"]["primary_t"])
                        link = run["weblink"]
                        video = run["videos"]["links"][0]["uri"]

                        speedrun = Speedrun(runId, runners, game, category["name"], time, link, video)
                        print("Adding src gameid: " + run["game"] + ",  run: " + str(speedrun))
                        result.append(speedrun)
            except RuntimeError as err:
                # TODO: Currently just move on when this happens, but could silently fail for a long time for some game
                print("Parsing Error: {0} for run {1}".format(err, run))
        count += batchSize

    raise RuntimeError("Found more than 100 recent runs on speedrun.com. Chances are something went wrong...");

def _isWorldRecord(gameId, categoryId, runId):
    response = _getJsonData("https://www.speedrun.com/api/v1/leaderboards/" + gameId + "/category/" + categoryId + "?top=1")

    # Might be more than one if there's a tie for first
    for run in response["runs"]:
        if run["run"]["id"] == runId:
            return True

    return False

def _parsePlayers(playersJson):
    result = []

    if playersJson is None or len(playersJson) == 0:
        raise RuntimeError("Players json was none.");

    for playerJson in playersJson:
        if playerJson["rel"] == "guest":
            result.append(playerJson["name"])
        elif playerJson["rel"] == "user":
            result.append(_getPlayerFromId(playerJson["id"]))
        else:
            raise RuntimeError("Player json didn't have handled user type: " + playerJson);

    return result

def _getPlayerFromId(id):
    response = _getJsonData("https://www.speedrun.com/api/v1/users/" + id)

    result = response["names"]["international"]
    if result is None:
        raise RuntimeError("Couldn't find player from id: " + id)

    return result

# Useful to see what could be blacklisted (but not used in lambda)
def findWhatGamesHacks():
    offset = 0
    while(True):
        response = _getJsonData("https://www.speedrun.com/api/v1/games?platform=jm95z9ol&offset=" + str(offset))
        offset += 20
        # TODO this doesn't actually work so the script just ends up hanging at the end
        if response is None:
            return

        for game in response:
            if game["romhack"]:
                print('"' + game["id"] + '", #' + game["names"]["international"])


def _getGameFromId(id):
    response = _getJsonData("https://www.speedrun.com/api/v1/games/" + id)

    result = {}
    result["name"] = response["names"]["international"]
    result["isCategoryExtensions"] = "Category Extensions" in result["name"]

    if result is None:
        raise RuntimeError("Couldn't find game from id: " + id)

    return result

def _getCategoryFromId(id):
    response = _getJsonData("https://www.speedrun.com/api/v1/categories/" + id)
    
    result = {}
    result["name"] = response["name"]
    result["miscellaneous"] = response["miscellaneous"]

    if result is None:
        raise RuntimeError("Couldn't find category from id: " + id)

    return result

def _getJsonData(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise RuntimeError("Failed to get response from: " + url)

    return response.json()["data"]
