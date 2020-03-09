#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This is the main script. It will download world records from speedrun.com and megaman leaderboards,
    double check if its been published yet and if not, will publish to discord and twitter
"""
import tweeter
import discorder
import speedrun_dot_com_runs
import megaman_runs
import stored_values
import json
import datetime

def lambda_handler(event, context):
    run()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def run():
    # Script runs every half hour so even with a couple failures, double checking the last 3 hours is probably safe
    oldestDate = (datetime.datetime.utcnow() - datetime.timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%SZ')
    print("Checking for new Nes world records that haven't been posted that occurred after: " + oldestDate)

    # We fetch only recent SRC runs so we can let our records age out with a TTL
    print("Processing speedrun.com...")
    postWrs(speedrun_dot_com_runs.getNewWRs(oldestDate), True)
    print("Processing speedrun.com complete.")

    # Megaman leaderboards don't have dates for runs so we can't age out the record of publishing
    # This api is struggling lately so skip it
    #print("Processing megamanleaderboards.com...")
    #postWrs(megaman_runs.getWRs(), False)
    #print("Processing megamanleaderboards.com complete.")

def postWrs(wrs, withTTL):
    tweetCount = 0
    discordCount = 0

    for speedrun in wrs:
        try:
            if not stored_values.runWasAlreadyDiscorded(speedrun.runId):
                discorder.post(speedrun)
                stored_values.markRunAlreadyDiscorded(speedrun.runId, withTTL)
                discordCount += discordCount
        except Exception as err:
            print("Issue posting wr {} to discord with err: {}".format(speedrun, err))

        try:
            if not stored_values.runWasAlreadyTweeted(speedrun.runId):
                tweeter.tweet(speedrun)
                stored_values.markRunAlreadyTweeted(speedrun.runId, withTTL)
                tweetCount += tweetCount
        except Exception as err:
            print("Issue posting wr {} to twitter with err: {}".format(speedrun, err))

    print("Done posting {0} world records to twitter and {1} to discord.".format(tweetCount, discordCount))
