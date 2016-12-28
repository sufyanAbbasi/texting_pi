#!/bin/bash
json-server db.json --routes routes.json --static ../website/ --port 80 >> ./json-server.log 2>&1 </dev/null &
PID=$(pgrep -f -n "node")
printf "#!/bin/bash\nkill $PID" > stop_rest_server.sh
