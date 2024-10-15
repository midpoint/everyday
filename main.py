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
G_T = os.environ.get("G_T")
REPO_NAME = os.environ.get("REPO_NAME")
ISSUE_NUMBER = os.environ.get("ISSUE_NUMBER")


if __name__ == "__main__":
    weather = get_weather(CAIYUN_KEY,LOCATION)
    
    text=f'# 每日早报\n---\n- {get_day()}\n---\n## 今日天气\n'
    text=text+str(weather)
    sentence1=get_one_sentence(SENTENCE_API,SENTENCE_TOKEN)
    
    picurl=make_pic(ZHOYAN_API_KEY,sentence1)
    text=text+f'\n---\n## 一诗一图\n- {sentence1}\n'
    text=text+f'![sentence1]({picurl})'   #!['+sentence1+']('+picurl+')'

    text=text+f'\n---\n## 热点新闻 \n{World_60S()}'
    
    create_comment(G_T,REPO_NAME,ISSUE_NUMBER,text)

    send_dd(DINGTALK_WEBHOOK,DD_SIGN,text)
    send_tg(TELEGRAM_BOT_TOKEN,TELEGRAM_CHAT_ID, text)
