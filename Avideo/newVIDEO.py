"""
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
"""
# @File  : newVIDEO.py
# @Author: huguangzhi
# @design: HP
# @ContactEmail : huguangzhi@ucsdigital.com.com
# @ContactPhone : 13121961510
# @Date  : 2018/8/8 - 22:47
# @Desc  : 获取最新更新视频页面URL及页面信息
import datetime
import re
from time import sleep
from urllib.request import urlopen
from urllib.request import Request
import urllib.request
import pymysql
from Avideo.Util import Properties
import socket

PropertiesFile = r'../filename.properties'


class newVIDEO():

    def getNewList(self, mainurl):
        contentlib = []
        newurl = mainurl + '/detail/new.html'
        # print(newurl)
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        req = Request(url=newurl, headers=headers)
        page = urlopen(req)
        pages = str(page.read(), 'utf-8')
        reg = ' <div class="hotcon">.*?<ul>(.*?)</ul>'
        list = re.findall(reg, pages, re.S)[0]
        contentReg = '<li><span>(.*?)</span><em><a href=".*?">(.*?)</a></em><i class="on">.*?</i><a href="(.*?)" target="_blank" title="(.*?)">.*?</a></li>'
        contentlist = re.findall(contentReg, list)
        page.close()
        # print(contentlist)
        for av in contentlist:
            print(av)
            content = {}
            if 'font' in av[0]:
                newREG = '<font color="red">(.*?)</font>'
                content['new'] = '1'
                year = str(datetime.datetime.now().year)
                content['releasedate'] = year+'-'+str(re.findall(newREG, av[0])[0])
            else:
                content['new'] = '0'
                content['releasedate'] = year+'-'+av[0]
            content['name'] = av[-1]
            content['movieurl'] = av[-2]
            content['type'] = av[1]
            idreg = '/vod/(.*?).html'
            content['id'] = re.findall(idreg, av[-2])[0]
            contentlib.append(content)
            # print(content)
        return contentlib

    def getAsia(self, mainurl, pagenum):
        adsbegin = int(pagenum)*10+2
        adsend = int(pagenum+1)*10+2
        contentlib = []
        for nm in range(adsbegin, adsend):
            newurl = mainurl + '/list/1-%s.html'% str(nm)
            print(newurl)
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
            req = Request(url=newurl, headers=headers)
            page = urlopen(req)
            pages = str(page.read(), 'utf-8')
            reg = ' <div class="movielist">.*?<ul class="mlist">(.*?)</ul>'
            list = re.findall(reg, pages, re.S)[0]

            lists = list.replace('\r\n', ' ')
            # print(lists)
            contentReg = '<li> <a href=".*?" title=".*?" target="_blank" class="p"><img src=".*?" alt=".*?" /></a> <div class="info"><h2><a href="(.*?)" title="(.*?)" target="_blank">.*?</a><em></em></h2> <p><i>更新：(.*?)</i></p> <p><i>类型：(.*?)</i></p> <p><i>撸量：.*?</i>.*?</li>'
            contentlist = re.findall(contentReg, lists, re.S)
            page.close()
            # print(contentlist)
            for av in contentlist:
                # print(av)
                content = {}

                content['releasedate'] = av[-2]
                content['name'] = av[1]
                content['movieurl'] = av[0]
                content['type'] = av[-1]
                idreg = '/vod/(.*?).html'
                content['id'] = re.findall(idreg, av[0])[0]
                contentlib.append(content)
                # print(content)

            # break
        return contentlib


    def getContent(self, main, detailURL):
        download = {}
        url = main+detailURL
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        req = Request(url=url, headers=headers)
        pages = urlopen(req)
        page = str(pages.read(), 'utf-8')
        pages.close()
        # print(page)
        thunderREG = '<li class="thunder"><a href="(.*?)"'
        download['thunder'] = re.findall(thunderREG, page)[0]

        qqdlREG = '<li class="qqdl"><a href="(.*?)"'
        download['qqdl'] = re.findall(qqdlREG, page)[0]

        flashgetREG = '<li class="flashget"><a href="(.*?)"'
        download['flashget'] = re.findall(flashgetREG, page)[0]

        ed2kREG = '<li class="ed2k"><a href="(.*?)"'
        download['ed2k'] = re.findall(flashgetREG, page)[0]

        return download


class saveDB():

    # 构建存储到mysql的入库语句
    def mysqlbuild(self, tbl, Tbname):
        field = ''
        values = ''
        for f in tbl:
            field = field + ',' + f
            values = values + ',' + "'" + str(tbl[f]) + "'"
        fields = list(field)

        fields[0] = ''
        field = ''.join(fields)

        value = list(values)

        value[0] = ''
        values = ''.join(value)

        from Avideo.Util import Properties

        sql = "replace into %s (%s)VALUES(%s);" % (Tbname, field, values)
        return sql

    def connection(self):
        hostname = Properties(PropertiesFile).getProperties()['spider']['host']
        database = Properties(PropertiesFile).getProperties()['spider']['database']
        port = int(Properties(PropertiesFile).getProperties()['spider']['port'])
        username = Properties(PropertiesFile).getProperties()['spider']['username']
        passwd = Properties(PropertiesFile).getProperties()['spider']['passwd']
        charset = Properties(PropertiesFile).getProperties()['spider']['charset']
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
            return cur, conn

    def exec(self, cursor, conn, sql):
        try:
            # print(sql)
            # mysql执行sql语句
            cursor.execute(sql)
        except Exception as e:
            print(e)
            print('---SQL语法错误，执行失败---' + sql)
        else:
            conn.commit()

if __name__ == '__main__':
    menu = 'http://6666av.vip'

    socket.setdefaulttimeout(100)
    # contentlist = newVIDEO.getNewList(newVIDEO, menu)
    for B in range(7, 53):
        contentlist = newVIDEO.getAsia(newVIDEO, menu, B)
        # print(len(contentlist))
        # print(contentlist)
        for C in contentlist:
            detailurl = C['movieurl']
            detail = newVIDEO.getContent(newVIDEO, menu, detailurl)
            for D in detail:
                C[D] = detail[D]
            sql = saveDB.mysqlbuild(saveDB, C, 'avideo')
            print(sql)
            cur, conn = saveDB.connection(saveDB)
            saveDB.exec(saveDB, cur, conn, sql)
            sleep(1)


