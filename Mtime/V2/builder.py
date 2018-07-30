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
from Mtime.V2.Util import Properties

global PropertiesFile
PropertiesFile = r'./filename.properties'


class KVbuildSQL():
    # 构建存储到sqlserver的入库语句

    def sqlserverbuild(self, tbl):
        field = ''
        value = ''
        using = ''
        updatedata = ''

        for field in tbl:
            val1 = str(tbl[field])+' AS ' + str(field)
            usingline = usingline + ' , ' + val1
            val2 = field + '=' + str(tbl[field])
            updatedataline = updatedata + ',' + val2
            fields = fields + ',' + field
            values = values + ',' + str(tbl[field])

        useing = list(usingline)
        useing[0] = 'select '
        using = ''.join(useing)

        updat = list(updatedataline)
        updat[0] = ' '
        updatedata = ''.join(updat)

        updat = list(fields)
        updat[0] = ' '
        fields = ''.join(updat)

        updat = list(values)
        updat[0] = ' '
        values = ''.join(updat)

        tablename = Properties(PropertiesFile).getProperties()['sqlserver']['table']
        sql = "merge into " + tablename + " as a " \
                                         " using (" + using + ") as b " \
                                                              " on a.movie_id = b.movie_id " \
                                                              " when matched then " \
                                                              " update set " + updatedata + \
             " when not matched then " \
             " insert (%s)VALUES(%s);" % (fields, values)
        return sql



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

        Tbname = Properties(PropertiesFile).getProperties()['spider']['table']
        sql = "replace into %s (%s)VALUES(%s);" % (Tbname, field, values)
        return sql
