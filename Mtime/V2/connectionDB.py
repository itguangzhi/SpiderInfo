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
import xlwt
from Mtime.V2.Util import Properties


global PropertiesFile
PropertiesFile = r'./filename.properties'


class SaveData(object):

    # 存储到mysql数据库
    def savemysql(self, sql):
        hostname = Properties(PropertiesFile).getProperties()['mysql']['host']
        database = Properties(PropertiesFile).getProperties()['spider']['database']
        port     = int(Properties(PropertiesFile).getProperties()['spider']['port'])
        username = Properties(PropertiesFile).getProperties()['spider']['username']
        passwd   = Properties(PropertiesFile).getProperties()['spider']['passwd']
        charset  = Properties(PropertiesFile).getProperties()['spider']['charset']
        conn = pymysql.connect(host=hostname,
                               user=username,
                               passwd=passwd,
                               port=port,
                               db=database,
                               charset=charset
                               )
        try:
            cur = conn.cursor()
        except Exception as e:
            print(e)
            print('-------------连接数据库失败-------------')
        # 执行sql
        else:
            try:
                # print(sql)
                # mysql执行sql语句
                cur.execute(sql)
            except Exception as e:
                print(e)
                print('---SQL语法错误，执行失败---'+sql)
            else:
                conn.commit()
                # print('执行成功，数据成功写入')

    # 存储到sqlserver数据库
    # def savesqlserver(self, sql):
    #     import pymssql
    #
    #     hostname = Properties(PropertiesFile).getProperties()['sqlserver']['host']
    #     database = Properties(PropertiesFile).getProperties()['sqlserver']['database']
    #     port = Properties(PropertiesFile).getProperties()['sqlserver']['port']
    #     username = Properties(PropertiesFile).getProperties()['sqlserver']['username']
    #     passwd = Properties(PropertiesFile).getProperties()['sqlserver']['passwd']
    #     # charset = Properties(PropertiesFile).getProperties()['sqlserver']['charset']
    #
    #     conn = pymssql.connect(host=hostname,
    #                            user=username,
    #                            port=port,
    #                            password=passwd,
    #                            database=database)
    #     try:
    #         cur = conn.cursor()
    #     except:
    #         print('-------------连接数据库失败-------------')
    #     # 执行sql
    #     else:
    #         try:
    #             # print(sql)
    #             # mysql执行sql语句
    #             cur.execute(sql)
    #         except:
    #             print('-------------sql语法错误，执行失败-------------')
    #             print(sql)
    #         else:
    #             conn.commit()
    #             # print('执行成功，数据成功写入')


class SelectData(object):

    # 查询mysql中数据
    def selectmysql(self, sql, host):
        try:
            hostname = Properties(PropertiesFile).getProperties()['spider']['host']
            database = Properties(PropertiesFile).getProperties()['spider']['database']
            port = int(Properties(PropertiesFile).getProperties()['spider']['port'])
            username = Properties(PropertiesFile).getProperties()['spider']['username']
            passwd = Properties(PropertiesFile).getProperties()['spider']['passwd']
            charset = Properties(PropertiesFile).getProperties()['spider']['charset']
        except Exception as ess:
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
    # def selectsqlserver(self, sql):
    #     hostname = Properties(PropertiesFile).getProperties()['sqlserver']['host']
    #     database = Properties(PropertiesFile).getProperties()['sqlserver']['database']
    #     port = Properties(PropertiesFile).getProperties()['sqlserver']['port']
    #     username = Properties(PropertiesFile).getProperties()['sqlserver']['username']
    #     passwd = Properties(PropertiesFile).getProperties()['sqlserver']['passwd']
    #     # charset = Properties(PropertiesFile).getProperties()['sqlserver']['charset']
    #
    #     conn = pymssql.connect(host=hostname,
    #                            user=username,
    #                            port=port,
    #                            password=passwd,
    #                            database=database)
    #     try:
    #         cur = conn.cursor()
    #     except:
    #         print('-------------连接数据库失败-------------')
    #     # 执行sql
    #     else:
    #         try:
    #             # print(sql)
    #             # mysql执行sql语句
    #             cur.execute(sql)
    #             # 获取数据库的内容
    #             result = cur.fetchall()
    #             return result
    #         except:
    #             print('-------------sql语法错误，执行失败-------------')
    #             print(sql)

if __name__ == '__main__':
    sql = "replace into Mtime_MovieInfo_Page (movie_id,Movie_url,MovieName,MovieNameOther,MoviePost,MovieType,ReleasedDate,ReleasedArea,MovieNation,MovieDirector,ScreenWriter,DistributionEnterp,MoviePlot,ReleasedYear,TrailerNum,TrailerUrl,ActorNum,ActorUrl,ImageNum,ImageUrl,CommentNum,CommentUrl,CommentShortUrl,NewsNum,NewsUrl,lastupdate_time)VALUES('258729','http://movie.mtime.com/258729/','下一站：前任','Passed By','http://img5.mtime.cn/mg/2018/07/26/092533.52171554_270X405X4.jpg','爱情','2018-8-17','-','中国','陈鸿仪','','-','林心恬暗恋黄克群许久，长大后两人无数次错过，又遇到一些缘分不到的爱情，以为此生不会再见。最终，在两人的努力和坚持下，走到了一起。','2018','0','-','8','http://movie.mtime.com/258729/fullcredits.html','2','http://movie.mtime.com/258729/posters_and_images/','7','http://movie.mtime.com/258729/reviews/short/new.html','http://movie.mtime.com/258729/reviews/short/new.html','0','-','2018-08-02 02:10:22');"
    SaveData.savemysql(SaveData, sql)
