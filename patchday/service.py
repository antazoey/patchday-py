from fastapi import FastAPI
from patchday.types import Hormone, Site
from patchday.main import patchday

app = FastAPI()


@app.get("/hormones", response_model=list[Hormone])
def get_hormones():
    """
    Retrieve a list of your hormones.
    """
    return list(patchday.hormones)


@app.get("/sites", response_model=list[Site])
def get_sites():
    """
    Retrieve a list of your sites.
    """
    return list(patchday.sites)
