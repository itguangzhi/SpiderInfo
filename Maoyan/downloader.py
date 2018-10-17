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

# @File  : downloader.py
# @Author: huguangzhi
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com
# @ContactPhone : 13121961510
# @Date  : 2018-09-17 - 15:25
# @Desc  : 页面下载器
from random import random
from urllib.request import urlopen

import requests

from Maoyan.conf.infomation import Info


class Downloader:

    # 获取useragent信息
    def get_useragent(self):
        ua = Info.useragent(Info)
        useragent = random.choice(ua)
        return useragent

    menu_url = r'http://maoyan.com'
    cinemas_url = r'http://maoyan.com/cinemas'
    films_url = r'http://maoyan.com/films'
    ua = Info.useragent(Info)

    header = {  # 'User-Agent':random.choice(ua),
        'Cookie': '__mta=209427373.1539761301494.1539762952557.1539762961002.9; uuid_n_v=v1; _lxsdk_cuid=16680ece7b24-0009952abea1ba-36664c08-100200-16680ece7b4c8; uuid=F562ADF0D1DE11E88D04613460674A3D348BFA2AB0584371B57AE75E1D338156; _csrf=d3fdc5d651971c2768bb04be827b2fc01382497dbf53f1104a9334846d7ece0c; _lxsdk=F562ADF0D1DE11E88D04613460674A3D348BFA2AB0584371B57AE75E1D338156; __mta=108886845.1539762947396.1539762947396.1539762949099.2; _lxsdk_s=%7C%7C0',
        'Host': 'maoyan.com',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': 1
    }

    def get_response(self, link):

        try:
            response = requests.get(link, headers=self.header, allow_redirects=False)
            # response = urlopen(link).read()
            if response.status_code == 200:
                pageinfo = str(response, 'utf8').replace('\n', '')
                return pageinfo
            else:
                print(response.status_code)
                pass

        except:
            return self.get_response(link)

    # 打开影片信息页
    def movieResponse(self, movieID: str):
        url = 'https://piaofang.maoyan.com/movie/%s' % movieID
        HTMLpage = urlopen(url)
        page = HTMLpage.read().decode('utf-8')
        return page
