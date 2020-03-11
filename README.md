# NesWRBot
Used to notify of Nes WR speedruns via twitter, discord, etc

## Overview
This will run periodically and look for new NES wrs from speedrun.com and Megaman leaderboards. It will then post this to discord and twitter.

To follow the tweets, you can find the twitter account here: https://twitter.com/NesWorldRecords
Or to get these via discord, reach out to me (I'm mitch3a on about every other platform)

For feature requests or to report bugs, feel free to ping me on any platform you can find me. Alternatively, you could:
* Submit an issue to this repo
* email me at:  [mitch3apps@gmail.com](mailto:mitch3apps@gmail.com?subject=Nes%20WR%20Bot)
* dm the twitter account

Donations not necessary. Chances are any funds would cover the aws account once the free tier runs out :) Or maybe convince me to do more projects like this.

[![Donate with PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_SM.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=7DZA9T6PVE3LL&item_name=Dev&currency_code=USD&source=url)

## How To
This code is setup to fetch recent speedrun data and post it various sources. It runs periodically. I used python 3.7 (in case using a different version creates any issues).

### Play with Speedrun.com api
```
pip3 install requests
git clone https://github.com/mitch3b/NesWRBot.git
cd NesWRBot
python
from speedrun_dot_com_runs import getNewWRs
getNewWRs()
```

### Run the full script locally
If you want to completely recreate this bot, first install some modules to run/test locally. Note: If you don't plan on integrating with AWS, you can skip 'boto3'

```
pip3 install requests
pip3 install tweepy
pip3 install boto3
git clone https://github.com/mitch3b/NesWRBot.git
cd NesWRBot
```

This code pulls config values from s3 (which you won't have access to because they're for my twitter/discord/etc). It also talks to dynamo to track post history. To get this to work, you'll mostly have to replace everything in 'stored_values.py' with your own functionality. See lambda section below on how to do this with just some config replacement.

Once you've accounted for stored_values.py, enter the python console, and run:
```
python
from bot import run
run()
```

### Setup your own bot in your own aws account
I'm actually going to skip a lot of this. It includes parts like setting up twitter and getting the dev keys, setting up a discord with webhooks, creating a lambda function with scheduled events. Its all honestly really straight forward but you'll have to consult their docs for those steps. Here are some tips I'm leaving in case I want to recreate it myself.

#### Setup a layer for the dependencies
If you install the dependencies with the rest of this code, it'll get super messy. So I built them into separate layer.
* Create a new folder.
* In this empty folder: mkdir python
* cd python
* (you might have to create a setup.cfg file whose only content is:
```
[install]
prefix=
```
* Install the dependencies to a local folder (no need for boto3 as it comes with lambda automagically)
 * pip3 install requests -t .
 * pip3 install tweepy -t .
* cd .. (so you now are in a folder with only a 'python' folder
* git archive -o function.zip @
* Create a layer in aws and upload this zip file.
* In your lambda function, add the layer relationship. You should now be able to reference tweepy and requests

#### Deploy code to lambda
To build/deploy the actual code, go into the code directory and (modify params depending on your function name):
```
git archive -o function.zip @
aws lambda update-function-code --function-name speedrunTweetBot --zip-file fileb://function.zip
```

## TODO
* Megaman - until the api is more stable, need to leave this off
* Code Deploy
* Handle some situations better (ie if someone tied the WR or beat their own, might want a slightly different message)
* Make discord (and maybe tweet) look nicer.
