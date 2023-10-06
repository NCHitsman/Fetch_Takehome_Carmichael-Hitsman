# How To Run

1. Enter "cd .\Fetch_Takehome_Carmichael-Hitsman"
2. Enter "docker compose up -d --build" into the command line
3. Check logs to see results of examples:
    - If you are not using the Docker application enter "docker ps" in your command line followed by "docker logs -f {CONTAINER ID}" using the CONTAINER ID shown from the docker ps command.
    - If you are using the Docker application simply click on the container to view the logs.


Note: This is also set up to be a live sever. If you'd like you can test it via Postman following the instructions below.

## Server Testing:

1. Send a POST request to the URL "http://localhost:5005/receipts/process" with a JSON body following the receipt structure.
2. Use the uuid returned to send a GET request to the URL "http://localhost:5005/receipts/{replace_with_id}/points". This will return the points for the receipt matching the uuid.
