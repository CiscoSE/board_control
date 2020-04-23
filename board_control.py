#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Board Control Console Script.

Copyright (c) 2020 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""

__author__ = "Eric Pylko"
__email__ = "erpylko@cisco.com"
__version__ = "1.0.0"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

from flask import Flask, request
from pyHS100 import SmartPlug
import json

#
# instantiate plug
#
PLUGIP="192.168.6.201"
plug=SmartPlug(PLUGIP)

#
# local IP address and port to listen on
#
HOSTIP="127.0.0.1"
HOSTPORT=6000

#
# turn off plug if starting up, just to have known state
#
plug.turn_off()
incoming = 0
hangups = 0
plugstatus = plug.state

# basic flask app starts here
app = Flask(__name__)

#
# In my use case, this is called from nginx. nginx is NOT a requirement
#
# This gets called every time data is PUT to the app. That's why we
# need global variables that are always available
#
@app.route('/',methods=['PUT'])
def control_kasa():
  global incoming
  global hangups
  global plugstatus

#
# This must be a new/first call, i.e. no calls on board
# so we want to store the state for what to do after
# one or more calls arrive
#
  if (incoming == hangups):
    plugstatus = plug.state

#
# app must have started while in a call, set state back to normal
#
  if (hangups > incoming):
    hangups = 0
    unanswered = 0
  
#
# get the data passed from nginx, take the value from the "Message" key
#
  req = request.get_json()["Message"]

#
# Current messages are Toggle, Answered, and Hangup. These are sent
# from the JS macro running on the board/codec
#
  if (req == "Toggle"):
    if (plug.state == "OFF"):
      plug.turn_on()
    else:
      plug.turn_off()
    return("200")
  elif (req == "Answered"):
    incoming += 1
  elif (req == "Hangup"):
    hangups += 1
  else:
    print ("Unhandled message: ", req)
    return("200")

# we have a new call, turn plug off
  if (incoming>hangups):
    plug.turn_off()
# must be a hangup, set state back to whatever it was when
# there were 0 calls. This also implies it ignores Toggle during a call
  else:
    plug.state = plugstatus
  return ("200")

if __name__ == '__main__':
  app.run(debug=False, host=HOSTIP, port=HOSTPORT)
