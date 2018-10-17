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
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com
# @ContactPhone : 13121961510
# @Date  : 2018-09-19 - 13:59
# @Desc  : 主程序控制器
import datetime
import logging

from Maoyan.conf.infomation import Info
from Maoyan.controller import controller
from Maoyan.downloader import Downloader
from Maoyan.execuater import SqlExecuate
from Maoyan.maoyan_Util import Properties, MaoYan_Tools
from Maoyan.modle import modle
from Maoyan.parse import MoviePares, CinemaPares, ShowPares
from Maoyan.pipeline import mysql_pipeline, file_pipeline

ShowPares = ShowPares()
modle = modle()
controller = controller()
MoviePares = MoviePares()
CinemaPares = CinemaPares()
mysql_pipeline = mysql_pipeline()
file_pipeline = file_pipeline()
MaoYan_Tools = MaoYan_Tools()
Downloader = Downloader()
SqlExecuate = SqlExecuate()
Info = Info()
# 配置文件中还没有传入配置参数文件目录
Properties = Properties('')

logging.basicConfig(
    level=logging.DEBUG,
    # format='[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
    format='[%(asctime)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S,%a',
    # filename=Info.logfilepath('info_path'),
    # filemode='w'
)


class Run:
    nowdatetime = str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    print('爬虫开始%s' % nowdatetime)

    def cinema_run(self):
        # 获取全国范围的影院链接
        # countrywide_cinemaslink = modle.getcinemaslink()
        countrywide_cinemaslink = [['http://maoyan.com/cinema/2']]
        for cinemalinks in countrywide_cinemaslink:
            for cinemalink in cinemalinks:
                logging.info(cinemalink)
                print(cinemalink)
                cinema_page = Downloader.get_response(cinemalink)
                logging.info(cinema_page)
                print(cinema_page)
                break
            break

    def show_run(self):
        pass

    def city_run(self):
        pass


if __name__ == '__main__':
    Run = Run()
    Run.cinema_run()

    # _options = sys.argv[1]
    # if _options == 'cinemainfo':
    #     Run.cinema_run()
    #
    # elif _options == 'showinfo':
    #     Run.show_run()
    #
    # elif _options == 'cityinfo':
    #     Run.city_run()
    #
    # else:print('ERROR ：%s参数错误'%str(_options))
