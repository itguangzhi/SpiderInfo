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
# @File  : sexy_img.py
# @Author: huguangzhi
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com 
# @ContactPhone : 13121961510 
# @Date  : 2018-08-27 - 18:34
# @Desc  :

from qcloud_image import CIUrls, CIFiles
from qcloud_image import Client

appid = 'APP_ID'
secret_id = 'SECRET_ID'
secret_key = 'SECRET_KEY'
bucket = 'BUCKET'
client = Client(appid, secret_id, secret_key, bucket)
client.use_http()
client.set_timeout(30)

# 单个或多个图片Url
print(client.porn_detect(
    CIUrls(['http://img.hb.aicdn.com/acad778fd13e9795c53ebae4689a41c07ff9e0bf1e8c0-6h13vX_fw658', ])))
# 单个或多个图片File
print(client.porn_detect(CIFiles(['./test.jpg', ])))
