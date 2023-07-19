import schedule
import requests
import os
import time


def call_discord_webhook():
    # TODO: maybe discord_webhook can be a POST request (which we normally won't call it directly)
    #       and load config to send should be here
    url = f'http://localhost:{os.getenv("PORT") if os.getenv("PORT") else 5000}/discord_webhook'
    response = requests.get(url)
    print(response, response.text)


# TODO: the time should be able to config or added from website..?
# TODO: set timezone & set tag
schedule.every().day.at("09:00").do(call_discord_webhook)


print("Schedule running...")
# TODO: periodically list next jobs
print("Current jobs:")
print(schedule.get_jobs())
while True:
    schedule.run_pending()
    time.sleep(1)
