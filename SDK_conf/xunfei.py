#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
                            _ooOoo_  
                           o8888888o  
                           88" . "88  
                          (|  -_-  |)  
                           O\  =  /O  
                        ____/`---'\____  
                      .   ' \\| |// `.  
                       / \\||| : |||// \  
                     / _||||| -:- |||||- \  
                       | | \\\ - /// | |  
                     | \_| ''\---/'' | |  
                      \ .-\__ `-` ___/-. /  
                   ___`. .' /--.--\ `. . __  
                ."" '< `.___\_<|>_/___.' >'"".  
               | | : `- \`.;`\ _ /`;.`/ - ` : | |  
                 \ \ `-. \_ __\ /__ _/ .-` / /  
         ======`-.____`-.___\_____/___.-`____.-'======  
                            `=---='  
  
         .............................................  
                  佛祖镇楼                  BUG辟易  
          佛曰:  
                  写字楼里写字间，写字间里程序员；  
                  程序人员写程序，又拿程序换酒钱。  
                  酒醒只在网上坐，酒醉还来网下眠；  
                  酒醉酒醒日复日，网上网下年复年。  
                  但愿老死电脑间，不愿鞠躬老板前；  
                  奔驰宝马贵者趣，公交自行程序员。  
                  别人笑我忒疯癫，我笑自己命太贱；  
                  不见满街漂亮妹，哪个归得程序员？ 
'''
# @File  : xunfei.py
# @Author: huguangzhi
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com 
# @ContactPhone : 13121961510 
# @Date  : 2018-08-29 - 11:02
# @Desc  :

import base64
import hashlib
import time

# -*- coding: utf-8 -*-
import requests

URL = "http://api.xfyun.cn/v1/service/v1/tts"
AUE = "raw"
APPID = ""
API_KEY = ""


def getHeader():
    curTime = str(int(time.time()))
    param = "{\"aue\":\"" + AUE + "\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"xiaoyan\",\"engine_type\":\"intp65\"}"
    paramBase64 = base64.b64encode(param)
    m2 = hashlib.md5()
    m2.update(API_KEY + curTime + paramBase64)
    checkSum = m2.hexdigest()
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APPID,
        'X-CheckSum': checkSum,
        'X-Real-Ip': '127.0.0.1',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header


def getBody(text):
    data = {'text': text}
    return data


def writeFile(file, content):
    with open(file, 'wb') as f:
        f.write(content)
    f.close()


r = requests.post(URL, headers=getHeader(), data=getBody("科大讯飞是中国最大的智能语音技术提供商"))
contentType = r.headers['Content-Type']
if contentType == "audio/mpeg":
    sid = r.headers['sid']
    if AUE == "raw":
        writeFile("audio/" + sid + ".wav", r.content)
    else:
        writeFile("audio/" + sid + ".mp3", r.content)
    print("success, sid = " + sid)
else:
    print(r.text)
