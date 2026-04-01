from __future__ import annotations

import datetime
import json
from typing import Optional

import cnlunar
import requests
from PIL import Image
from PIL.Image import Image as PILImage
from github import Github
from telebot import TeleBot
from dingtalkchatbot.chatbot import DingtalkChatbot


# ============ 常量映射表 ============

WIND_FORCE_TABLE: list[tuple[float, str]] = [
    (0.3, "0级 无风"),
    (1.5, "1级 微风徐徐"),
    (3.3, "2级 清风"),
    (5.4, "3级 和风，树叶摇摆"),
    (7.9, "4级 树枝摇动"),
    (10.7, "5级 风力强劲"),
    (13.8, "6级 风力较强"),
    (17.1, "7级 风力超强"),
    (20.7, "8级 狂风大作"),
    (24.4, "9级 狂风呼啸"),
    (28.4, "10级 暴风毁树"),
    (32.6, "11级 暴风毁树"),
    (36.9, "12级 飓风"),
    (41.4, "13级 台风"),
    (46.1, "14级 强台风"),
    (50.9, "15级 强台风"),
    (56.0, "16级 超强台风"),
    (61.2, "17级 超强台风"),
    (float("inf"), "17+级 超超强台风"),
]

DIRECTION_TABLE: list[tuple[float, float, str]] = [
    (0.0, 22.5, "北"),
    (22.5, 67.5, "东北"),
    (67.5, 112.5, "东"),
    (112.5, 157.5, "东南"),
    (157.5, 202.5, "南"),
    (202.5, 247.5, "西南"),
    (247.5, 292.5, "西"),
    (292.5, 337.5, "西北"),
]

WEATHER_STATUS: dict[str, str] = {
    "CLEAR_DAY": "晴天",
    "CLEAR_NIGHT": "晴夜",
    "PARTLY_CLOUDY_DAY": "多云",
    "PARTLY_CLOUDY_NIGHT": "多云",
    "CLOUDY": "阴",
    "LIGHT_RAIN": "小雨",
    "MODERATE_RAIN": "中雨",
    "HEAVY_RAIN": "大雨",
    "STORM_RAIN": "暴雨",
    "FOG": "雾",
    "LIGHT_SNOW": "小雪",
    "MODERATE_SNOW": "中雪",
    "HEAVY_SNOW": "大雪",
    "STORM_SNOW": "暴雪",
    "DUST": "浮尘",
    "SAND": "沙尘",
    "WIND": "大风",
    "LIGHT_HAZE": "轻度雾霾",
    "MODERATE_HAZE": "中度雾霾",
    "HEAVY_HAZE": "重度雾霾",
}

DEFAULT_SENTENCE: str = (
    "赏花归去马如飞\r\n去马如飞酒力微\r\n酒力微醒时已暮\r\n醒时已暮赏花归\r\n"
)


# ============ 工具函数 ============

def _get_wind_force_level(wind_speed: float) -> str:
    for threshold, label in WIND_FORCE_TABLE:
        if wind_speed < threshold:
            return label
    return "17+级 超超强台风"


def _get_direction(angle: float) -> str:
    if angle < 0 or angle >= 360:
        return "无效的角度值"
    for start, end, label in DIRECTION_TABLE:
        if start <= angle < end or (end == 337.5 and angle >= 337.5):
            return label
    return "北"


# ============ 主要功能函数 ============

def get_inspirational_quote() -> str:
    """获取每日励志语"""
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"https://open.iciba.com/dsapi/?date={current_date}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return f"{data.get('content')}\n{data.get('note')}"
    except requests.RequestException as e:
        return f"无法获取励志语: {e}"


def World_60S() -> str:
    """获取60秒新闻简报"""
    url = "https://60s-api.viki.moe/v2/60s"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        formatted_json = json.loads(r.text)
        data = formatted_json.get("data", {})
        news_list = data.get("news", [])
        if not news_list:
            return "今日无新闻数据"
        return "\n".join([f"- {news}" for news in news_list]) + "\n"
    except requests.RequestException as e:
        return f"无法获取新闻 ({url}): {e}"


def create_comment(
    github_token: str,
    repo_name: str,
    issue_number: int | str,
    text: str,
) -> None:
    """在 GitHub Issue 下创建评论"""
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(int(issue_number))
    issue.create_comment(text)


