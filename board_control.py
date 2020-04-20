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
__version__ = "0.1.0"
__copyright__ = "Copyright (c) 2020 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

from flask import Flask, request
from pyHS100 import SmartPlug
import json
from dictor import dictor

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
# This gets called every time data is POSTed to the app. That's why we
# need global variables that are always available
#
@app.route('/',methods=['POST'])
def index():
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
# get the data passed from nginx as JSON
#
  req = request.get_json()

#
# Status.Call returns a JSON list, want to use it as a dict
#
# see different JSON messages in the examples directory
#
  state = dictor(req,'Status.Call')[0]
  
#
# The WebEx Board seems to send 3 messages for call status
#   - AnswerState - Unanswered
#   - AnswerState - Answered
#   - ghost - True (this is when a call is over) 
#
  if (dictor(state,'AnswerState.Value')=="Unanswered"):
    incoming += 1
  elif (dictor(state,'ghost')=="True"):
    hangups += 1
  elif (dictor(state,'AnswerState.Value')=="Answered"):
# we don't care if the call was answered
    return ("No change")
  else:
    return ("Error")
  
# we have a new call, turn plug off
  if (incoming>hangups):
    plug.turn_off()
# must be a hangup, set state back to whatever it was when
# there were 0 calls
  else:
    plug.state = plugstatus

#
  return ("Done")

if __name__ == '__main__':
  app.run(debug=False, host=HOSTIP, port=HOSTPORT)
