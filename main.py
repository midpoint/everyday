from __future__ import annotations

import os

from my_function import (
    create_comment,
    get_bing_wallpaper,
    get_day,
    get_inspirational_quote,
    get_weather,
    send_dd,
    send_tg,
    World_60S,
)

CITY: str | None = os.environ.get("CITY")
DD_SIGN: str | None = os.environ.get("DD_SIGN")
DINGTALK_WEBHOOK: str | None = os.environ.get("DINGTALK_WEBHOOK")
LATITUDE: str | None = os.environ.get("LATITUDE")
LONGITUDE: str | None = os.environ.get("LONGITUDE")
TELEGRAM_BOT_TOKEN: str | None = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID: str | None = os.environ.get("TELEGRAM_CHAT_ID")
G_T: str | None = os.environ.get("G_T")
REPO_NAME: str | None = os.environ.get("REPO_NAME")
ISSUE_NUMBER: str | None = os.environ.get("ISSUE_NUMBER")


if __name__ == "__main__":
    weather = get_weather(LATITUDE, LONGITUDE)

    text = f"# 每日早报\n---\n- {get_day()}\n---\n## 今日天气\n"
    text += str(weather)

    wallpaper, wallpaper_title, wallpaper_copyright = get_bing_wallpaper()
    text += f"\n---\n## 每日美图\n![必应壁纸]({wallpaper})"
    if wallpaper_title:
        text += f"\n{wallpaper_title}"
    if wallpaper_copyright:
        text += f"\n{wallpaper_copyright}"
    text += "\n"

    text += f"\n---\n## 热点新闻 \n{World_60S()}"
    text += f"\n---\n## 励志语 \n{get_inspirational_quote()}"

    create_comment(G_T, REPO_NAME, ISSUE_NUMBER, text)

    send_dd(DINGTALK_WEBHOOK, DD_SIGN, text)
    send_tg(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, text)

