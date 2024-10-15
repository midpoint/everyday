# 每日早报
## 运行例图

![每日早报](https://i.imgur.com/lcUpkEC.jpeg)


## 功能说明
- 显示当天日期信息（包括农历）
- 自动生成指定位置的天气情况
- 自动获取古诗词并生成图片
- 自动获取每日热点新闻
- 自动发送到钉钉和tg
- 自动保存结果到Issues的指定帖子中



## 变量设定
注意：要提前设置好需要的各种变量。
![变量设定](https://i.imgur.com/oYwZoT0.jpeg)

变量名|含义|举例
------|------|------
CAIYUN_KEY|彩云天气API key|***
CITY|城市名（显示天气）|广州
LOCATION|经度纬度（定位天气）|"113.466487,22.627804"
DD_SIGN|钉钉签名|SEC*
DINGTALK_WEBHOOK|钉钉对话webhook|https://oapi.dingtalk.com/robot/send?access_token=*
SENTENCE_API|获取古诗词|https://v2.jinrishici.com/one.json
SENTENCE_TOKEN|古诗词api的token|* 可省略
TELEGRAM_BOT_TOKEN|tg机器人的token|*
TELEGRAM_CHAT_ID|tg对话ID|*
ZHOYAN_API_KEY|智谱清言的API|*
G_T|Github Token|*
REPO_NAME|项目名|midpoint/everyday
ISSUE_NUMBER|问题编号|1
