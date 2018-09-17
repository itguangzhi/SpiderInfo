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


# @File  : infomation.py
# @Author: huguangzhi
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com 
# @ContactPhone : 13121961510 
# @Date  : 2018-09-17 - 15:16
# @Desc  : 配置信息

class Info:
    def datefilepath(self):
        # 数据落地到本地文件路径
        cinema_file_path = r'./data/cinemainfo.data'
        show_file_path = r'./data/showinfo.data'

    def logfilepath(self, name):
        # 日志输出路径
        error_path = r'./logs/error.log'
        info_path = r'./logs/info.log'
        warning_path = r'./logs/warning.log'

        if name == 'error_path':
            return error_path
        elif name == "info_path":
            return info_path
        elif name == "warning_path":
            return warning_path
        else:
            print("参数错误，请核查")

    def databaseinfo(self):
        # 数据库连接
        mysql_host = '192.168.30.111'
        mysql_port = 3306
        mysql_user = 'root'
        mysql_passwd = '123456'
        mysql_charset = 'utf8'
        mysql_database = 'spiderInc'

    def threadinfo(self):
        # 线程最大值
        poolsize = 50

    def sleepinfo(self):
        # 爬虫等待时间
        spider_v = 0.2
