from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from pymongo import MongoClient
import os

app = FastAPI()


MODEL_NAME = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
sentiment_analyzer = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)


mongo_client = MongoClient(os.getenv("MONGO_URL", "mongodb://mongo_service:27017/"))
db = mongo_client["sentiment_db"]
collection = db["results"]

class TextRequest(BaseModel):
    text: str

@app.post("/analyze")
def analyze_sentiment(request: TextRequest):
    result = sentiment_analyzer(request.text)[0]
    
    collection.insert_one({"text": request.text, "result": result})
    return {"text": request.text, "result": result}
