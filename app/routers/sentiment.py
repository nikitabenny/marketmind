from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.data.database import SessionLocal
from app.data.models import Stock
from pydantic import BaseModel
import yfinance as yf
import pandas as pd
import scipy
import torch

from transformers import pipeline


class SentimentOut(BaseModel):
    sentiment: float

class NewsOut(BaseModel):
    news: List[str]


pipe = pipeline("text-classification", model="ProsusAI/finbert")

from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")


router = APIRouter(prefix="/sentiment", tags=["Sentiment"])



#weighted average sentiment of a stock
@router.get("/{symbol}", response_model = SentimentOut)
def get_senti(symbol):
  ticker = yf.Ticker(symbol)

  final_sent = 0
  news_count = 0

  cleaned_news = []

  for news in ticker.news:
    #add title and summary seperately
    
    title = news["content"].get("title", None)
    if title:
      cleaned_news.append(title)

    summary =  news["content"].get("summary", None)
    if summary:
      cleaned_news.append(summary)


  preds = []
  preds_proba = []
  tokenizer_kwargs = {"padding": True, "truncation": True, "max_length": 512}

  for x in cleaned_news:
      news_count += 1
      with torch.no_grad():
          input_sequence = tokenizer(x, return_tensors="pt", **tokenizer_kwargs)
          logits = model(**input_sequence).logits
          scores = {
          k: v
          for k, v in zip(
              model.config.id2label.values(),
              scipy.special.softmax(logits.numpy().squeeze()),
          )
      }
      sentimentFinbert = max(scores, key=scores.get)
      probabilityFinbert = max(scores.values())

      if sentimentFinbert == 'positive':
        final_sent += probabilityFinbert
      if sentimentFinbert == 'negative':
        final_sent -= probabilityFinbert

  if news_count > 0:
    final_sent /= news_count

  else:
    final_sent = 0

  return{
   "sentiment": final_sent
  }


@router.get("/news/{symbol}", response_model=NewsOut)
def get_news(symbol):
  ticker = yf.Ticker(symbol)

  final_sent = 0
  news_count = 0

  cleaned_news = []

  for news in ticker.news:
    #add title and summary seperately
    
    title = news["content"].get("title", None)
    if title:
      cleaned_news.append(title)

    summary =  news["content"].get("summary", None)
    if summary:
      cleaned_news.append(summary)

  return{
    "news " : cleaned_news
  }