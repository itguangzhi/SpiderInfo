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


# @File  : parse.py
# @Author: huguangzhi
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com
# @ContactPhone : 13121961510
# @Date  : 2018-09-17 - 15:21
# @Desc  : 页面解析
import datetime
import json
import logging
import re

from Maoyan.conf.infomation import Info
from Maoyan.downloader import Downloader
from Maoyan.execuater import SqlExecuate

Downloader = Downloader()
SqlExecuate = SqlExecuate()
Info = Info()

logging.basicConfig(
    level=logging.INFO,
    # format='[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
    format='[%(asctime)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S,%a',
    filename=Info.logfilepath('info_path'),
    filemode='w'
)


class CinemaPares:
    '''
    影院信息解析
    '''
    def cinema_pares(self, pageinfo, link):
        '''
        获取影院服务信息,传入link只为了获取影院ID
        :param pageinfo: 请求的html页面
        :param link: 当前影院的url
        :return: 影院基础信息，字典的形式 cinemainfo
        '''
        cinemainfo = {}
        cinemaservicereg = r'<div class="cinema-brief-container">(.*?)<div class="cinema-map"'
        logging.info(re.findall(cinemaservicereg, pageinfo, re.M))
        cinemaservice = re.findall(cinemaservicereg, pageinfo, re.M)[0]
        cinemanamereg = r'<h3 class="name text-ellipsis">(.*?)</h3>'
        cinemaaddrreg = r'<div class="address text-ellipsis">(.*?)</div>'
        cinematelreg = r'<div class="telphone">电话：(.*?)</div>'
        cinema3Dglasstagreg = r'<span class="tag ">(.*?)</span>'
        cinema3Dglassreg = r'<p class="desc text-ellipsis" title="(.*?)">'
        cinemachildreg = r'<p class="desc text-ellipsis" title="(.*?)">'
        cinemaparkreg = r'<span class="tag park-tag">.*?<p class="desc text-ellipsis" title="(.*?)">'
        cinemainfo['cinema_id'] = str(link).split('/')[-1]
        cinemainfo['city_id'] = str(
            SqlExecuate.unexecSQL("SELECT city_id FROM maoyan_cinema_link WHERE cinema_link = '%s'" % link)[0][0])
        cinemainfo['cinema_link'] = link
        cinemainfo['cinema_name'] = re.findall(cinemanamereg, cinemaservice)[0]
        cinemainfo['cinema_address'] = re.findall(cinemaaddrreg, cinemaservice)[0]
        cinemainfo['cinema_tel'] = re.findall(cinematelreg, cinemaservice)[0]
        try:
            cinemainfo['cinema_service_3Dglasses_info'] = re.findall(cinema3Dglassreg, cinemaservice)[0]
        except:
            cinemainfo['cinema_service_3Dglasses_info'] = '-'
        try:
            cinemainfo['cinema_service_3Dglasses_by'] = re.findall(cinema3Dglasstagreg, cinemaservice)[0]
        except:
            cinemainfo['cinema_service_3Dglasses_by'] = '-'
        try:
            cinemainfo['cinema_service_child'] = re.findall(cinemachildreg, cinemaservice)[1]
        except:
            cinemainfo['cinema_service_child'] = '-'
        try:
            cinemainfo['cinema_service_park'] = re.findall(cinemaparkreg, cinemaservice)[0]
        except:
            cinemainfo['cinema_service_park'] = '-'
        # cinemainfo['creation_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cinemainfo['last_update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logging.debug('cinemainfo:%s' % str(cinemainfo))
        return cinemainfo

