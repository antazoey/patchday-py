from fastapi import FastAPI
from patchday.main import patchday
from patchday.schedule import HormoneSchedule

app = FastAPI()


@app.get("/schedules", response_model=list[HormoneSchedule])
def get_schedules():
    """
    Retrieve a list of your schedules.
    """
    return list(patchday.schedules)
