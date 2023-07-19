# Finance Notifier

Periodically send webhook with stock or other finance feed summary.

This can do what Chart-Img can do, and it's free.

## Getting Started

```sh
pip install -r requirements.txt
playwright install

python app.py
# or
flask run
```

```sh
docker compose up --build
```

## Todo

- [X] Able to host TradingView widget
- [X] Able to take screenshot
- [X] Discord webhook
- [X] Able to pass HTTP GET parameter to create chart
- [X] Periodically trigger
- [X] Docker
- [ ] ~~Load config into `periodic/server.py`'s docker~~
- [ ] Try add indicators, strategies, studies on the TradingView Advanced Chart
- [ ] What if "click" the save image button on the TradingView Advanced Chart?

## Resources

- Discord Webhook
  - [lovvskillz/python-discord-webhook: execute discord webhooks](https://github.com/lovvskillz/python-discord-webhook)
- Information
  - [microsoft/playwright-python: Python version of the Playwright testing and automation library.](https://github.com/microsoft/playwright-python)
  - [pyppeteer/pyppeteer: Headless chrome/chromium automation library (unofficial port of puppeteer)](https://github.com/pyppeteer/pyppeteer)
  - [CHART-IMG | Capture Chart Image By API](https://chart-img.com/)
  - [Free Stock Widgets — Financial Web Components — TradingView](https://www.tradingview.com/widget/)
    - [Free Financial Chart Widget for Technical Analysis — TradingView](https://www.tradingview.com/widget/advanced-chart/)
    - [Technical Analysis Widget — Free and Powerful Tool — TradingView](https://www.tradingview.com/widget/technical-analysis/)
    - [Brokerage Integration to a Powerful Financial Platform — TradingView](https://www.tradingview.com/brokerage-integration/)
- Period Run
  - [schedule — schedule 1.2.0 documentation](https://schedule.readthedocs.io/en/stable/)
    - [dbader/schedule: Python job scheduling for humans.](https://github.com/dbader/schedule)
  - [python - How can I run an async function using the schedule library? - Stack Overflow](https://stackoverflow.com/questions/51530012/how-can-i-run-an-async-function-using-the-schedule-library)
  - [sched — Event scheduler — Python 3.11.4 documentation](https://docs.python.org/3/library/sched.html)
  - [threading — Thread-based parallelism — Python 3.11.4 documentation](https://docs.python.org/3/library/threading.html#timer-objects)
  - [Advanced Python Scheduler — APScheduler 3.9.1.post1 documentation](https://apscheduler.readthedocs.io/en/stable/index.html)
    - [agronholm/apscheduler: Task scheduling library for Python](https://github.com/agronholm/apscheduler)
  - [Flask APScheduler](https://viniciuschiele.github.io/flask-apscheduler/)
    - [viniciuschiele/flask-apscheduler: Adds APScheduler support to Flask](https://github.com/viniciuschiele/flask-apscheduler)

## Trouble Shooting

### pyppeteer (deprecated)

```txt
OSError: [WinError 14001] The application has failed to start because its side-by-side configuration is incorrect. Please see the application event log or use the command-line sxstrace.exe tool for more detail
```

- [Crash on running the example screenshot script from the documentation in VSCode Windows 10 · Issue #248 · pyppeteer/pyppeteer](https://github.com/pyppeteer/pyppeteer/issues/248)
  - If anyone is having this issue; what fixed it for me was to uninstall the python version downloaded from the windows store and install python directly from their webpage. After doing so, I was able to launch Chromium using Pyppeteer.
- [Can't run pyppeteer in local, or on web-based machine such as Replit · Issue #425 · pyppeteer/pyppeteer](https://github.com/pyppeteer/pyppeteer/issues/425)
  - longer updated. Check README.md for more info. You can use Playright instead.

### Scheduler API 404

- [python - Get list of all routes defined in the Flask app - Stack Overflow](https://stackoverflow.com/questions/13317536/get-list-of-all-routes-defined-in-the-flask-app)

```txt
$ flask routes
 * Ignoring a call to 'app.run()' that would block the current 'flask' CLI command.
   Only call 'app.run()' in an 'if __name__ == "__main__"' guard.
Endpoint                        Methods  Rule
------------------------------  -------  --------------------------------------
add_job                         POST     /scheduler/jobs
delete_job                      DELETE   /scheduler/jobs/<job_id>
discord_webhook                 GET      /discord_webhook
get_job                         GET      /scheduler/jobs/<job_id>
get_jobs                        GET      /scheduler/jobs
get_scheduler_info              GET      /scheduler
home                            GET      /
pause_job                       POST     /scheduler/jobs/<job_id>/pause
resume_job                      POST     /scheduler/jobs/<job_id>/resume
run_job                         POST     /scheduler/jobs/<job_id>/run
screenshot                      GET      /screenshot/<chart>
static                          GET      /static/<path:filename>
tradingview_advanced_chart      GET      /widget/tradingview_advanced_chart
tradingview_technical_analysis  GET      /widget/tradingview_technical_analysis
update_job                      PATCH    /scheduler/jobs/<job_id>
```

Seems if host is 0.0.0.0 will have some issue

Just because I am running an old one...
