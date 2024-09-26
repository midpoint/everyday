import os
from io import BytesIO
import requests
import json
import pendulum
from PIL import Image
import matplotlib.pyplot as plt
import telebot
from telebot import apihelper
from dingtalkchatbot.chatbot import DingtalkChatbot


def get_one_sentence(SENTENCE_API,SENTENCE_Token):
    DEFAULT_SENTENCE = (
    "赏花归去马如飞\r\n去马如飞酒力微\r\n酒力微醒时已暮\r\n醒时已暮赏花归\r\n"
)
    headers = {
    "X-User-Token": SENTENCE_Token
    }
    try:
        r = requests.get(SENTENCE_API,headers=headers)
        if r.ok:
            return r.json()["data"]["content"]
        else:
            return DEFAULT_SENTENCE
    except:
        print("get SENTENCE_API wrong")
        return DEFAULT_SENTENCE
def make_pic(zhoyan_api_key,sentence):
    from zhipuai import ZhipuAI
    client = ZhipuAI(api_key=zhoyan_api_key)
    response = client.images.generations(
        model ="cogview-3",#填写需要调用的模型名称
        prompt=sentence)
    return response.data[0].url

def send_dd(dingtalk_webhook,Dd_sign, message):
    # telegram_bot.send_photo(chat_id=telegram_chat_id, photo=image_url)
    dingtalk_bot = DingtalkChatbot(dingtalk_webhook,Dd_sign)
    dingtalk_bot.send_markdown(title='每日早报', text=message)

def get_weather(caiyun_key,city,location):
    # weather_status = {"PARTLY_CLOUDY_DAY":"多云（白天）","PARTLY_CLOUDY_NIGHT":"多云（夜间）","CLOUDY":"阴","LIGHT_HAZE":"轻度雾霾","MODERATE_HAZE":"中度雾霾","HEAVY_HAZE":"重度雾霾","LIGHT_RAIN":"小雨","MODERATE_RAIN":"中雨","HEAVY_RAIN":"大雨","STORM_RAIN":"暴雨","FOG":"雾",}
    weather_status = {
        'CLEAR_DAY': '晴天',
        'CLEAR_NIGHT': '晴夜',
        'PARTLY_CLOUDY_DAY': '多云',
        'PARTLY_CLOUDY_NIGHT': '多云',
        'CLOUDY': '阴',
        'LIGHT_RAIN': '小雨',
        'MODERATE_RAIN': '中雨',
        'HEAVY_RAIN': '大雨',
        'STORM_RAIN': '暴雨',
        'FOG': '雾',
        'LIGHT_SNOW': '小雪',
        'MODERATE_SNOW': '中雪',
        'HEAVY_SNOW': '大雪',
        'STORM_SNOW': '暴雪',
        'DUST': '浮尘',
        'SAND': '沙尘',
        'WIND': '大风',
        'LIGHT_HAZE': '轻度雾霾',
        'MODERATE_HAZE': '中度雾霾',
        'HEAVY_HAZE': '重度雾霾'
    }
    url = f"https://api.caiyunapp.com/v2.6/{caiyun_key}/{location}/weather"
    response = requests.get(url)
    data = response.json()
    if data['status'] == "ok":
        weather_info = data['result']['realtime']
        return f"- 天气：{weather_status[weather_info['skycon']]}\n- 温度：{weather_info['temperature']}℃\n- 体感温度：{weather_info['apparent_temperature']}℃\n- 风力：{weather_info['wind']['speed']}\n- 湿度：{weather_info['humidity']}\n- 能见度：{weather_info['visibility']}\n"
    else:
        return "无法获取天气信息"

def send_tg(telegram_bot_token,telegram_chat_id, caption,message):
    apihelper.proxy = {'https':'socks5://127.0.0.1:12334'}
    bot = telebot.TeleBot(telegram_bot_token)
    bot.send_message(chat_id=telegram_chat_id, text=caption)
    bot.send_photo(chat_id=telegram_chat_id, photo=message)
    
