# work in progress README

bot ver 0.2

The project is based of https://habr.com/ru/post/341678/
This bot is based of https://github.com/python-telegram-bot/
python-telegram-bot/blob/master/examples/echobot.py
(using python-telegram-bot)

my_homepc surveillance monitor telegram bot

This bot is meant as a part of an exercise pet project that
performs functions of a home monitor. The project goal is to
use an old notebook repurposed as an experimental debian bullseye
server to utilise https://motion-project.github.io/ to setup
automatic webcam capture and motion detection for no hassle
"video monitoring" of some area e.g. my studio appartment.
python-telegram-bot.org is used to build telegram bot, that will
be acting as a remote front end and will run on an experimental
debian bullseye server.

## Usage
>/start

>/debug

>/help

>TO_DO /update x

## TEMP
### (TO_DO) ver 0.4
Add custom reply keyboard with /help, /update commands.

### (TO_DO) ver 0.3
In case motion is detected, for all authorised users send last captured video.

### (14.10) ver 0.2
For all registred users in the "valid user ids" file send current webcam snapshot every x sec.

>add /update x - display new settings information for all authorised users, then start sending current snapshot every x seconds. /update 0 to disable.

### (14.10) ver 0.11
Assess if the current user id is in a local custom_config file before sending any sensitive information. Print user id and error message otherwise. 

>edit /snapshot (now /debug) - send last snapshot made by motion program and last motion capture video recorded 

>update /help

### (13.10) ver 0.1
Assess if the current user id is in a SPECIAL_USERS constant before sending any sensitive information. Print user id and error message otherwise.

### (13.10) ver 0.0

>add /start - activate bot

>add /snapshot - send last snapshot made by the debianpc webcam

>add /help - send help message detailing available commands