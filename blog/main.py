from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

router = APIRouter()

router.mount("/static", StaticFiles(directory="blog/static"), name="static")

templates = Jinja2Templates(directory="blog/templates")

@router.get("/", response_class=HTMLResponse)
async def blog(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
