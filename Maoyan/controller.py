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
# @File  : controller.py
# @Author: huguangzhi
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com
# @ContactPhone : 13121961510
# @Date  : 2018-09-17 - 16:37
# @Desc  : 控制层
import datetime
import logging

import pymysql
import redis
import threadpool
from DBUtils.PooledDB import PooledDB

from Maoyan.conf.infomation import DatabaseInfo
from Maoyan.conf.infomation import Info

logging.basicConfig(
    level=logging.WARNING,
    format='[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
    # format='[%(asctime)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S,%a',
    # filename=Info.logfilepath(Info, 'warning_path'),
    # filemode='w'
)


class controller:
    # 线程池
    def threadpoolcontronl(self, some_callable, list_of_args, callback=None):
        poolsize = Info.threadinfo(Info)
        pool = threadpool.ThreadPool(poolsize)
        requests = threadpool.makeRequests(some_callable, list_of_args, callback)
        [pool.putRequest(req) for req in requests]
        pool.wait()

    def connectionDB(self, db):
        if db == 'mysql':
            # mysql连接池
            pool = PooledDB(
                pymysql,
                mincached=2,
                maxcached=5,
                maxshared=3,
                maxconnections=6,
                host=DatabaseInfo.mysql_host,
                port=DatabaseInfo.mysql_port,
                user=DatabaseInfo.mysql_user,
                passwd=DatabaseInfo.mysql_passwd,
                db=DatabaseInfo.mysql_database,
                charset=DatabaseInfo.mysql_charset
            )

            try:
                conn = pool.connection()
                # conn.cursor()
                return conn
            except Exception as e:
                logging.error('数据库获取连接失败，报错日志为：%s' % e)
        elif db == 'redis':
            try:
                conn = redis.Redis(host=DatabaseInfo.redis_host,
                                   port=DatabaseInfo.redis_port,
                                   password=DatabaseInfo.redis_passwd
                                   )
                return conn
            except Exception as e:
                logging.error('数据库获取连接失败，报错日志为：%s' % e)

    # 针对城市信息，针对性的做一个城市列表转字典
    def cityinfo_list2dict(self, listinfo):
        dicts = []
        for i in listinfo:
            cityinfo = {}
            cityinfolist = str(i).split(':')
            cityinfo['city_id'] = cityinfolist[0]
            cityinfo['city_name'] = cityinfolist[-1]
            cityinfo['last_update_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
            dicts.append(cityinfo)
        return dicts
