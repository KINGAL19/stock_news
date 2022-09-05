import requests
import os
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

ALPHA_API_KEY = os.getenv('ALPHA_API_KEY')
STOCK_URL = 'https://www.alphavantage.co/query'

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
NEWS_URL = 'https://newsapi.org/v2/everything'


stock_parameters = {
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK,
    'apikey': ALPHA_API_KEY,
}

r = requests.get(STOCK_URL, params=stock_parameters)
data = r.json()["Time Series (Daily)"]

data_list = [value for key, value in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data['4. close']

day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data['4. close']

difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)


up_down = None
if difference > 0:
    up_down = '🔺'
else:
    up_down = '🔻'

diff_percent = round((difference / float(yesterday_closing_price)) * 100, 2)


if abs(diff_percent) > 5:

    news_parameters = {
        'apiKey': NEWS_API_KEY,
        'q': COMPANY_NAME,
        'searchIn': 'title'
    }

    print('Get news')
    r = requests.get(NEWS_URL, params=news_parameters)
    articles = r.json()['articles']
    three_articles = articles[:3]

    formatted_articles_list = [f'{STOCK}: {up_down}{diff_percent}%\nHeadline: {article["title"]}. \n' \
                               f'Brief: {article["description"]}'for article in three_articles]

    print(formatted_articles_list)

    account_sid = os.getenv('twilio_sid')
    auth_token = os.getenv('twilio_token')
    client = Client(account_sid, auth_token)


    for article in formatted_articles_list:
        message = client.messages \
                        .create(
                             body=article,
                             from_='',
                             to=''
                         )

    print(message.sid)




