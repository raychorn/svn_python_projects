Name Server

Use the following command to start the Name Server in the background

nohup ./start-ns.sh &

Use a Cron job to keep the Name Server running - ignore all error messages from restart.

OR

Use Python script to check the process list to determine if there is a Name Server running and then take appropriate actions.

server caching methods:

1). Cache proactively - Grab all known objects up-front (aggresive).

2). Cache Most Used objects proactively - Track objects being requested based on usage patterns and pre-cache them.

3). Use memoized_duration object to cache objects fetched by server for 60 secs.