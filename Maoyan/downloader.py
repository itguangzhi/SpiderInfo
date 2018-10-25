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
import time
from urllib import request

from fake_useragent import UserAgent

from Maoyan.conf.infomation import Info
from Maoyan.controller import controller

controller = controller()
Info = Info()

class Downloader:


    menu_url = r'http://maoyan.com'
    cinemas_url = r'http://maoyan.com/cinemas'
    films_url = r'http://maoyan.com/films'


    def get_response(self, link):

        db = controller.connectionDB('redis')

        try:
            proxy = db.rpop("proxies").decode('utf-8')
            req = request.Request(link)
            req.add_header('User-Agent', UserAgent().random)
            # 创建一个ProxyHandler对象
            proxy_support = request.ProxyHandler({'http': proxy})
            # 创建一个opener对象
            opener = request.build_opener(proxy_support)
            # 给request装载opener
            request.install_opener(opener)
            # 打开一个url
            try:
                response = request.urlopen(req, timeout=120)
                pageinfo = response.read().decode().replace('\n', '')
                # print(pageinfo)
                return pageinfo
            except:
                return self.get_response(link)
        except:
            time.sleep(Info.GetResponse_ErrorWait)
            return self.get_response(link)


    # 打开影片信息页
    def movieResponse(self, movieID: str):
        url = 'https://piaofang.maoyan.com/movie/%s' % movieID
        page = self.get_response(url)
        # print(page)
        return page

    def cityResponse(self):
        url = 'http://maoyan.com/ajax/cities'
        return self.get_response(self, url)
