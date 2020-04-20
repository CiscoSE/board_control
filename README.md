# Board Control

*Use HttpFeedback to send POST messages and take actions on it*

---

**ToDo's:**

 - Push config to WebEx board to setup the xCommand instead of having
    a user do it through a different interface

 - Try this with another web-controlled plug

---

## Motivation

I borrowed a WebEx Board from work during the COVID-19 pandemic and kept it
in my basement office. I have a small space heater to keep the room warm,
but the heater is a little noisy. I got tired of manually turning the heater
on and off every time a call came in.

I wrote this middleware to take HttpFeedback information from the WebEx
Board and turn off the plug if it's on, and turn the plug back on when
the call is over.

## Features

 - Turn on and off a TP-Link plug based on call status

 - Call from an existing web server or run stand-alone

## Technologies & Frameworks Used

This uses Python 3.x for the code of the application. Other packages:

 - nginx - I already had a web server at my house, so the WebEx Board sends
   commands to nginx which routes the data to Flask
 - dictor - a Python library to easily parse JSON
 - pyHS100 - a Python library for controlling TP-LINK Kasa plugs

**Cisco Products & Services:**

This was designed with a WebEx Board 55. I expect this will work with any
WebEx-registered endpoint such as a RoomKit, DX80, etc.

**Third-Party Products & Services:**

 - TP-Link Kasa HS-105 Plug - this is a network-enabled power plug with
   APIs to let you control power through a smartphone app or APIs.

**Tools & Frameworks:**

 - Flask - A lightweight web app framework used to take requests from nginx
 - pm2 - pm2 is a javascript process manager that also can manage Python
   apps. I use pm2 to have my middleware run at system boot as a daemon.

## Usage

For testing, start the app with: board_control.py

This runs in as a webapp listening on localhost port 6000. This lets the
app be called only from a web server already on the device. If you want
this to run on a different IP and port, change HOSTIP and HOSTPORT, and
make sure your xCommand points to the right IP address and port.

For starting at boot time, you can create your own startup script or use
pm2 (a javascript process manager app that works with both JS and Python)

## Installation

You must have admin access to your WebEx device. Use the following xCommand,
but substitute your server that will be running this app:
  - xCommand HttpFeedback Register FeedbackSlot:1 ServerUrl:http://192.168.255.101/board format:json expression[1]:/Status/Call/AnswerState

You can also use a different FeedbackSlot if 1 is already in use

Clone the board control repo. After cloning, do:

  pip install -r requirements.txt

to get the required packages installed.

When you are ready to run your app, specify your TP-Link plug info and
IP address/port the app will listen on, and then just run the app.

## Authors & Maintainers

Smart people responsible for the creation and maintenance of this project:

- Eric Pylko <erpylko@cisco.com>

## Credits

Thanks to Benjamin Pylko (https://github.com/brpylko) for pointing me in
the right direction with my first attempt at this with JavaScript and
the "express" package. The asynchronous aspects of JS and the HS100
library I used made me try it with Python.

Also thanks to GadgetReactor (https://github.com/GadgetReactor/pyHS100) for
the pyHS100 library/APIs

## License

This project is licensed to you under the terms of the [Cisco Sample
Code License](./LICENSE).
