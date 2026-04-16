# 每日早报
## 运行例图

<img width="761" height="4575" alt="image" src="https://github.com/user-attachments/assets/1a496516-78e6-40c7-bb70-35ce83c22ac8" />


## 功能说明
- 显示当天日期信息（包括农历）
- 自动生成指定位置的天气情况
- 自动获取每日格言（iciba.com）
- 自动获取必应每日壁纸
- 自动获取每日热点新闻（viki.moe）
- 自动发送到钉钉和Telegram
- 自动保存结果到Issues的指定帖子中



## 变量设定
注意：要提前设置好需要的各种变量。
![变量设定](https://i.imgur.com/oYwZoT0.jpeg)

变量名|含义|举例
------|------|------
CITY|城市名（显示天气）|广州
LATITUDE|纬度（天气定位）|"22.627804"
LONGITUDE|经度（天气定位）|"113.466487"
DD_SIGN|钉钉签名|SEC*
DINGTALK_WEBHOOK|钉钉对话webhook|https://oapi.dingtalk.com/robot/send?access_token=*
TELEGRAM_BOT_TOKEN|tg机器人的token|*
TELEGRAM_CHAT_ID|tg对话ID|*
G_T|Github Token|*
REPO_NAME|项目名|midpoint/everyday
ISSUE_NUMBER|问题编号|1
