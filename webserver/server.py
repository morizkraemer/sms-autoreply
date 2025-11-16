from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from helpers.shared_data import shared_data
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()


app.mount("/static", StaticFiles(directory="webserver/static"), name="static")

templates = Jinja2Templates(directory="webserver/templates")

@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={"message": shared_data.get_reply_message()}
            )

@app.post('/update-message', response_class=HTMLResponse)
async def update_message(message: str = Form(...)):
    shared_data.set_reply_message(message)
    return f"<html><body><h1>Message has been changed to \"{message}\"</h1><a href='/'>go back</a></body></html>"
