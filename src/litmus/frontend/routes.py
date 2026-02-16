from fastapi import APIRouter, Request
from vibetuner import render_template


router = APIRouter()


@router.get("/")
async def index(request: Request):
    return render_template("index.html.jinja", request)
