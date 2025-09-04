from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from uuid import uuid4
import json, os, tomllib, subprocess
from .app import app

def ensure_dirs(appconf):
    os.makedirs(appconf["request_dir"], exist_ok=True)
    os.makedirs(appconf["result_dir"], exist_ok=True)


_config = None

def read_config(path):    
    global _config
    with open(path, "rb") as f:
         _config = tomllib.load(f)

@app.on_event("startup")
async def load_config():
    read_config(os.getenv('LG_CONFIG'))


@app.post("/{app_name}/submit")
async def submit(app_name: str, request: Request):

    if app_name not in _config["apps"]:
        raise HTTPException(404, "Unknown app")

    appconf = _config["apps"][app_name]
    ensure_dirs(appconf)

    data = await request.json()
    uid = str(uuid4())

    req_path = os.path.join(appconf["request_dir"], f"{uid}.json")
    with open(req_path, "w") as f:
        json.dump(data, f)

    # Optional hook
    hook = appconf.get("hook")
    if hook:
        args = [a.format(uuid=uid, request_file=req_path,
                         result_file=os.path.join(appconf["result_dir"], f"{uid}.json"))
                for a in hook["args"]]
        try:
            subprocess.Popen([hook["command"], *args])
        except Exception as e:
            # не валим весь сервис из-за хуков
            print(f"Hook failed: {e}")

    return {"uuid": uid}


@app.get("/{app_name}/tasks/result/{uuid}")
async def get_result(app_name: str, uuid: str):
    if app_name not in _config["apps"]:
        raise HTTPException(404, "Unknown app")

    appconf = _config["apps"][app_name]
    ensure_dirs(appconf)

    path = os.path.join(appconf["result_dir"], f"{uuid}.json")
    if not os.path.exists(path):
        raise HTTPException(404, "Result not found")

    with open(path) as f:
        data = json.load(f)
    return JSONResponse(content=data)
