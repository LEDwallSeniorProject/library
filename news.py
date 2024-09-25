from matrix_library import canvas as c, shapes as s
from dotenv import load_dotenv
import os
import requests
import time

load_dotenv()

access_key = os.getenv("NEWS_ACCESS_KEY")

def get_news():
  response = requests.get(f"http://api.mediastack.com/v1/news?access_key={access_key}&languages=en")
  return response.json()

canvas = c.Canvas()

news = get_news()
news_index = 0
title = s.Phrase(news["data"][news_index]["title"], (0, 0), (255, 255, 255), size=2)
desc = s.Phrase(news["data"][news_index]["description"], (0, 128), (255, 255, 255), size=1, auto_newline=True)
background = s.Polygon(((0,0), (128, 0), (128, 16), (0, 16)), color=(0, 0, 0))


start_time = time.perf_counter()
while True:
  canvas.clear()
  
  if time.perf_counter() - start_time > 5:
    title.set_text(news["data"][news_index]["title"])
    desc.set_text(news["data"][news_index]["description"][:50]+"...")
    news_index = (news_index + 1) % len(news["data"])
    start_time = time.perf_counter()
  
  desc.translate(0, -1)
  if desc.position[1] < -128:
    desc.set_position([0, 128])
  canvas.add(desc)
  
  canvas.add(background)
  
  title.translate(-1, 0)
  if title.get_width() + title.position[0] < 0:
    title.set_position([128, title.position[1] % 128])
  canvas.add(title)
  
  canvas.draw()
  
  
  

