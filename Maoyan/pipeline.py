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
# @File  : pipeline.py
# @Author: huguangzhi
# @Drivce: Thinkpad E470
# @ContactEmail : huguangzhi@ucsdigital.com.com
# @ContactPhone : 13121961510
# @Date  : 2018-09-17 - 16:55
# @Desc  : 数据落地
import logging

from Maoyan.conf.infomation import Info

Info = Info()

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(filename)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
    # format='[%(asctime)s] [line:%(lineno)d] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S,%a',
    filename=Info.logfilepath("info_path"),
    filemode='w'
)


class mysql_pipeline:

    # 构建大量数据sql入库语句
    def mysqlAllbuild(self, tbl, tablename: str):
        field = ''
        values = []
        for item in tbl:
            # item 是以键值对存在的字典类型
            for key in item:
                # key是字典中的列名
                field = field + ',' + key
            break
        fields = list(field)
        fields[0] = ''
        field = ''.join(fields)
        for item in tbl:
            # item 是以键值对存在的字典类型
            value = []
            for key in item:
                value.append(item[key])
            values.append(value)
        values = str(values).replace('[', '(').replace(']', ')')
        values = values[1:-1]

        Tbname = tablename
        # sql = "replace into %s (%s)VALUES %s;" % (Tbname, field, values)
        sql = "replace into %s (%s)VALUES %s;" % (Tbname, field, values)
        return sql

    # 构建数据成sql入库语句
    def mysqlbuild(self, tbl, tablename: str):
        field = ''
        values = ''
        for f in tbl:
            field = field + ',' + f
            values = values + ',' + "'" + tbl[f] + "'"
        fields = list(field)

        fields[0] = ''
        field = ''.join(fields)

        value = list(values)

        value[0] = ''
        values = ''.join(value)

        Tbname = tablename
        sql = "replace into %s (%s)VALUES(%s);" % (Tbname, field, values)
        return sql


class file_pipeline:
    # 保存cinemainfo的信息到文件
    def cinemainfosave(self, data, writef):
        # 数据信息： {'cinema_id': '616', 'city_id': '59', 'cinema_link': 'http://maoyan.com/cinema/616', 'cinema_name': '希望电影城', 'cinema_address': '都江堰市建设路天和盛世4栋3楼（近沃尔玛超市）', 'cinema_tel': '028-87120256', 'cinema_service_3Dglasses_info': '地下停车场 乘电梯可直接到达影城', 'cinema_service_3Dglasses_by': '-', 'cinema_service_child': '-', 'cinema_service_park': '地下停车场 乘电梯可直接到达影城', 'creation_date': '2018-09-04 17:52:04', 'last_update_time': '2018-09-04 17:52:04'}
        # 数据库结构：cinema_id,city_id,cinema_name,cinema_address,cinema_tel,cinema_service_3Dglasses_info,cinema_service_3Dglasses_by,cinema_service_child,cinema_service_park,cinema_link,creation_date,last_update_time,
        line = str(data['cinema_id']) + ','
        line = line + str(data['city_id']) + ','
        line = line + str(data['cinema_name']) + ','
        line = line + str(data['cinema_address']) + ','
        line = line + str(data['cinema_tel']) + ','
        line = line + str(data['cinema_service_3Dglasses_info']) + ','
        line = line + str(data['cinema_service_3Dglasses_by']) + ','
        line = line + str(data['cinema_service_child']) + ','
        line = line + str(data['cinema_service_park']) + ','
        line = line + str(data['cinema_link']) + ','
        line = line + str(data['creation_date']) + ','
        line = line + str(data['last_update_time'])
        self.writefile(self, writef, line)
        return line

    # 保存showinfo的内容到文件
    def showinfosave(self, datalist, writef):
        lines = ''
        # 数据信息[{'show_id': '201809040268614', 'movie_id': '343070', 'movie_name': '精灵旅社3：疯狂假期', 'cinema_id': '283', 'cinema_name': '嘉和电影院', 'show_date': '2018-09-04', 'begin_time': '19:50', 'end_time': '21:28', 'language': '国语3D', 'hall': '2号厅', 'pos': '-', 'last_update_time': '2018-09-04 18:21:53'}, {'show_id': '201809040268613', 'movie_id': '343208', 'movie_name': '蚁人2：黄蜂女现身', 'cinema_id': '283', 'cinema_name': '嘉和电影院', 'show_date': '2018-09-04', 'begin_time': '19:50', 'end_time': '21:49', 'language': '国语3D', 'hall': '3号厅', 'pos': '-', 'last_update_time': '2018-09-04 18:21:53'}]
        for data in datalist:

            line = str(data['show_id']) + ','
            line = line + str(data['cinema_id']) + ','
            try:
                line = line + str(data['cinema_name']) + ','
            except:
                line = line + str('-') + ','
                logging.warning('影院ID: %s 在未获取到' % str(data['cinema_id']))
                pass
            line = line + str(data['movie_id']) + ','
            try:
                line = line + str(data['movie_name']) + ','
            except:
                line = line + str('-') + ','
                logging.warning('影片ID: %s 在数据库中未检索到 ：%s' % (str(data['movie_id']), str(data)))
            line = line + str(data['show_date']) + ','
            line = line + str(data['begin_time']) + ','
            line = line + str(data['end_time']) + ','
            line = line + str(data['language']) + ','
            line = line + str(data['hall']) + ','
            line = line + str(data['pos']) + ','
            # line = line + str(data['creation_date']) + ','
            line = line + str('-') + ','
            line = line + str(data['last_update_time'])
            self.writefile(self, writef, line)
            lines += line + '\n'
        return lines
