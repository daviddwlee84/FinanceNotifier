from flask import Flask, render_template, request, Response
from playwright.async_api import async_playwright
from discord_webhook import DiscordWebhook
import yaml
import os
import time
import asyncio
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import utils


# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True
    SCHEDULER_API_PREFIX = "/scheduler"
    SCHEDULER_ENDPOINT_PREFIX = ""
    # BUG (solved): KeyError: 'JSONIFY_PRETTYPRINT_REGULAR'
    JSONIFY_PRETTYPRINT_REGULAR = True


# create app
app = Flask("Finance Notifier")
app.config.from_object(Config())

curr_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(curr_dir, "config.yml")

with open(CONFIG_FILE, "r") as fp:
    config = yaml.safe_load(fp)

# ==== Web Page ====


@app.route("/", methods=["GET"])
def home():
    return render_template(
        "index.html",
        jobs=scheduler.get_jobs(),
        tickers=utils.get_all_tradingview_tickers(),
    )


@app.route("/configure", methods=["GET", "POST"])
def configure():
    global config
    # Save config
    if request.method == "POST":
        yaml_code = request.data.decode("utf-8")

        # TODO: Add yaml syntax check
        with open(CONFIG_FILE, "w") as fp:
            fp.write(yaml_code)

        with open(CONFIG_FILE, "r") as fp:
            config = yaml.safe_load(fp)

    # Open config
    else:
        with open(CONFIG_FILE, "r") as fp:
            yaml_code = fp.read()

    return render_template("config.html", yaml_code=yaml_code)


# ==== Schedule ====

# initialize scheduler
scheduler = APScheduler(
    scheduler=BackgroundScheduler(timezone=os.getenv("TZ", "Asia/Taipei"))
)
scheduler.init_app(app)


# https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html#module-apscheduler.triggers.cron
# TODO: make this configurable
@scheduler.task("cron", id="discord_webhook", day="*", hour="09")
def call_discord_webhook():
    # Not sure if there is more elegant way, but since the discord_webhook is async function
    url = f'http://localhost:{os.getenv("PORT") if os.getenv("PORT") else 5000}/discord_webhook'
    response = requests.get(url)
    print(response, response.text)


scheduler.start()

# ==== Widgets ====

widget_clip = {
    # Modify height to remove "Track all markets on TradingView"
    # TODO: remove the copyright in the templates
    "tradingview_advanced_chart": {"x": 0, "y": 0, "width": 980, "height": 610 - 32},
    "tradingview_technical_analysis": {
        "x": 2,
        "y": 2,
        "width": 425 - 4,
        "height": 450 - 35.2,
    },
}


@app.route("/widget/tradingview_advanced_chart", methods=["GET"])
def tradingview_advanced_chart():
    symbol = request.args.get("symbol", "MSFT")
    interval = request.args.get("interval", "30")
    return render_template(
        "tradingview_advanced_chart.html", symbol=symbol, interval=interval
    )


@app.route("/widget/tradingview_technical_analysis", methods=["GET"])
def tradingview_technical_analysis():
    symbol = request.args.get("symbol", "NASDAQ:MSFT")
    interval = request.args.get("interval", "1D")
    return render_template(
        "tradingview_technical_analysis.html", symbol=symbol, interval=interval
    )


# ==== Capture ====


async def get_screenshot(chart: str, **kwargs):
    """
    Basically this is what Chart-Img does
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        url = f'http://localhost:{os.getenv("PORT") if os.getenv("PORT") else 5000}/widget/{chart}'
        if kwargs:
            url += "?" + "&".join(f"{key}={value}" for key, value in kwargs.items())
        await page.goto(url, wait_until="networkidle")
        # To make sure the content loaded
        time.sleep(5)
        image = await page.screenshot(clip=widget_clip.get(chart))
        await browser.close()

    return image


@app.route("/screenshot/<chart>", methods=["GET"])
async def screenshot(chart: str):
    image = await get_screenshot(chart, **request.args)
    return Response(image, headers={"Content-Type": "image/jpeg"})


# ==== Webhook ====


@app.route("/discord_webhook", methods=["GET"])
async def discord_webhook():
    # TODO: don't load setting here, should pass parameter here
    # but widget and symbol config is complex, we need a mapping
    for setting in config["discord"]:
        print(setting)
        for symbol in setting["symbols"]:
            webhook = DiscordWebhook(
                url=setting["webhook"], content=f"📨 Quick Summary of **{symbol}**"
            )
            images = await asyncio.gather(
                *[get_screenshot(chart, symbol=symbol) for chart in setting["widgets"]]
            )
            for i, image in enumerate(images):
                # webhook.add_file(file=image, filename=f"{chart}_{symbol}.png")
                webhook.add_file(file=image, filename=f"{symbol}_{i}.png")
            webhook.execute()
    # Must return something...
    # TypeError: The view function for 'discord_webhook' did not return a valid response. The function either returned None or ended without a return statement.
    return "Success"


# Run the Flask app

#  * Ignoring a call to 'app.run()' that would block the current 'flask' CLI command.
#    Only call 'app.run()' in an 'if __name__ == "__main__"' guard.
if __name__ == "__main__":
    # BUG: when set host to 0.0.0.0 will let /scheduler API failed (404)
    app.run(host="0.0.0.0", port=os.getenv("PORT"))
    # app.run()
