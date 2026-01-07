from app.model import ChatbotAssistant, get_stocks

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

assistant = ChatbotAssistant('app/intents.json', function_mappings={'stocks': get_stocks})
assistant.parse_intents()
assistant.load_model('app/chatbot_model.pth', 'app/dimensions.json')


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_message = request.message

    if user_message.lower() == "/quit":
        return {"reply": "Goodbye 👋"}

    bot_reply = assistant.process_message(user_message)

    return {"reply": bot_reply}


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True,host="0.0.0.0",port=8080)