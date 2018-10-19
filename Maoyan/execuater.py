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
# @File  : execuater.py
# @Author: huguangzhi
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com
# @ContactPhone : 13121961510
# @Date  : 2018-09-17 - 17:14
# @Desc  :  执行层
import logging

from Maoyan.conf import infomation
from Maoyan.controller import controller
from Maoyan.maoyan_Util import MaoYan_Tools

infomation = infomation.Info()

logging.basicConfig(
    level=logging.INFO,
    # format='[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
    format='[%(asctime)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S,%a',
    filename=infomation.logfilepath('info_path'),
    filemode='w'
)

controller = controller()


class SqlExecuate:

    # 异步sql
    @MaoYan_Tools.async
    def execSQL(self, sql):
        conn = controller.connectionDB('mysql')
        try:
            cur = conn.cursor()
            num = cur.execute(sql)
            logging.info('sql 返回值：%s' % str(num))
            cur.close()
            conn.commit()
            conn.close()
            return num
        except:
            logging.error('SQL执行失败，执行语句为:%s' % str(sql))
            cur.close()
            conn.close()

    # 同步执行SQL
    def unexecSQL(self, sql):
        conn = controller.connectionDB('mysql')
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return res
