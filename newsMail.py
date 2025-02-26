import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# הגדרות API
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
NEWS_API_URL = "https://newsapi.org/v2/everything"

# הגדרות מייל
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SENDER = "hyylhyyly@gmail.com"  # כתובת המייל השולח
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = "hyylhyyly@gmail.com"  # כתובת המייל המקבל


def get_sports_news():
    """מחזיר רשימה של כתבות ספורט מהשבוע האחרון"""
    today = datetime.today().strftime('%Y-%m-%d')
    week_ago = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    params = {
        "q": "sports",
        "from": week_ago,
        "to": today,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URL, params=params)
    articles = response.json().get("articles", [])

    if not articles:
        return ["לא נמצאו כתבות חדשות היום."]

    news_list = [f"<b>{article['title']}</b> - <a href='{article['url']}'>קרא עוד</a>" for article in articles[:10]]
    return news_list


def send_email(news):
    """שולח מייל עם רשימת כתבות הספורט מהשבוע האחרון"""
    msg = MIMEMultipart()
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg["Subject"] = "🏆 עדכון שבועי: חדשות ספורט מהשבוע האחרון"

    body = "<h2>הנה הכתבות הבולטות מהשבוע האחרון בתחום הספורט:</h2><ul>"
    body += "".join(f"<li>{item}</li>" for item in news)
    body += "</ul>"

    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        print("✅ המייל נשלח בהצלחה!")
    except Exception as e:
        print(f"❌ שגיאה בשליחת המייל: {e}")


if __name__ == "__main__":
    news_list = get_sports_news()
    send_email(news_list)
