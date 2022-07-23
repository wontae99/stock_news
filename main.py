import json
import requests
import datetime
import hashlib
import time

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
get_news = False
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_api_key = "5YCRSCVS600ZWZFJ"
news_api_key = "23a2490fab68420eab41e607669181a8"

# SMS API INFO
base_url = "https://api.onbuka.com/v3"
api_key = "TdZDL5fM"
api_pwd = "e09DtnCL"
appid = "mona99"


parameters_stock = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": stock_api_key,
    "datatype": "json"
}

response = requests.get(STOCK_ENDPOINT, params=parameters_stock)
response.raise_for_status()
stock_data = response.json()

today_date = datetime.date.today()


def n_day_before(n: int):
    cal_date = today_date - datetime.timedelta(n)
    return str(cal_date)


data21 = float(stock_data["Time Series (Daily)"][n_day_before(2)]["4. close"])
data20 = float(stock_data["Time Series (Daily)"][n_day_before(3)]["4. close"])

data_gap = abs(data21 - data20)
gap_per = round(data_gap / data20 * 100, 1)


def up_down():
    if data21 - data20 > 0:
        return "▲"
    elif data20 == data21:
        return "-"
    else:
        return "▼"


parameters_news = {
    "apikey": news_api_key,
    "language": "en",
    "q": COMPANY_NAME,
    "totalResults": 3
}
news_response = requests.get(NEWS_ENDPOINT, params=parameters_news)
news_response.raise_for_status()
news_data = news_response.json()["articles"][:2]

message_head = f"{COMPANY_NAME}: {up_down()}{gap_per}%\n\n"
message_body = [f'Headline: {article["title"]}\nBrief: {article["description"]}\n\n' for article in news_data]
message = message_head + message_body[0] + message_body[1]


# -------------------------------------------SMS ---------------------------------- #
def create_headers():
  timestamp = int(time.time())
  s = "%s%s%s" % (api_key, api_pwd, str(timestamp))
  sign = hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()

  headers = {
    'Content-Type': 'application/json;charset=utf-8',
    'Sign': sign,
    'Timestamp': str(timestamp),
    'Api-Key': api_key
  }

  return headers

headers = create_headers()

url = "%s/sendSms" % base_url

#post method
body = {"appId": appid, "numbers": "01054813943", "content": f"{message}", "senderId": ""}
print(body)

if gap_per >= 5:
    rsp = requests.post(url, json=body, headers=headers)
    if rsp.status_code == 200:
        res = json.loads(rsp.text)
        print(res)
# ----------------------------------------------------------------------------------------------#

