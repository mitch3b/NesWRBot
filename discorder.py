#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This class is used to post speedruns to discord
"""
import requests
import stored_values
import exclamations

webhookUrl = stored_values.getConfig()["Discord"]["webhookUrl"]

def post(speedrun):
    content = getTweetString(speedrun)
    print("Posting this to discord: " + content)

    myobj = {'content': content}

    x = requests.post(webhookUrl, data = myobj)

    if x.status_code != 204 and x.status_code != 200:
        raise Exception("Failed to post with code {} to discord. Content: {}".format(x.status_code, content))

# Consider making this better: https://leovoel.github.io/embed-visualizer/
def getTweetString(speedrun):
    people = speedrun.getRunnersAsString()

    return exclamations.getExclamation() + " " + people +  " got the world record in " + speedrun.game + " - " + speedrun.category + " with a time of " + speedrun.time + "! " + speedrun.link
