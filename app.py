from flask import Flask, render_template, redirect, Response
import pyppeteer
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask('Finance Notifier')

@app.route('/')
def home():
    # TODO: This should be a management website
    return redirect('/tradingview_advanced_chart')

# ==== Widgets ====

@app.route('/tradingview_advanced_chart')
def tradingview_advanced_chart():
    return render_template('tradingview_advanced_chart.html')

# ==== Capture ====

@app.route('/screenshot/<chart>')
async def screenshot(chart: str):
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.goto(f'http://localhost:{os.getenv("PORT") if os.getenv("PORT") else 5000}/{chart}')
    await page.screenshot({'path': f'{chart}.png'})
    await browser.close()

    with open(f'{chart}.png', 'rb') as fp:
        image = fp.read()
    return Response(image, headers={'Content-Type': 'image/jpeg'})

# ==== Webhook ====

@app.route('/discord_webhook', methods=['POST'])
def discord_webhook() -> dict:
    pass
   
# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'))
