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

from Maoyan.Util import Tools


class GetResponse:
    menu_url = r'http://maoyan.com'
    cinemas_url = r'http://maoyan.com/cinemas'
    films_url = r'http://maoyan.com/films'
    cinemaslist = []

    # 在影院筛选也获取影院url信息
    def getcinemaslink(self):
        print('开始获取影院链接信息')
        pageinfo = Tools.MaoYanurlopen(Tools, self.cinemas_url)
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
                pageinfo = Tools.MaoYanurlopen(Tools, nowpageurl)
                nowcinemaslinklist = Tools.getcinemaslinklist(Tools, pageinfo)
                for nowcinemaslink in nowcinemaslinklist:
                    cinemaslinklist.append(nowcinemaslink)
        except:
            print('就一页')

        return cinemaslinklist

    # 获取影院排期页面内容及信息
    def getcinemapageinfo(self, link):
        pageinfo = Tools.MaoYanurlopen(Tools, link)
        # 拿到影院服务信息
        serviceinfo = self.getcinemaserviceinfo(self, pageinfo, link)
        # 拿到影院排映信息
        showlist = self.getcinemashowinfo(self, pageinfo)
        return serviceinfo, showlist

    # 获取城市信息信息
    def getaddressinfo(self):
        link = 'http://maoyan.com/'
        pageinfo = Tools.MaoYanurlopen(Tools, link)
        addrreg = r'<a class="js-city-name" data-ci="(.*?)" data-val="{ choosecityid:.*? }" data-act="cityChange-click">(.*?)</a>'
        addrs = re.findall(addrreg, pageinfo)
        addrlist = []
        for addr in addrs:
            addrlib = {}
            addrlist['city_id'] = addr[0]
            addrlist['city_name'] = addr[1]
            addrlist.append(addrlib)
        return addrlist



    # 获取影院服务信息,传入link只为了获取影院ID
    def getcinemaserviceinfo(self, pageinfo, link):
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

    # 获取影院排期
    def getcinemashowinfo(self, pageinfo):
        showlist = []
        # 限制匹配范围
        showinforeg = r'<div class="container" id="app"(.*?)<div class="big-map-modal"'
        cinemashowinfo = str(re.findall(showinforeg, pageinfo, re.M)[0]).replace(' ', '')
        showinfolistsreg = r'<trclass(.*?)</tr>'
        showinfolist = re.findall(showinfolistsreg, cinemashowinfo)
        for showinfos in showinfolist:
            showinfo = {}
            # print(showinfos)
            showidreg = r'/xseats/(.*?)\?movieId=(.*?)&cinemaId=(.*?)"'
            # print(re.findall(showidreg, showinfos))
            showinfo['show_id '] = re.findall(showidreg, showinfos)[0][0]
            showinfo['movie_id '] = re.findall(showidreg, showinfos)[0][1]
            showinfo['cinema_id '] = re.findall(showidreg, showinfos)[0][2]
            showinfo['show_date '] = str(showinfo['show_id '])[:4] + '-' + str(showinfo['show_id '])[4:6] + '-' + str(
                showinfo['show_id '])[6:8]
            schedulreg = r'"begin-time">(.*?)</span><br/><spanclass="end-time">(.*?)散场</span></td><td><spanclass="lang">(.*?)</span></td><td><spanclass="hall">(.*?)</span>'
            # print(re.findall(schedulreg, showinfos))
            showinfo['begin_time '] = re.findall(schedulreg, showinfos)[0][0]
            showinfo['end_time '] = re.findall(schedulreg, showinfos)[0][1]
            showinfo['language '] = re.findall(schedulreg, showinfos)[0][2]
            showinfo['hall '] = re.findall(schedulreg, showinfos)[0][3]
            showinfo['pos '] = '-'
            showinfo['creation_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            showinfo['last_update_time '] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            showlist.append(showinfo)
        return showlist


if __name__ == '__main__':
    cinemalinklist = GetResponse.getcinemaslink(GetResponse)
    addrinfo = GetResponse.getaddressinfo(GetResponse)
    for cinemalink in cinemalinklist:
        cinemainfo = GetResponse.getcinemapageinfo(GetResponse, cinemalink)[0]
        cinemashow = GetResponse.getcinemapageinfo(GetResponse, cinemalink)[1]
