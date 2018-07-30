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
# @File  : connectionDB.py
# @Author: huguangzhi
# @ContactEmail : huguangzhi@ucsdigital.com.com 
# @ContactPhone : 13121961510 
# @Date  : 2018-07-16 - 11:47
# @Desc  : 数据入库

import pymysql
import pymssql
from Mtime.V2.Util import Properties


global PropertiesFile
PropertiesFile = r'./filename.properties'


class SaveData(object):

    # 存储到mysql数据库
    def savemysql(self, sql, host):
        hostname = Properties(PropertiesFile).getProperties()['mysql'][str(host)]['host']
        database = Properties(PropertiesFile).getProperties()['mysql'][str(host)]['database']
        port     = int(Properties(PropertiesFile).getProperties()['mysql'][str(host)]['port'])
        username = Properties(PropertiesFile).getProperties()['mysql'][str(host)]['username']
        passwd   = Properties(PropertiesFile).getProperties()['mysql'][str(host)]['passwd']
        charset  = Properties(PropertiesFile).getProperties()['mysql'][str(host)]['charset']

        conn = pymysql.connect(host=hostname,
                               user=username,
                               passwd=passwd,
                               port=port,
                               db=database,
                               charset=charset)
        try:
            cur = conn.cursor()
        except:
            print('-------------连接数据库失败-------------')
        # 执行sql
        else:
            try:
                # print(sql)
                # mysql执行sql语句
                cur.execute(sql)
            except:
                print('---SQL语法错误，执行失败---'+sql)
            else:
                conn.commit()
                # print('执行成功，数据成功写入')

    # 存储到sqlserver数据库
    def savesqlserver(self, sql):

        hostname = Properties(PropertiesFile).getProperties()['sqlserver']['host']
        database = Properties(PropertiesFile).getProperties()['sqlserver']['database']
        port = Properties(PropertiesFile).getProperties()['sqlserver']['port']
        username = Properties(PropertiesFile).getProperties()['sqlserver']['username']
        passwd = Properties(PropertiesFile).getProperties()['sqlserver']['passwd']
        # charset = Properties(PropertiesFile).getProperties()['sqlserver']['charset']

        conn = pymssql.connect(host=hostname,
                               user=username,
                               port=port,
                               password=passwd,
                               database=database)
        try:
            cur = conn.cursor()
        except:
            print('-------------连接数据库失败-------------')
        # 执行sql
        else:
            try:
                # print(sql)
                # mysql执行sql语句
                cur.execute(sql)
            except:
                print('-------------sql语法错误，执行失败-------------')
                print(sql)
            else:
                conn.commit()
                # print('执行成功，数据成功写入')


class SelectData(object):

    # 查询mysql中数据
    def selectmysql(self, sql, host):
        try:
            hostname = Properties(PropertiesFile).getProperties()['mysql'][str(host)]['host']
            database = Properties(PropertiesFile).getProperties()['mysql'][str(host)]['database']
            port = int(Properties(PropertiesFile).getProperties()['mysql'][str(host)]['port'])
            username = Properties(PropertiesFile).getProperties()['mysql'][str(host)]['username']
            passwd = Properties(PropertiesFile).getProperties()['mysql'][str(host)]['passwd']
            charset = Properties(PropertiesFile).getProperties()['mysql'][str(host)]['charset']
        except Exception as  ess:
           print('Database Information Error :' + str(ess))

        conn = pymysql.connect(host=hostname,
                               user=username,
                               passwd=passwd,
                               port=port,
                               db=database,
                               charset=charset)
        try:
            cur = conn.cursor()
        except:
            print('-------------连接数据库失败-------------')
        # 执行sql
        else:
            try:
                # print(sql)
                # mysql执行sql语句
                cur.execute(sql)
                # 获取数据库的内容
                result = cur.fetchall()
                return result
            except:
                print('-------------sql语法错误，执行失败-------------')
                print(sql)

    # 查询sqlserver中数据
    def selectsqlserver(self, sql):
        hostname = Properties(PropertiesFile).getProperties()['sqlserver']['host']
        database = Properties(PropertiesFile).getProperties()['sqlserver']['database']
        port = Properties(PropertiesFile).getProperties()['sqlserver']['port']
        username = Properties(PropertiesFile).getProperties()['sqlserver']['username']
        passwd = Properties(PropertiesFile).getProperties()['sqlserver']['passwd']
        # charset = Properties(PropertiesFile).getProperties()['sqlserver']['charset']

        conn = pymssql.connect(host=hostname,
                               user=username,
                               port=port,
                               password=passwd,
                               database=database)
        try:
            cur = conn.cursor()
        except:
            print('-------------连接数据库失败-------------')
        # 执行sql
        else:
            try:
                # print(sql)
                # mysql执行sql语句
                cur.execute(sql)
                # 获取数据库的内容
                result = cur.fetchall()
                return result
            except:
                print('-------------sql语法错误，执行失败-------------')
                print(sql)