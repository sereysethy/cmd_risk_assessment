import json
from fastapi import FastAPI
from risk.assessment import RiskAssessment
from model import Payload

# Load config for the riks model
with open("config.json", "r") as fin:
    config = json.load(fin)

app = FastAPI()

risk_assessment = RiskAssessment(config)

@app.post("/cmds/risk")
async def get_risk(payload: Payload):

    result = risk_assessment.get_risk([payload.raw_cmd])

    return result