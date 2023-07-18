from flask import Flask, render_template, redirect, Response
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os
import time

load_dotenv()

app = Flask("Finance Notifier")


@app.route("/")
def home():
    # TODO: This should be a management website
    return redirect("/widget/tradingview_advanced_chart")


# ==== Widgets ====

widget_clip = {
    # Modify height to remove "Track all markets on TradingView"
    "tradingview_advanced_chart": {"x": 0, "y": 0, "width": 980, "height": 610 - 32}
}


@app.route("/widget/tradingview_advanced_chart")
def tradingview_advanced_chart():
    return render_template("tradingview_advanced_chart.html")


# ==== Capture ====


@app.route("/screenshot/<chart>")
async def screenshot(chart: str):
    """
    Basically this is what Chart-Img does
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        # TODO: pass parameters
        await page.goto(
            f'http://localhost:{os.getenv("PORT") if os.getenv("PORT") else 5000}/widget/{chart}',
            wait_until="networkidle",
        )
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
