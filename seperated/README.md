# Standalone Modules [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

In this folder is a bunch of standalone scripts

## websocket.py
This is a simple websocket server that can be used to call any file via LogiX.<BR>
N.B: Only use UTF-8 standard characters so emoji isn't supported

## ovr.py
This script is used to call OpenVR data about controller battery levels

# Requirements
* [Python 3.8.6](https://www.python.org/downloads/release/python-386/) Due to Bleak Requirements in Windows - Do not use versions higher
* Pip
* SimpleWebSocketServer
* pexpect
* bleak - Windows Only
* asyncio - Windows Only
* openvr - For SteamVR Stuff

# License
Copyright 2018 Christopher Brown.
[MIT Licensed](https://chbrown.github.io/licenses/MIT/#2018).
