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
# @File  : getPage.py
# @Author: huguangzhi
# @design: HP
# @ContactEmail : huguangzhi@ucsdigital.com.com
# @ContactPhone : 13121961510
# @Date  : 2018/8/19 - 14:28
# @Desc  : 获取网页内容
import datetime
import re
from urllib.request import urlopen


class GetResponse:
    menu_url = r'http://maoyan.com'
    cinemas_url = r'http://maoyan.com/cinemas'
    films_url = r'http://maoyan.com/films'
    cinemaslist = []

    # 在影院筛选也获取影院url信息
    def getcinemaslink(self):
        print('开始获取影院链接信息')
        response = urlopen(self.cinemas_url).read()
        pageinfo = str(response, 'utf8').replace('\n', '')
        reg = r'"?offset=(.*?)"'
        cinemaslinklist = Tools.getcinemaslinklist(Tools, pageinfo)

        try:
            max_page = int(re.findall(reg, pageinfo, re.S)[-2]) / 12
            maxnum = int(max_page) + 1
            print('共计有' + str(maxnum) + '页')
            # 遍历每一个影院网页
            for maxpage in range(1, maxnum):
                print('正在处理第' + str(maxpage + 1) + '页')
                nowpageurl = self.cinemas_url + '?offset=%s' % str(int(maxpage) * 12)
                response = urlopen(nowpageurl).read()
                pageinfo = str(response, 'utf8').replace('\n', '')
                nowcinemaslinklist = Tools.getcinemaslinklist(Tools, pageinfo)
                for nowcinemaslink in nowcinemaslinklist:
                    cinemaslinklist.append(nowcinemaslink)
        except:
            print('就一页')

        return cinemaslinklist

    # 获取影院排期页面内容及信息
    def getcinemapageinfo(self, link):

        response = urlopen(link).read()
        pageinfo = str(response, 'utf8').replace('\n', '')
        # 拿到影院服务信息
        serviceinfo = self.getcinemaserviceinfo(self, pageinfo)
        # 拿到影院排映信息

        showlist = self.getcinemashowindo(self, pageinfo)


        return serviceinfo, showlist

    # 获取影院服务信息
    def getcinemaserviceinfo(self, pageinfo):
        cinemainfo = {}
        cinemaservicereg = r'<div class="cinema-brief-container">(.*?)<div class="cinema-map"'
        cinemaservice = re.findall(cinemaservicereg, pageinfo, re.M)[0]
        cinemanamereg = r'<h3 class="name text-ellipsis">(.*?)</h3>'
        cinemaaddrreg = r'<div class="address text-ellipsis">(.*?)</div>'
        cinematelreg = r'<div class="telphone">电话：(.*?)</div>'
        cinema3Dglasstagreg = r'<span class="tag ">(.*?)</span>'
        cinema3Dglassreg = r'<p class="desc text-ellipsis" title="(.*?)">'
        cinemachildreg = r'<p class="desc text-ellipsis" title="(.*?)">'
        cinemaparkreg = r'<span class="tag park-tag">.*?<p class="desc text-ellipsis" title="(.*?)">'
        cinemainfo['cinema_id'] = str(link).split('/')[-1]
        cinemainfo['cinema_name'] = re.findall(cinemanamereg, cinemaservice)[0]
        cinemainfo['cinema_address '] = re.findall(cinemaaddrreg, cinemaservice)[0]
        cinemainfo['cinema_tel '] = re.findall(cinematelreg, cinemaservice)[0]
        cinemainfo['cinema_service_3Dglasses_info'] = re.findall(cinema3Dglassreg, cinemaservice)[0]
        cinemainfo['cinema_service_3Dglasses_by'] = re.findall(cinema3Dglasstagreg, cinemaservice)[0]
        cinemainfo['cinema_service_child '] = re.findall(cinemachildreg, cinemaservice)[1]
        try:
            cinemainfo['cinema_service_park'] = re.findall(cinemaparkreg, cinemaservice)[0]
        except:
            cinemainfo['cinema_service_park'] = '-'
        cinemainfo['creation_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cinemainfo['last_update_time '] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return cinemainfo

    def getcinemashowindo(self, pageinfo):
        showlist = []
        showinfo = {}
        showinforeg = r'<div class="container" id="app"(.*?)<div class="big-map-modal"'
        cinemashowinfo = str(re.findall(showinforeg, pageinfo, re.M)[0]).replace(' ', '')

        moviereg = r'data-val="{city_id:.*?,movie_id:(.*?),cinema_id:(.*?)}">'
        showlistreg = r'<divclass="show-list.*?"data-index="0">(.*?)<divclass="show-list'
        movielists = re.findall(moviereg, cinemashowinfo, re.S)

        showlists = re.findall(showlistreg, cinemashowinfo, re.M)
        showinfo['cinema_id '] = movielists[0][1]
        for item in range(0, len(showlists)):
            showinfolist = showlists[item]

            showinfo['movie_id '] = movielists[item][0]

        # showinfo['show_id '] = re.findall(showidreg, cinemashowinfo, re.M)
        #
        # showinfo['movie_id '] = re.findall(moviereg, cinemashowinfo, re.M)
        # showinfo['show_date '] = re.findall(, cinemashowinfo, re.M)
        # showinfo['begin_time '] = re.findall(, cinemashowinfo, re.M)
        # showinfo['end_time '] = re.findall(, cinemashowinfo, re.M)
        # showinfo['language '] = re.findall(, cinemashowinfo, re.M)
        # showinfo['hall '] = re.findall(, cinemashowinfo, re.M)
        # showinfo['pos '] = re.findall(, cinemashowinfo, re.M)
            showinfo['creation_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            showinfo['last_update_time '] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            showlist.append(showinfo)

        return showlist


class Tools:
    menu_url = GetResponse.menu_url

    def getcinemaslinklist(self, pageinfo):
        cinemalinklist = []
        cinemareg = r'class="cinema-name" .*?data-val="{city_id: .*?, cinema_id: (.*?)}">(.*?)</a>'
        cinemasinfo = re.findall(cinemareg, pageinfo)
        for c in cinemasinfo:
            # cinema = {}
            # # 影院id
            # cinema['cinema_id'] = c[0]
            # # 影院名称
            # cinema['cinema_name'] = c[1]
            # 影院link
            cinemalink = self.menu_url + '/cinema/' + str(c[0])
            cinemalinklist.append(cinemalink)

        return cinemalinklist


link = 'http://maoyan.com/cinema/5278'
for i in GetResponse.getcinemapageinfo(GetResponse, link):
    print(i)
