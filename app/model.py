from typing import Union, List
from pydantic import BaseModel

class Payload(BaseModel):
    raw_cmd: str