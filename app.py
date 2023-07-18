from flask import Flask, render_template, redirect
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

# ==== Webhook ====

@app.route('/discord_webhook', methods=['POST'])
def discord_webhook() -> dict:
    pass
   
# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT'))
