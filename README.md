# Finance Notifier

Periodically send webhook with stock or other finance feed summary.

## Getting Started

```sh
pip install -r requirements.txt

python app.py
```

## Resources

- Discord Webhook
  - [lovvskillz/python-discord-webhook: execute discord webhooks](https://github.com/lovvskillz/python-discord-webhook)
- Information
  - [microsoft/playwright-python: Python version of the Playwright testing and automation library.](https://github.com/microsoft/playwright-python)
  - [pyppeteer/pyppeteer: Headless chrome/chromium automation library (unofficial port of puppeteer)](https://github.com/pyppeteer/pyppeteer)
  - [CHART-IMG | Capture Chart Image By API](https://chart-img.com/)
- Period Run
  - [sched — Event scheduler — Python 3.11.4 documentation](https://docs.python.org/3/library/sched.html)
  - [threading — Thread-based parallelism — Python 3.11.4 documentation](https://docs.python.org/3/library/threading.html#timer-objects)

## Trouble Shooting

### pyppeteer

```txt
OSError: [WinError 14001] The application has failed to start because its side-by-side configuration is incorrect. Please see the application event log or use the command-line sxstrace.exe tool for more detail
```

- [Crash on running the example screenshot script from the documentation in VSCode Windows 10 · Issue #248 · pyppeteer/pyppeteer](https://github.com/pyppeteer/pyppeteer/issues/248)
  - If anyone is having this issue; what fixed it for me was to uninstall the python version downloaded from the windows store and install python directly from their webpage. After doing so, I was able to launch Chromium using Pyppeteer.
- [Can't run pyppeteer in local, or on web-based machine such as Replit · Issue #425 · pyppeteer/pyppeteer](https://github.com/pyppeteer/pyppeteer/issues/425)
  - longer updated. Check README.md for more info. You can use Playright instead.
