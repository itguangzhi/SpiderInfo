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
# @File  : othercity_cinemainfo.py
# @Author: huguangzhi
# @design: HP
# @ContactEmail : huguangzhi@ucsdigital.com.com
# @ContactPhone : 13121961510
# @Date  : 2018/9/2 - 17:10
# @Desc  :
import re
import time

import pymysql
from selenium import webdriver

broswer = webdriver.Chrome('./chromedriver.exe')

maoyan = r'http://maoyan.com/cinemas'
broswer.get(maoyan)


def city_data(sqls):
    conn = pymysql.connect(
        host='192.168.30.111',
        port=3306,
        user='root',
        passwd='123456',
        charset='utf8',
        database='spiderInc'
    )
    cur = conn.cursor()
    cur.execute(sqls)
    res = cur.fetchall()
    # print(res)
    result = str(res).replace('(', '').replace(' ', '').replace(',)', '').replace(')', '').split(',')
    conn.commit()
    return result


def builder(cityid, linklist):
    '''
    城市信息的城市ID和当前城市下的所有影院合并
    :param cityid:
    :param linklist:
    :return:
    '''
    values = []
    for link in linklist:
        # print(link)
        value = []
        value.append(int(str(link).split('/')[-1]))
        value.append(int(cityid))
        value.append(link)
        # print(value)
        values.append(value)
    # print(values)

    val = str(values)[1:-1].replace('[', '(').replace(']', ')')
    SQL = 'replace into maoyan_cinema_link (cinema_id,city_id,cinema_link)values %s' % val
    updateSQL = ''
    print(SQL)

    return SQL

def getcityxpath(ci: str):
    city_xpath = '//a[@data-ci="%s"]'%ci
    return city_xpath

def getallcitycinemainfo():
    cinemaListAll = {}
    sql = 'select city_id from maoyan_city_info order by city_id;'
    for city_id in city_data(sql):
        print('城市ID：'+str(city_id))
        citypath = getcityxpath(city_id)
        # print(citypath)

        broswer.find_element_by_xpath('//div[@class="city-selected"]').click()
        time.sleep(0.1)
        broswer.find_element_by_xpath(citypath).click()
        time.sleep(0.1)

        try:
            firstpage = broswer.find_element_by_xpath('//ul[@class="list-pager"]/li[1]').text

            if firstpage == '上一页':
                broswer.find_element_by_xpath('//ul[@class="list-pager"]/li[2]').click()
            cinemalinklist = []
            while True:
                for sel in range(1, 13):
                    try:
                        cinemalinkxpath = '//*[@id="app"]/div[2]/div[%s]/div[1]/a' % str(sel)
                        cinemalink = broswer.find_element_by_xpath(cinemalinkxpath)
                        cinemalink = cinemalink.get_attribute('href')
                        # print(cinemalink)
                        cinemalink = re.findall('(.*?)\?poi=.*?', cinemalink)[0]
                        # print(cinemalink)
                        cinemalinklist.append(cinemalink)
                        time.sleep(0.1)
                        # print(len(cinemalinklist))
                    except:
                        break
                # print('----一页------------------------------------------------------------------')
                broswer.find_element_by_xpath('//ul[@class="list-pager"]/li[last()]').click()
                lastpage = broswer.find_element_by_xpath('//ul[@class="list-pager"]/li[last()]').text
                if lastpage != '下一页':
                    break

            sql = builder(city_id, cinemalinklist)
            city_data(sql)
        except:
            pass


        # cinemaListAll[city_id] = cinemalinklist

alllist = getallcitycinemainfo()
print(alllist)