class ShowPares:
    '''
        排映信息解析
    '''
    def getcinemashowinfo(self, pageinfo):
        '''
        获取影院排期
        :param pageinfo: 影院解析的页面
        :return: 当前影院中的所有排期 字典类型 showlist
        '''
        showlist = []
        # 限制匹配范围
        showinforeg = r'<div class="container" id="app"(.*?)<div class="big-map-modal"'
        cinemashowinfo = str(re.findall(showinforeg, pageinfo, re.M)[0]).replace(' ', '')
        showinfolistsreg = r'<trclass(.*?)</tr>'
        showinfolist = re.findall(showinfolistsreg, cinemashowinfo)
        for showinfos in showinfolist:
            showinfo = {}
            showidreg = r'/xseats/(.*?)\?movieId=(.*?)&cinemaId=(.*?)"'
            showinfo['show_id'] = re.findall(showidreg, showinfos)[0][0]
            showinfo['movie_id'] = re.findall(showidreg, showinfos)[0][1]
            try:
                movie_name = SqlExecuate.unexecSQL("SELECT movie_name FROM maoyan_movie_info WHERE movie_id = '%s'" %
                                                   showinfo['movie_id'])[0][0]
                showinfo['movie_name'] = movie_name
                # print(movie_name)
            except:
                logging.warning('movie_name 没有获取到，当前影片ID为:%s' % str(showinfo['movie_id']))
                showinfo['movie_name'] = '-'

            showinfo['cinema_id'] = re.findall(showidreg, showinfos)[0][2]
            try:
                cinemaservicereg = r'<div class="cinema-brief-container">(.*?)<div class="cinema-map"'
                cinemaservice = re.findall(cinemaservicereg, pageinfo, re.M)[0]
                cinemanamereg = r'<h3 class="name text-ellipsis">(.*?)</h3>'
                cinema_name = re.findall(cinemanamereg, cinemaservice)[0]
                # cinema_name = DataSave.unexecSQL(DataSave, "SELECT cinema_name FROM maoyan_cinema_info WHERE cinema_id = '%s'" % showinfo['cinema_id'])[0][0]
                showinfo['cinema_name'] = cinema_name
                # print(cinema_name)

            except:
                cinema_name = SqlExecuate.unexecSQL(
                    "SELECT cinema_name FROM maoyan_cinema_info WHERE cinema_id = '%s'" % showinfo['cinema_id'])[0][0]
                showinfo['cinema_name'] = cinema_name
            else:
                logging.debug('cinema_name 直接通过网页获取成功，影院ID为%s，影院名为：%s' % (str(showinfo['cinema_id']), cinema_name))
                # showinfo['cinema_name'] = '-'
            showinfo['show_date'] = str(showinfo['show_id'])[:4] + '-' + str(showinfo['show_id'])[4:6] + '-' + str(
                showinfo['show_id'])[6:8]
            schedulreg = r'"begin-time">(.*?)</span><br/><spanclass="end-time">(.*?)散场</span></td><td><spanclass="lang">(.*?)</span></td><td><spanclass="hall">(.*?)</span>'
            showinfo['begin_time'] = re.findall(schedulreg, showinfos)[0][0]
            showinfo['end_time'] = re.findall(schedulreg, showinfos)[0][1]
            showinfo['language'] = re.findall(schedulreg, showinfos)[0][2]
            showinfo['hall'] = re.findall(schedulreg, showinfos)[0][3]
            showinfo['pos'] = '-'
            # showinfo['creation_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            showinfo['last_update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # logging.info("showinfo:%s" % str(showinfo))
            showlist.append(showinfo)
            logging.debug("showlist:%s" % str(showlist))
        return showlist

class MoviePares:
    '''
       影片信息解析
    '''
    def movie_pares(self, page, movieID: str):
        '''
        影片信息解析
        :param page: 影片页面
        :param movieID: 影片ID
        :return: 影片信息 字典类型 pageinfo
        '''
        pageinfo = {}
        pageinfo['movie_id'] = movieID
        movieREG = '<span class="info-title-content">(.*?)</span>'
        releasedateREG = r'<span class="score-info ellipsis-1">(.*?)</span>'
        pageinfo['movie_name'] = re.findall(movieREG, page)[0].replace('&quot;', '"')
        # 影片上映时间
        try:
            pageinfo['release_date'] = re.findall(releasedateREG, page)[0]
        except:
            pageinfo['release_date'] = '-'
        # 影片评分
        rating_numREG = '<span class="rating-num">(.*?)</span>'
        try:
            pageinfo['rating_num'] = re.findall(rating_numREG, page)[0]
        except:
            pageinfo['rating_num'] = '-'

        pageinfo['last_update_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
        emovieREG = '<span class="info-etitle-content">(.*?)</span>'
        try:
            pageinfo['movie_name_other'] = re.findall(emovieREG, page)[0].replace('&quot;', '"')
        except:
            pageinfo['movie_name_other'] = '-'

        logging.debug('movie_info:%s' % pageinfo)
        return pageinfo

class CityPares:
    '''
        城市信息解析更新
    '''
    def city_pares(self, page):
        city_dict = json.loads(page)['letterMap']
        city_list = []
        for citymap in city_dict:
            city_list.extend(city_dict[citymap])
            for i in city_dict[citymap]:
                cityinfo = {}
                cityinfo['city_id'] = i['id']
                cityinfo['city_name'] = i['nm']
                cityinfo['city_name_pinyin'] = i['py']
                if '' == i['nm']:
                    cityinfo['city_info_id'] = '-'
                else:
                    cityinfo['city_info_id'] = '-'
                city_list.append(cityinfo)

        return city_list
