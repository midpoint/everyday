from my_function import *

CAIYUN_KEY=os.environ.get("CAIYUN_KEY")
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
    weather = get_weather(CAIYUN_KEY,LOCATION)
    # print(weather)
    text=f'# 每日早报\n- {get_day()}\n---\n## 今日天气[{CITY}]\n'
    text=text+str(weather)
    sentence1=get_one_sentence(SENTENCE_API,SENTENCE_TOKEN)
    # print('sentence1:',sentence1)
    picurl=make_pic(ZHOYAN_API_KEY,sentence1)
    # picurl="https://sfile.chatglm.cn/testpath/be86d380-ee41-5aa9-a96d-2775cd12cd0e_0.png"
    print('picurl:',picurl)
    text=text+f'\n---\n## 一诗一图\n{sentence1}\n'
    text=text+f'![]({picurl})'   #!['+sentence1+']('+picurl+')'
    # print(text)

    send_dd(DINGTALK_WEBHOOK,DD_SIGN,text)
    send_tg(TELEGRAM_BOT_TOKEN,TELEGRAM_CHAT_ID, text)
