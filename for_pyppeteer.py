import asyncio
import pyppeteer
from dotenv import load_dotenv
import os

load_dotenv()

async def main(chart: str):
    browser = await pyppeteer.launch()
    page = await browser.newPage()
    await page.goto(f'http://localhost:{os.getenv("PORT") if os.getenv("PORT") else 5000}/{chart}')
    await page.screenshot({'path': f'{chart}.png'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main('tradingview_advanced_chart'))
