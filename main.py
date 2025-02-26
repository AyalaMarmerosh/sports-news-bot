import schedule
import time
from newsMail import get_sports_news, send_email

def job():
    news_list = get_sports_news()
    send_email(news_list)

schedule.every().day.at("12:10").do(job)  # קובע שליחה כל יום ב-08:00

while True:
    schedule.run_pending()
    time.sleep(60)
