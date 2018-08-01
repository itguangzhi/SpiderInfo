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
# @File  : main.py
# @Author: huguangzhi
# @ContactEmail : huguangzhi@ucsdigital.com.com 
# @ContactPhone : 13121961510 
# @Date  : 2018-07-16 - 11:44
# @Desc  : 这里是主方法，用于运行整个爬虫内容

from Mtime.V2.getinfo import tomovieinfo
from Mtime.V2.builder import KVbuildSQL
from Mtime.V2.connectionDB import SaveData
from Mtime.V2.selector import selectID
from Mtime.V2.future import comingReginList


def getComingReleaseMovie():
    movielist = comingReginList.comingReginLists.gettfulturemovieUrl(comingReginList.comingReginLists)
    for movieid in movielist:
        replaceToMysql(movieid)
        print(movieid+' is well done ')


# 爬虫结果放到MySQL中（要把大象放冰箱，总共分几步？）
def replaceToMysql(x):
    pageinfomation = tomovieinfo(x)
    # print(pageinfomation)
    saveinfomation = KVbuildSQL.mysqlbuild(KVbuildSQL, pageinfomation)
    # print(saveinfomation)
    SaveData.savemysql(SaveData, saveinfomation)


def mergeToSqlserver(x):
    ''

def updateToSqlserver(x):
    ''

# 更新数据库中上映状态为1的影片
def updateReleaseType(type=1):
    # default type = 1

    try:
        IDlist = selectID.getReleaseID(selectID,
                                       database='mysql',
                                       releasetype=type)
        print('Step [01] Load IDlist is well ')
        if len(IDlist) == 0:
            print('No new IDlist')
    except Exception as es:
        print('Step [01] Load IDlist in ERROR')
        print(es)
        pass

    for id in IDlist:
        x = id[0]
        x = '104640'
        try:
            pageinfo = tomovieinfo(int(x))
            print('Step [02] get page infomation is well')
        except Exception as es:
            print('Step [02] get page infomation is ERROR')
            print(es)
            continue

        try:
            SQL = KVbuildSQL.mysqlbuild(KVbuildSQL, pageinfo)
            print(SQL)
            print('Step [03] building SQL is well')
        except Exception as es:
            print('Step [03] building SQL is well')
            print(es)
            continue

        try:
            SaveData.savemysql(SaveData, SQL, 111)
            print('Step [04] save movie information is well')
        except Exception as es:
            print('Step [04] save movie information is well')
            print(es)
            continue


#
# if __name__ == "__main__":
#
#     setFrame = sys.argv
#
#
#     try:
#         if len(setFrame) == 3:
#             if setFrame[1] == 'mysql':
#                 if setFrame[2] == 'insert':
#                     replaceToMysql('2')
#                 elif setFrame[2] == 'update':
#                     updateToMysql('2')
#                 else:
#                     print('Second Coding Error , Please Try Again .')
#             elif setFrame[1] == 'sqlserver':
#                 if setFrame[2] == 'insert':
#                     mergeToSqlserver('2')
#                 elif setFrame[2] == 'update':
#                     updateToSqlserver('2')
#                 else:
#                     print('Second Coding Error , Please Try Again .')
#             else:
#                 print('First Coding Error , Please Try Again .')
#         else:
#             print('Coding Too Long , Please Try Again .')
#
#     except:
#         print('Input Coding Error , Please Try Again .')
#         pass

getComingReleaseMovie()
