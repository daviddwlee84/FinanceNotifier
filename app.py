from flask import Flask, render_template, request, Response
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os
import time

load_dotenv()

app = Flask("Finance Notifier")


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# ==== Widgets ====

widget_clip = {
    # Modify height to remove "Track all markets on TradingView"
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


@app.route("/screenshot/<chart>", methods=["GET"])
async def screenshot(chart: str):
    """
    Basically this is what Chart-Img does
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        url = f'http://localhost:{os.getenv("PORT") if os.getenv("PORT") else 5000}/widget/{chart}'
        if request.args:
            url += "?" + "&".join(
                f"{key}={value}" for key, value in request.args.items()
            )
        await page.goto(url, wait_until="networkidle")
        # To make sure the content loaded
        time.sleep(1)
        image = await page.screenshot(clip=widget_clip.get(chart))
        await browser.close()

    return Response(image, headers={"Content-Type": "image/jpeg"})


# ==== Webhook ====


@app.route("/discord_webhook", methods=["POST"])
def discord_webhook() -> dict:
    pass


# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"))
