#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This class will post a speedrun to twitter.
"""
import tweepy
import exclamations
import stored_values

def tweet(speedrun):
    content = _getTweetString(speedrun)
    print("Posting this to twitter: " + content)

    config = stored_values.getConfig()["Twitter"]

    # authentication of consumer key and secret
    auth = tweepy.OAuthHandler(config["consumer_key"], config["consumer_secret"])

    # authentication of access token and secret
    auth.set_access_token(config["access_token"], config["access_token_secret"])
    api = tweepy.API(auth)

    # update the status
    api.update_status(status = content)

def _getTweetString(speedrun):
    people = speedrun.getRunnersAsString()

    return exclamations.getExclamation() + " " + people +  " got the world record in " + speedrun.game + " - " + speedrun.category + " with a time of " + speedrun.time + "! " + speedrun.link
