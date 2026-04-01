from __future__ import annotations

import os

from my_function import (
    create_comment,
    get_day,
    get_inspirational_quote,
    get_one_sentence,
    get_weather,
    make_pic,
    send_dd,
    send_tg,
    World_60S,
)

CITY: str | None = os.environ.get("CITY")
DD_SIGN: str | None = os.environ.get("DD_SIGN")
DINGTALK_WEBHOOK: str | None = os.environ.get("DINGTALK_WEBHOOK")
LATITUDE: str | None = os.environ.get("LATITUDE")
LONGITUDE: str | None = os.environ.get("LONGITUDE")
SENTENCE_API: str | None = os.environ.get("SENTENCE_API")
SENTENCE_TOKEN: str | None = os.environ.get("SENTENCE_TOKEN")
TELEGRAM_BOT_TOKEN: str | None = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID: str | None = os.environ.get("TELEGRAM_CHAT_ID")
G_T: str | None = os.environ.get("G_T")
REPO_NAME: str | None = os.environ.get("REPO_NAME")
ISSUE_NUMBER: str | None = os.environ.get("ISSUE_NUMBER")


if __name__ == "__main__":
    weather = get_weather(LATITUDE, LONGITUDE)

    text = f"# 每日早报\n---\n- {get_day()}\n---\n## 今日天气\n"
    text += str(weather)

    sentence1 = get_one_sentence(SENTENCE_API, SENTENCE_TOKEN)
    picurl = make_pic(sentence1)
    text += f"\n---\n## 一诗一图\n- {sentence1}\n![诗词图片]({picurl})\n"

    text += f"\n---\n## 热点新闻 \n{World_60S()}"
    text += f"\n---\n## 励志语 \n{get_inspirational_quote()}"

    create_comment(G_T, REPO_NAME, ISSUE_NUMBER, text)

    send_dd(DINGTALK_WEBHOOK, DD_SIGN, text)
    send_tg(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, text)