def get_day() -> str:
    """获取今日日期信息（包含农历和节气）"""
    today = datetime.datetime.now()
    cntoday = cnlunar.Lunar(today, godType="8char")
    lines = [
        f"{today.year}年{today.month}月{today.day}日 {cntoday.weekDayCn}",
        f"- 农历：{cntoday.year8Char}【{cntoday.chineseYearZodiac}】年 "
        f"{cntoday.lunarMonthCn}{cntoday.lunarDayCn}日",
        f"- 今日节气：{cntoday.todaySolarTerms} / "
        f"下一节气：{cntoday.nextSolarTerm}  "
        f"{cntoday.nextSolarTermYear}{cntoday.nextSolarTermDate}",
    ]
    return "\n".join(lines) + "\n"


def get_one_sentence(
    sentence_api: str,
    sentence_token: Optional[str] = None,
) -> str:
    """获取一句古诗词"""
    headers = {}
    if sentence_token:
        headers["X-User-Token"] = sentence_token
    try:
        r = requests.get(sentence_api, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()["data"]["content"]
    except (requests.RequestException, KeyError, json.JSONDecodeError) as e:
        return DEFAULT_SENTENCE


def make_pic(sentence: str) -> str:
    """根据古诗词生成图片，返回图片URL或错误信息（使用 Pollinations.ai，免费无需 API key）"""
    import urllib.parse

    # Pollinations.ai 使用 Stable Diffusion，prompt 支持多语言
    encoded_prompt = urllib.parse.quote(sentence)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

    # 验证图片是否可访问（不下载，只检查返回）
    try:
        response = requests.get(image_url, timeout=30, allow_redirects=True)
        if response.status_code == 200 and len(response.content) > 1000:
            # 返回可访问的图片 URL
            return image_url
        else:
            return f"无法生成图片: HTTP {response.status_code}"
    except requests.RequestException as e:
        return f"无法生成图片: {e}"


def send_dd(dingtalk_webhook: str, dd_sign: str, message: str) -> None:
    """发送到钉钉"""
    dingtalk_bot = DingtalkChatbot(dingtalk_webhook, dd_sign)
    dingtalk_bot.send_markdown(title="每日早报", text=message)


def get_weather(latitude: str, longitude: str) -> str:
    """获取天气信息（使用 Open-Meteo API，无需 API key）"""
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ["temperature_2m", "relative_humidity_2m", "weather_code",
                    "wind_speed_10m", "wind_direction_10m"],
        "daily": ["temperature_2m_max", "temperature_2m_min", "uv_index_max"],
        "timezone": "Asia/Shanghai",
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()["current"]
        daily = response.json()["daily"]

        weather_code = data.get("weather_code", -1)
        weather_label = _weather_code_to_text(weather_code)
        wind_level = _get_wind_force_level(data.get("wind_speed_10m", 0))
        wind_direction = _get_direction(data.get("wind_direction_10m", 0))

        lines = [
            f"- 天气：{weather_label}",
            f"- 温度：{data.get('temperature_2m', 'N/A')}℃  "
            f"【{daily['temperature_2m_max'][0]}℃/{daily['temperature_2m_min'][0]}℃】",
            f"- 风力：{wind_level} / 风向：{wind_direction}",
            f"- 湿度：{data.get('relative_humidity_2m', 'N/A')}%",
            f"- 紫外线：{daily.get('uv_index_max', ['N/A'])[0]}",
        ]
        return "\n".join(lines) + "\n"
    except requests.RequestException as e:
        return f"无法获取天气信息: {e}"
    except (KeyError, json.JSONDecodeError) as e:
        return f"天气数据解析失败: {e}"


def _weather_code_to_text(code: int) -> str:
    """将 WMO 天气代码转换为中文描述"""
    mapping = {
        0: "晴天",
        1: "晴间多云",
        2: "多云",
        3: "阴天",
        45: "雾",
        48: "雾凇",
        51: "小毛毛雨",
        53: "中毛毛雨",
        55: "大毛毛雨",
        56: "冻毛毛雨",
        57: "强冻毛毛雨",
        61: "小雨",
        63: "中雨",
        65: "大雨",
        66: "冻雨",
        67: "强冻雨",
        71: "小雪",
        73: "中雪",
        75: "大雪",
        77: "雪粒",
        80: "小阵雨",
        81: "中阵雨",
        82: "大阵雨",
        85: "小阵雪",
        86: "大阵雪",
        95: "雷暴",
        96: "雷暴+小冰雹",
        99: "雷暴+大冰雹",
    }
    return mapping.get(code, f"未知({code})")


def send_tg(telegram_bot_token: str, telegram_chat_id: str, message: str) -> None:
    """发送到Telegram"""
    bot = TeleBot(telegram_bot_token)
    bot.send_message(chat_id=telegram_chat_id, text=message)
    
    
