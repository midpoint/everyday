from my_function import *

CAIYUN_KEY=os.environ.get("KLING_COOKIE")
CITY=os.environ.get("CITY")
DD_SIGN=os.environ.get("DD_SIGN")
DINGTALK_WEBHOOK=os.environ.get("DINGTALK_WEBHOOK")
LOCATION=os.environ.get("LOCATION")
SENTENCE_API=os.environ.get("SENTENCE_API")
SENTENCE_TOKEN=os.environ.get("SENTENCE_TOKEN")
TELEGRAM_BOT_TOKEN=os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID=os.environ.get("TELEGRAM_CHAT_ID")
ZHOYAN_API_KEY=os.environ.get("ZHOYAN_API_KEY")

if __name__ == "__main__":
    weather = get_weather(CAIYUN_KEY,CITY,LOCATION)
    print(weather)
    text=f'# 每日早报\n---\n## {CITY}天气\n'
    text=text+weather
    sentence1=get_one_sentence(SENTENCE_API,SENTENCE_TOKEN)
    print('sentence1:',sentence1)
    # picurl=make_pic(zhoyan_api_key,sentence1)
    picurl="https://sfile.chatglm.cn/testpath/be86d380-ee41-5aa9-a96d-2775cd12cd0e_0.png"
    print('picurl:',picurl)
    text=text+f'\n---\n## 每日一图\n{sentence1}\n'
    text=text+f'![{sentence1}]({picurl})'   #!['+sentence1+']('+picurl+')'
    print(text)

    send_dd(DINGTALK_WEBHOOK,DD_SIGN,text)
    # send_tg(telegram_bot_token,telegram_chat_id, sentence1,picurl)
