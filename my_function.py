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
import datetime
import cnlunar
from github import Github


def World_60S():
    url='https://60s.viki.moe'
    txt=''
    r=requests.get(url)
    if r.ok:
        formatted_json = json.loads(r.text)
        # 将格式化的字符串分割成行，并返回一个列表
        for item in formatted_json["data"]:
            txt=txt+'- '+item+f" \n"

        return txt
    else:
        return "60s.viki.moe is not working" 
       

def create_comment(Github_token,repo_name,issue_number,text):
    g = Github(Github_token)
    repo = g.get_repo(repo_name)
    issue = repo.get_issue(int(issue_number))
    issue.create_comment(text)

def get_day():
    today = datetime.datetime.now()
    cntoday = cnlunar.Lunar(datetime.datetime.now(), godType='8char')  # 常规算法
    text=f'{today.year}年{today.month}月{today.day}日 {cntoday.weekDayCn} \n'
    text=text+f'- 农历：{cntoday.year8Char}【{cntoday.chineseYearZodiac}】年 {cntoday.lunarMonthCn}{cntoday.lunarDayCn}日\n'
    text=text+f'- 今日节气：{cntoday.todaySolarTerms} / 下一节气：{cntoday.nextSolarTerm}  {cntoday.nextSolarTermYear}{cntoday.nextSolarTermDate} \n'
    return text
    
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
    try:
        response = client.images.generations(
        model ="cogview-3",#填写需要调用的模型名称
        prompt=sentence)
        return response.data[0].url
    except Exception as e:
        return e

def send_dd(dingtalk_webhook,Dd_sign, message):
    # telegram_bot.send_photo(chat_id=telegram_chat_id, photo=image_url)
    dingtalk_bot = DingtalkChatbot(dingtalk_webhook,Dd_sign)
    dingtalk_bot.send_markdown(title='每日早报', text=message)

def get_weather(caiyun_key,location):
    url = f"https://api.caiyunapp.com/v2.6/{caiyun_key}/{location}/weather"
    def get_wind_force_level(wind_speed):
        if wind_speed < 0.3:
            return "0级 无风"
        elif wind_speed < 1.5:
            return "1级 微风徐徐"
        elif wind_speed < 3.3:
            return "2级 清风"
        elif wind_speed < 5.4:
            return "3级 和风，树叶摇摆"
        elif wind_speed < 7.9:
            return "4级 树枝摇动"
        elif wind_speed < 10.7:
            return "5级 风力强劲"
        elif wind_speed < 13.8:
            return "6级 风力较强"
        elif wind_speed < 17.1:
            return "7级 风力超强"
        elif wind_speed < 20.7:
            return "8级 狂风大作"
        elif wind_speed < 24.4:
            return "9级 狂风呼啸"
        elif wind_speed < 28.4:
            return "10级 暴风毁树"
        elif wind_speed < 32.6:
            return "11级 暴风毁树"
        elif wind_speed < 36.9:
            return "12级 飓风"
        elif wind_speed < 41.4:
            return "13级 台风"
        elif wind_speed < 46.1:
            return "14级 强台风"
        elif wind_speed < 50.9:
            return "15级 强台风"
        elif wind_speed < 56:
            return "16级 超强台风"
        elif wind_speed < 61.2:
            return "17级 超强台风"
        else:
            return "17+级  超超强台风"
    
    def get_direction(angle):
        if angle < 0 or angle >= 360:
            return "无效的角度值"
        elif angle < 22.5 or angle >= 337.5:
            return "北"
        elif angle < 67.5:
            return "东北"
        elif angle < 112.5:
            return "东"
        elif angle < 157.5:
            return "东南"
        elif angle < 202.5:
            return "南"
        elif angle < 247.5:
            return "西南"
        elif angle < 292.5:
            return "西"
        else:
            return "西北"
    
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
    
    try:
        response = requests.get(url)
        data = response.json()
        if data['status'] == "ok":
            weather_info_now = data['result']['realtime']
            weather_info_day = data['result']['daily']
            wind_level=get_wind_force_level(weather_info_now['wind']['speed'])
            wind_direction=get_direction(weather_info_now['wind']['direction'])
            text=f"- 天气：{weather_status[weather_info_now['skycon']]} 【{data['result']['forecast_keypoint']}】\n"
            text=text+f"- 温度：{weather_info_now['temperature']}℃  【{weather_info_day['temperature'][0]['max']}℃/{weather_info_day['temperature'][0]['min']}℃】\n"
            text=text+f"- 风力：{wind_level} / 风向：{wind_direction}\n"
            text=text+f"- 湿度：{weather_info_now['humidity']*100}%  / 能见度：{weather_info_now['visibility']}\n"
            text=text+f"- 空气：AQI：{weather_info_day['air_quality']['aqi'][0]['avg']['chn']} / PM2.5：{weather_info_day['air_quality']['pm25'][0]['avg']} \n"
            text=text+f"- 生活：紫外线{weather_info_day['life_index']['ultraviolet'][0]['desc']} / 洗车{weather_info_day['life_index']['carWashing'][0]['desc']} \n"
            return text
    except Exception as e:
        return f"无法获取天气信息:\n {e}"
        
def send_tg(telegram_bot_token,telegram_chat_id, message):
    bot = telebot.TeleBot(telegram_bot_token)
    bot.send_message(chat_id=telegram_chat_id, text=message)
    
    
