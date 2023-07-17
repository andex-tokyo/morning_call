from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

# Twilioの認証情報を環境変数から取得します
account_sid = <sid>
auth_token = <twillio_token>
from_phone_number = <phone_number> # あなたのTwilio番号

# Slackの認証情報を環境変数から取得します
slack_token = <slack_token>
channel_id = <channel_id> # 通知を送りたいSlackのチャンネルID

# Twilioクライアントを作成します
client = Client(account_sid, auth_token)

# Slackクライアントを作成します
slack_client = WebClient(token=slack_token)

# 呼び出しを行いたい人々とその時間を定義します
# 時間はJSTで、各エントリは次の形式です：[時間（24時間形式）, 電話番号, 名前]
people_to_call = [
    # 呼び出しを行いたい人々とその時間を定義します
    # 時間はJSTで、各エントリは次の形式です：[時間（24時間形式）, 電話番号, 名前]
]

scheduler = BlockingScheduler()

def make_call(time, to_phone_number, name):
    try:
        call = client.calls.create(
            twiml=f'<Response><Play>https://64b16887ce0f533072f450c4--subtle-fenglisu-d94f5b.netlify.app/chanpon.mp3</Play></Response>',
            from_=from_phone_number,
            to=to_phone_number
        )
        slack_client.chat_postMessage(channel=channel_id, text=f'{name}に電話しました。時刻:{time} 電話番号: {to_phone_number}')
    except Exception as e:
        slack_client.chat_postMessage(channel=channel_id, text=f'{name}に電話失敗しました。時刻:{time} 電話番号: {to_phone_number} Error: {str(e)}')

# 各人とその時間に対してスケジュールされたジョブを追加します
for person in people_to_call:
    time, number, name = person
    hour, minute = map(int, time.split(':'))
    scheduler.add_job(make_call, 'cron', hour=hour, minute=minute, args=[time, number, name])

scheduler.start()
