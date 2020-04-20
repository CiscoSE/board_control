sample.json has the 3 different JSON messages from the WebEx board.

You can test them against this with curl.

The first message from the board:
curl -X POST -d @unans.json http://localhost:6000/ --header "Content-Type:application/json"

After a call is answered:
curl -X POST -d @ans.json http://localhost:6000/ --header "Content-Type:application/json"

When the call is hung up:
curl -X POST -d @ghost.json http://localhost:6000/ --header "Content-Type:application/json"
