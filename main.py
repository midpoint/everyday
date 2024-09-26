from my_function import *

if __name__ == "__main__":
    weather = get_weather(caiyun_key,city,location)
    print(weather)
    text=f'# 每日早报\n---\n## {city}天气\n'
    text=text+weather
    sentence1=get_one_sentence(SENTENCE_API,SENTENCE_Token)
    print('sentence1:',sentence1)
    # picurl=make_pic(zhoyan_api_key,sentence1)
    picurl="https://sfile.chatglm.cn/testpath/be86d380-ee41-5aa9-a96d-2775cd12cd0e_0.png"
    print('picurl:',picurl)
    text=text+f'\n---\n## 每日一图\n{sentence1}\n'
    text=text+f'![{sentence1}]({picurl})'   #!['+sentence1+']('+picurl+')'
    print(text)

    send_dd(dingtalk_webhook,Dd_sign,text)
    # send_tg(telegram_bot_token,telegram_chat_id, sentence1,picurl)