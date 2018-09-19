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

from Maoyan.conf.infomation import Info


class Downloader:
    menu_url = r'http://maoyan.com'
    cinemas_url = r'http://maoyan.com/cinemas'
    films_url = r'http://maoyan.com/films'

    def get_response(self, link):
        # request = urllib.request.Request(link)
        # request.add_header('User-Agent', str(self.getUA(self)))
        # request.add_header('Cookie',
        #                    '__mta=248954552.1533172087368.1534732553267.1534733685746.25"; _lxsdk_cuid=164f82d7537c8-0f989cd149666d-51422e1f-100200-164f82d7537c8; uuid_n_v=v1; uuid=84AB523095F011E883FE1F23FDFD6ADB1819195A754C410281F6435BC0E4293D; _lxsdk=84AB523095F011E883FE1F23FDFD6ADB1819195A754C410281F6435BC0E4293D; _csrf=d8e8905256c16f10cbd4629efc693c1df7c2221b9e4b90901125f75d1abff9d1; __mta=248954552.1533172087368.1533806526342.1533880670342.22; theme=moviepro; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ci=140; __mta=248954552.1533172087368.1533880670342.1534754983897.23"; _lxsdk_s=165566fc902-2e-3cc-73b%7C%7C35')
        response = urlopen(link).read()
        pageinfo = str(response, 'utf8').replace('\n', '')
        return pageinfo

    # 获取useragent信息
    def get_useragent(self):
        ua = Info.useragent(Info)
        useragent = random.choice(ua)
        return useragent

    # 打开影片信息页
    def movieResponse(self, movieID: str):
        url = 'https://piaofang.maoyan.com/movie/%s' % movieID
        HTMLpage = urlopen(url)
        page = HTMLpage.read().decode('utf-8')
        return page
