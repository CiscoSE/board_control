const xapi = require('xapi');

// Make sure HttpClient mode is on
xapi.config.set('HttpClient Mode', 'On');

// send the message in msg to the URL as PUT.
function sendmsg(msg) {
  var url = 'http://192.168.255.101/board';
  var headers = 'Content-Type: application/json';
  var command = '{"Message":"' + msg + '"}';
  xapi.command('HttpClient Put', {'URL':url, 'Header':headers }, command);
}

// A button with the ID 'kasa' was clicked. This is the button to
// toggle the kasa plug on and off
// It's using a case statement so other button actions can easily be added
xapi.event.on('UserInterface Extensions Panel Clicked', (event) => {
  switch(event.PanelId){
    case 'kasa':
      sendmsg("Toggle");
      break;
  }
});

// a call was answered
xapi.event.on('CallSuccessful', (event) => {
  sendmsg("Answered");
});

// a call was declined or hung up.
xapi.event.on('CallDisconnect', (event) => {
  sendmsg("Hangup");
});