import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_VANTAGE_API = "alpha_vantage_api"
NEWS_API = "news_api"
account_sid = "account_sid"
auth_token = "auth_token"


def get_stock_difference():
    alpha_vantage_endpoint = "https://www.alphavantage.co/query"
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": STOCK,
        "apikey": ALPHA_VANTAGE_API,
    }
    stocks_response = requests.get(url=alpha_vantage_endpoint, params=stock_params)
    stocks_response.raise_for_status()
    stock_data = stocks_response.json()

    most_recent_stock_data = list(stock_data['Time Series (Daily)'].items())[0]
    most_recent_closing_value = most_recent_stock_data[1]["4. close"]

    second_most_recent_stock_data = list(stock_data['Time Series (Daily)'].items())[1]
    second_most_recent_closing_value = second_most_recent_stock_data[1]["4. close"]

    stock_price_difference = float(most_recent_closing_value) - float(second_most_recent_closing_value)
    return stock_price_difference


def get_news():
    news_api_endpoint = "https://newsapi.org/v2/everything"
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API,
    }
    news_response = requests.get(url=news_api_endpoint, params=news_params)
    news_response.raise_for_status()
    news_data = news_response.json()
    articles = []
    for news_article in range(3):
        articles.append(news_data["articles"][news_article])
    return articles


def create_message(news_article, stock_price_difference):
    stock_name = STOCK
    if stock_price_difference > 0:
        arrow = "🔺"
    else:
        arrow = "🔻"
    percent_change = round(abs(stock_price_difference), 0)
    title = f"{stock_name}:  {arrow}{percent_change}%"
    headline = f"Headline: {news_article['title']}"
    brief = f"Brief: {news_article['description']}"
    message = f"{title}\n{headline}\n{brief}\n"
    return message


def send_message(message):
    client = Client(account_sid, auth_token)
    client.messages.create(
            body=message,
            from_="from_phone_number",
            to="to_phone_number"
        )


stock_change = get_stock_difference()
if abs(stock_change) > 5:
    news_articles = get_news()
    for article in range(len(news_articles)):
        send_message(create_message(news_articles[article], stock_change))
