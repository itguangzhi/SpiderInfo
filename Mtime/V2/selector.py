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
# @File  : selector.py
# @Author: huguangzhi
# @ContactEmail : huguangzhi@ucsdigital.com.com 
# @ContactPhone : 13121961510 
# @Date  : 2018-07-16 - 19:41
# @Desc  : ID选择器，区分不同业务的重要工具
import re
from urllib.request import urlopen
from Mtime.V2.connectionDB import SelectData


class selectID():
    # 数据来于网页即将上映的影片ID
    def getMtimeFultureID(self):
        commingRegionUrl = 'http://movie.mtime.com/comingsoon/'
        conmminRegin = urlopen(commingRegionUrl).read()

        # print(conmminRegin)

        coming = str(conmminRegin, encoding='utf-8')
        # 过滤只需要即将上映的内容
        regPage = r'<dl class="tab1" data-index="\d+" data-parent-name="tab1">(.*?)</dl>'
        ownpage = re.findall(regPage, coming)
        pagelist = []
        for i in ownpage:
            # 过滤获取影片URLID号
            reg = r'<a href="http://movie.mtime.com/(\d+)" target="_blank">.*?</a>'
            mid = re.findall(reg, i)
            pagelist.extend(mid)
            # movieID = eval(mid)
        return set(pagelist)

    # 当前正在上映影片的ID
    def getReleaseID(self, database='mysql',  releasetype=1):
        releaseSQL = "SELECT movie_id FROM spiderInc.`Mtime_movieinfo_page` WHERE releaseType='%s';" % str(releasetype)
        if database == 'mysql':
            IDlist = SelectData.selectmysql(SelectData, releaseSQL)
        elif database == 'sqlserver':
            IDlist = SelectData.selectsqlserver(SelectData, releaseSQL)

        return IDlist
