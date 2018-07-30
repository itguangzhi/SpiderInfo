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
# @File  : builder.py
# @Author: huguangzhi
# @ContactEmail : huguangzhi@ucsdigital.com.com 
# @ContactPhone : 13121961510 
# @Date  : 2018-07-16 - 17:06
# @Desc  :  构建入库sql
from Util import Properties

global PropertiesFile
PropertiesFile = r'./filename.properties'


class KVbuildSQL():
    # 构建存储到sqlserver的入库语句
    def sqlserverbuild(self,field,values):
        tablename = Properties(PropertiesFile).getProperties()['sqlserver']['table']
        sql = ""



    # 构建存储到mysql的入库语句
    def mysqlbuild(self, tbl):
        field = ''
        values = ''
        for f in tbl:
            field = field+','+f
            values = values+','+"'"+tbl[f]+"'"
        fields = list(field)

        fields[0] = ''
        field = ''.join(fields)

        value = list(values)

        value[0] = ''
        values = ''.join(value)


        Tbname = Properties(PropertiesFile).getProperties()['mysql']['111']['table']
        sql = "replace into %s (%s)VALUES(%s);" % (Tbname, field, values)
        return sql
