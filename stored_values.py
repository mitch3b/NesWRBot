#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This class is for everything specific to my instance. It holds:
      1. discord webhook url (fetching from s3 file)
      2. Twitter app credentials (fetched from the same s3 file)
      3. DynamoDB to keep track of previously published posts

    For running your own bot, you'll mostly have to change this file.
"""
import boto3
import datetime
import math
import json

dynamodb = boto3.resource('dynamodb')
wrsPostedTable = dynamodb.Table('WorldRecordsPosted')

# Used to store keys, etc
def getConfig():
    s3 = boto3.resource('s3')
    content_object = s3.Object('nes-world-records', 'AccountsConfig.json')
    file_content = content_object.get()['Body'].read().decode('utf-8')

    return json.loads(file_content)

def runWasAlreadyTweeted(runId):
    return __runWasAlreadyPosted(runId + "-Twitter")

def markRunAlreadyTweeted(runId, withTTL):
    __markRunAlreadyPosted(runId + "-Twitter", withTTL)

def runWasAlreadyDiscorded(runId):
    return __runWasAlreadyPosted(runId + "-Discord")

def markRunAlreadyDiscorded(runId, withTTL):
    __markRunAlreadyPosted(runId + "-Discord", withTTL)

def __runWasAlreadyPosted(runIdDashPlatform):
    response = wrsPostedTable.get_item(
        Key={
            'runIdDashPlatform': runIdDashPlatform
        }
    )

    if 'Item' not in response:
        return False

    return True

# If runs don't have a time associated with it (like Megaman), we don't want to
# age out the "published" record
def __markRunAlreadyPosted(runIdDashPlatform, withTTL):
    if withTTL:
        response = wrsPostedTable.put_item(
            Item={
                'runIdDashPlatform': runIdDashPlatform,
                'ttl': __getTTL()
            }
        )
    else:
        response = wrsPostedTable.put_item(
            Item={
                'runIdDashPlatform': runIdDashPlatform,
            }
        )

def __getTTL():
    timeRightNow = datetime.datetime.now()
    return math.floor((timeRightNow + datetime.timedelta(days=10)).timestamp())
