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

import logging

from Maoyan.conf import infomation
# @File  : modle.py
# @Author: huguangzhi
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com
# @ContactPhone : 13121961510
# @Date  : 2018-09-17 - 17:13
# @Desc  : 数据加载模型层
from Maoyan.execuater import SqlExecuate

SqlExecuate = SqlExecuate()
infomation = infomation.Info()

logging.basicConfig(
    level=logging.INFO,
    # format='[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
    format='[%(asctime)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S,%a',
    filename=infomation.logfilepath('info_path'),
    filemode='w'
)

class modle:
    # 获取全国影院链接地址方法（使用）
    def getcinemaslink(self):
        print('=========开始获取取全国影院链接地址=========')
        city_sql = 'SELECT DISTINCT city_id FROM maoyan_cinema_link ORDER BY city_id;'
        city_list = SqlExecuate.unexecSQL(city_sql)
        logging.debug('step 1 : exec sql ,result city_list :%s' % str(city_list))
        city_cinemalists = []
        for cityid in city_list:
            city_id = cityid[0]
            logging.debug('item city_id in citylist,is citylist[0],city_id:%s' % str(city_id))
            # print(city_id)
            cinemalist_city = "SELECT cinema_link FROM maoyan_cinema_link WHERE city_id = '%s'" % city_id
            cinemalist = SqlExecuate.unexecSQL(cinemalist_city)
            logging.debug('step 2 : exec sql ,result city_id = (%s) cinemalist :%s' % (str(city_id), str(cinemalist)))
            city_cinemalist = []
            for cinemalinks in cinemalist:
                cinemalinked = cinemalinks[0]
                city_cinemalist.append(cinemalinked)
            city_cinemalists.append(city_cinemalist)
        # 数据库中存在一部分没有连接，并且不记录在link表中的影院id
        cinemalinkNONE = "SELECT cinema_id FROM maoyan_cinema_info WHERE city_id IS NULL"
        cinemalinkID = SqlExecuate.unexecSQL(cinemalinkNONE)
        try:
            cinemalinkNONEList = []
            for cinemaid in cinemalinkID:
                cinema_id = cinemaid[0]
                cinemalink = 'http://maoyan.com/cinema/%s' % str(cinema_id)
                cinemalinkNONEList.append(cinemalink)

            city_cinemalists.append(cinemalinkNONEList)
        except:
            logging.info('数据库中没有连接为空的影院信息')
            pass
        logging.info('city_cinemalists:%s' % str(city_cinemalists))
        return city_cinemalists
