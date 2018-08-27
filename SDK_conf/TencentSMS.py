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
# @File  : TencentSMS.py
# @Author: huguangzhi
# @ContactEmail : huguangzhi@ucsdigital.com.com 
# @ContactPhone : 13121961510 
# @Date  : 2018-08-27 - 14:34
# @Desc  : 腾讯云短信接口SDK

from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError

appid = '1400120315'
appkey = ''
template_id = 171118
phone_numbers = ['15831833670']
sms_sign = 'Tremble'
# 当模板没有参数时，`params = []`，数组具体的元素个数和模板中变量个数必须一致，例如事例中templateId:5678对应一个变量，参数数组中元素个数也必须是一个
params = ["liyang"]  # 个人用户限制长度为12个字符

ssender = SmsSingleSender(appid, appkey)
try:
    result = ssender.send_with_param(86, phone_numbers[0],
                                     template_id, params, sign=sms_sign, extend="", ext="")  # 签名参数未提供或者为空时，会使用默认签名发送短信
except HTTPError as e:
    print(e)
except Exception as e:
    print(e)

print(result)
