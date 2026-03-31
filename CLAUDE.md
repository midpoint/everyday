# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **每日早报 (Daily Morning Report)** automation project. It generates a daily report containing weather, news, classical Chinese poetry with AI-generated images, and inspirational quotes, then sends it to DingTalk and Telegram, and saves it to a GitHub Issue.

## Project Structure

- `main.py` — Entry point that orchestrates report generation and distribution
- `my_function.py` — All utility functions (weather, news, poetry, messaging, GitHub integration)
- `requirements.txt` — Python dependencies
- `m25.sh` — Environment setup script (sets Anthropic API credentials and launches Claude Code)

## Running the Project

### Local Execution

```bash
pip install -r requirements.txt
# Set required environment variables (see README.md for full list)
# Required: CAIYUN_KEY, CITY, LOCATION, DD_SIGN, DINGTALK_WEBHOOK, SENTENCE_API,
#           SENTENCE_TOKEN, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, ZHOYAN_API_KEY,
#           G_T, REPO_NAME, ISSUE_NUMBER
python main.py
```

### GitHub Actions

The `GET UP` workflow runs daily at 22:00 (Asia/Shanghai) via cron. All secrets are configured in GitHub repository settings.

## Architecture

`main.py` imports all functions from `my_function.py` and orchestrates the pipeline:
1. Fetch weather from Caiyun API
2. Fetch classical Chinese poetry from Jinrishici API
3. Generate image for poetry using Zhipu AI (cogview-4 model)
4. Fetch news from viki.moe 60s API
5. Fetch inspirational quote from iciba.com
6. Post to GitHub Issue
7. Send to DingTalk and Telegram

Environment variables are loaded from `os.environ.get()` in `main.py`, making the project configurable without code changes.
