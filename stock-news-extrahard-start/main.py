import requests
from twilio.rest import Client

STOCK = "AMZN"
COMPANY_NAME = "Amazon Inc"

API_STOCK_KEY = 'ECH1MDTKVV7B83XA'
OWN_STOCK = 'https://www.alphavantage.co/query'

API_NEWS_KEY = '07ffa0dfc414450e8cc573e69a14eeb8'
OWN_NEWS = 'https://newsapi.org/v2/everything'

TWILIO_ACCOUNT_SID = 'AC99a12b970f35bebe47e7f5cdd25b2b22'
TWILIO_AUTH_TOKEN = 'e485f20b700d619b7557a7b9b2882d4e'
TWILIO_PHONE_NO = '12184005996'

stock_params = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': API_STOCK_KEY,
}

stock_response = requests.get(OWN_STOCK, params=stock_params)
data = stock_response.json()['Time Series (Daily)']
stock_data = [value for (key, value) in data.items()]
yesterday_close = float(stock_data[0]['4. close'])
day_before_yesterday_close = float(stock_data[1]['4. close'])

print(f'yesterday: {yesterday_close}')
print(f'day before yesterday: {day_before_yesterday_close}')
change_in_price = (yesterday_close - day_before_yesterday_close)/yesterday_close
print(f'change: {change_in_price} %')

if abs(change_in_price) > .0001:
    news_params = {
        'qinTitle': COMPANY_NAME,
        'apiKey': API_NEWS_KEY,
    }
    news_response = requests.get(OWN_NEWS, params=news_params)
    articles = news_response.json()['articles']
    three_articles = articles[:3]

    formatted_articles = [f"Stock: {STOCK} *** change: {change_in_price} *** Headline: {article['title']}. \n***Brief: " \
                          f"{article['description']}"
                          for article in three_articles]

    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=TWILIO_PHONE_NO,
            to='+14388621036',
        )

