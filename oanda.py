import requests
import datetime as dt
from googleapiclient.discovery import build
from google.oauth2 import service_account
import json

SERVICE_ACCOUNT_FILE = 'micro-edge-343610-5fc7b9ba1f6a.json'
SCOPES = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
          "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = None
creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# The ID spreadsjeet
SAMPLE_SPREADSHEET_ID = "1IBhjsOUnPWqPfkScrSMZf4QOAt42CQXgXJaw3jaWPyo"
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()


start_time = '2024-07-14T00:00:00.00'
restart_time = start_time
end_time = '2024-07-28T00:00:00.00'

diff = dt.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f')-dt.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f')
diff_min = diff.total_seconds() / 60
print(diff_min)
conv_st = dt.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S.%f') + dt.timedelta(minutes=75) 
print(conv_st)
print(dt.datetime(1985, 4, 12, 23, 20, 50, 520000))
iterations = int(diff_min/5000)
print(iterations)

data = []

#for i in range(iterations):
if dt.datetime.strptime(restart_time, '%Y-%m-%dT%H:%M:%S.%f') < dt.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S.%f'):
    print('yes mon')
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer f715f4b860187c51c367dbd44c6bccf4-4411543d26b109a6f201426ab8395953',
}
params = {
    #'from': '2024-01-01T04:29:00.000000000Z+08:00',
    'from': start_time + '-04:00',
    'count': '3',
    'price': 'M',
    'granularity': 'M1',
}
response = requests.get('https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles', params=params, headers=headers)
print(response.json()['candles'])
print(response.json()['candles'][-1]['time'])
restart_time = response.json()['candles'][-1]['time']
restart_time =  restart_time.replace('000Z', '')
restart_time = dt.datetime.strptime(restart_time, '%Y-%m-%dT%H:%M:%S.%f') + dt.timedelta(minutes=1) 
restart_time = restart_time.isoformat('T')
print("restart"+str(restart_time))

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer f715f4b860187c51c367dbd44c6bccf4-4411543d26b109a6f201426ab8395953',
}
params = {
    #'from': '2024-01-01T04:29:00.000000000Z+08:00',
    'from': restart_time + '-04:00',
    'count': '3',
    'price': 'M',
    'granularity': 'M1',
}
response = requests.get('https://api-fxpractice.oanda.com/v3/instruments/EUR_USD/candles', params=params, headers=headers)
print(response.json()['candles'])

for candle in response.json()['candles']:
    candle['time'] = candle['time'].replace('000Z', '')
    candle['time'] = dt.datetime.strptime(candle['time'], '%Y-%m-%dT%H:%M:%S.%f') - dt.timedelta(minutes=240) 
    print(candle['time'])
    date_time = candle['time'].strftime("%Y-%m-%d %H:%M:%S")
    print("date and time:",date_time)
    entry = [candle['complete'], candle['volume'], date_time, candle['mid']['o'], candle['mid']['h'], candle['mid']['l'], candle['mid']['c']]
print(entry)


data.append(entry)
#

request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
    range="Sheet1!A1", valueInputOption="USER_ENTERED", body={"values":data}).execute()