import logging
import json
from os import path
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from fastapi import FastAPI
from fastapi import Request
from risk.assessment import RiskAssessment
from model import Payload

logpath = path.join("/code/var/log", 'access.log')
logging.basicConfig(format='%(message)s', level=logging.INFO,
                    handlers=[
                        TimedRotatingFileHandler(logpath, when='midnight')
                    ])

# Load config for the riks model
with open("/code/src/config.json", "r") as fin:
    config = json.load(fin)

app = FastAPI()

risk_assessment = RiskAssessment(config)

@app.post("/cmds/risk")
async def get_risk(payload: Payload, request: Request):
    """
    GET risk level for the command contained in the payload.
    Params
    ------
        payload (Payload): payload contains the raw_cmd (str)
    Returns
    -------
        json object containing `risk_level`, `probability` and `embedding`
    """

    x_real_ip = request.headers.get('X-Real-IP')
    now = datetime.now().isoformat()

    result = risk_assessment.get_risk([payload.raw_cmd])

    # keep them in access log file
    cmd = {}
    cmd["date"] = now
    cmd["ip"] = x_real_ip
    cmd["input"] = payload.raw_cmd
    cmd["risk_level"] = result["risk_level"]
    cmd["probability"] = result["probability"]
    logging.info(json.dumps(cmd))

    return result
