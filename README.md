# CherishWechatBot
CherishWechatBot 基于ItChat接口，以插件化的形式实现微信个人号的定制化功能。主要基于群，私聊的功能也可以实现。

## 警告
如果过度使用聊天机器人（怎么样算过度我也不知道，问腾讯），可能会被腾讯封网页版微信的接口（无法登录网页版微信，机器人自然也不能使用）。严重的甚至直接封号（可以通过申诉找回）

## 相关项目
* ItChat源码：[https://github.com/littlecodersh/ItChat](https://github.com/littlecodersh/ItChat)

* 鸭哥的bot：[https://github.com/grapeot/WechatForwardBot](https://github.com/grapeot/WechatForwardBot)

## 安装
项目支持Win和Linux。依赖的环境有python、mongodb等。Linux下，运行运行deploy文件夹内的deploy.sh文件，然后安装requirements.txt中的库

## 运行
如果以上安装都顺利的话，在命令行中执行“python3 -u main.py”将出现二维码，用微信扫描登录即可运行

## 功能
详细的功能列表查看src文件夹下help.png文件
* 成语接龙
* 对联模式
* 群成员信息统计
* 群聊天内容标签云
* 群聊天数统计
* 语音转文本
* 查看必应美图
* 调教模式
* 图灵对话
* 网易云歌词生成
* 消息防撤回
* 红包检测
* 群新成员检测


## 部分文件说明
1. utilities.py ResGroup变量设置了要响应机器人的群，避免在一些重要群造成打扰

2. BingText2Speech.py 中的apikey要填写自己的key才能使用

3. deploy文件夹内的chengyu.dat文件是用于成语接龙功能的mongodb数据，需导入数据库 

## 作者
* 微博 [http://weibo.com/zmqcherish](http://weibo.com/zmqcherish)
* 知乎 [https://www.zhihu.com/people/zmqcherish/](https://www.zhihu.com/people/zmqcherish/)

## 问题和建议
欢迎大家提出一些有意思的feature，共同学习