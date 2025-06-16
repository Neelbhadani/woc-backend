import os


class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/woc")
    SECRET_KEY = os.getenv("SECRET_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    BASE_URL = os.getenv("BASE_URL")