# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **每日早报 (Daily Morning Report)** automation project. It generates a daily report containing weather, news, Bing wallpaper, and inspirational quotes, then sends it to DingTalk and Telegram, and saves it to a GitHub Issue.

## Project Structure

- `main.py` — Entry point; orchestrates the pipeline
- `my_function.py` — All utility functions. Key lookup tables at module level: `WIND_FORCE_TABLE`, `DIRECTION_TABLE`, `WEATHER_STATUS` (WMO weather code mapping). Also contains `_markdown_to_html()` for Telegram HTML formatting.
- `requirements.txt` — Python dependencies
- `.github/workflows/GET UP.yml` — Runs daily at 22:00 Asia/Shanghai; also triggerable manually
- `m25.sh` — Local dev setup script (not used in CI)

## Running the Project

### Local Execution

```bash
pip install -r requirements.txt
# Set required environment variables (see README.md for full list)
# Required: CITY, LATITUDE, LONGITUDE, DD_SIGN, DINGTALK_WEBHOOK,
#           TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID,
#           G_T, REPO_NAME, ISSUE_NUMBER
python main.py
```

### GitHub Actions

The `GET UP` workflow runs daily at 22:00 (Asia/Shanghai) via cron. All secrets are configured in GitHub repository settings.

## Architecture

`main.py` imports all functions from `my_function.py` and orchestrates the pipeline:
1. Fetch weather from Open-Meteo API (free, no API key)
2. Fetch date info with lunar calendar via `cnlunar`
3. Fetch daily inspirational quote from iciba.com
4. Fetch Bing daily wallpaper (mkt=zh-CN for Chinese market)
5. Fetch news from viki.moe 60s API
6. Post to GitHub Issue (create_comment)
7. Send to DingTalk (send_dd) and Telegram (send_tg)

Environment variables are loaded from `os.environ.get()` at module level in `main.py` and passed as arguments to each function.

## Key Implementation Details

- Weather code mapping: `_weather_code_to_text()` maps WMO weather codes (0-99) to Chinese descriptions
- Wind force levels: `_get_wind_force_level()` maps wind speed (m/s) to Beaufort-scale labels
- Wind direction: `_get_direction()` maps degrees to cardinal directions (N, NE, E, SE, S, SW, W, NW)
- Markdown to Telegram HTML: `_markdown_to_html()` handles conversion for Telegram's HTML parse mode
- `get_bing_wallpaper()` forces Chinese market via `mkt=zh-CN` query parameter
