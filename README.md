# LaterGate
LaterGate - scandalously slow API.

What if your API needs 5min or hour or year to process request? Will browser or other HTTP client still wait for it? LaterGate is an HTTP API for long-running shell script.
Script should poll `request_dir`, and for each filename.json should process it, unlink and write results to filename.json in `result_dir`. Script should run in separate session (in tmux/screen session, or daemon or systemd service)

## Example basic config
~~~toml
[apps.myapp]
request_dir = ".tasks/myapp/request"
result_dir  = ".tasks/myapp/results"
~~~

## Hooks
Optionally, hooks could be defuned for app. Hook will be called after each new task submitted. Note: hook should be "notification" process which finishes quickly. 
~~~toml
[apps.myapp.hook]
command = "/tmp/notify.sh"
args = ["--id", "{uuid}", "--file", "{request_file}"]
~~~

## Usage:
~~~bash
# submit task (I use httpie for this)

$ http POST http://localhost:8901/adscr/submit a=1 b=2
HTTP/1.1 200 OK
content-length: 47
content-type: application/json
date: Fri, 05 Sep 2025 10:24:25 GMT
server: uvicorn

{
    "uuid": "ae04f62b-0d5a-4faf-b523-cd178ff343cd"
}


# we now have uuid, lets check results

$ http GET http://localhost:8901/adscr/result/ae04f62b-0d5a-4faf-b523-cd178ff343cd
HTTP/1.1 404 Not Found
content-length: 29
content-type: application/json
date: Fri, 05 Sep 2025 10:25:04 GMT
server: uvicorn

{
    "detail": "Result not found"
}

# not ready yet. Lets wait and then check again:

$ http GET http://localhost:8901/adscr/result/ae04f62b-0d5a-4faf-b523-cd178ff343cd 
JSON-response comes here
~~~