# work in progress README

## CHANGELOG
ver 0.3
>add global_update_motion x(int)
>add global_update_motion information to /help
>reword /help message

ver 0.21
>refactor /update x(int) into /update_photo x(int)
>add simple logging.info() calls
>reword docstrings and refactor /help
>refactor remove_job_if_exists() to job_if_exists(..., remove=False)

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
Commands will be executed only if the current user id is in the custom_config.py file.

>/start - activate surveillance bot

>/debug - send debug information (current snapshot & current motion-movie)

>update_photo x(int) - every x seconds: send the last snapshot made by the motion program to current user.

>global_update_motion x(int) - every x seconds: check if a new motion-movie was made by the motion program. Send new movie to every authorised user then resume checks.

>/help - print this
