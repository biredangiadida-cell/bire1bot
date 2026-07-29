from fastapi import FastAPI
from pydantic import BaseModel
from telegram import Bot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=BOT_TOKEN)
app = FastAPI()

class Student(BaseModel):
    name: str
    phone: str
    email: str

@app.get("/")
def home():
    return {"status": "ELBS API Running"}

@app.post("/register")
async def register(student: Student):
    text = f"""
📚 ELBS New Registration

👤 Name: {student.name}
📱 Phone: {student.phone}
📧 Email: {student.email}

Website irraa galmaa'e.
"""

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=text
    )

    return {
        "success": True,
        "message": "Registration received."
    }
