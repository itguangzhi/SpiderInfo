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
import random
import re
import urllib
from threading import Thread
from urllib.request import urlopen


# from Maoyan.Util import Tools



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
                # print('正在处理第' + str(maxpage + 1) + '页')
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
        link = 'http://maoyan.com/cinema/7524'
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

    def getaddressinfo2(self):
        city_info = ''
        info = str(city_info, encoding='utf-8')
        addrreg = r'<a class="js-city-name" data-ci="(.*?)" data-val="{ choosecityid:.*? }" data-act="cityChange-click">(.*?)</a>'
        addrs = re.findall(addrreg, info)
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
        try:
            cinemainfo['cinema_service_3Dglasses_info'] = re.findall(cinema3Dglassreg, cinemaservice)[0]
        except:
            cinemainfo['cinema_service_3Dglasses_info'] = '-'
        try:
            cinemainfo['cinema_service_3Dglasses_by'] = re.findall(cinema3Dglasstagreg, cinemaservice)[0]
        except:
            cinemainfo['cinema_service_3Dglasses_by'] = '-'

        try:
            cinemainfo['cinema_service_child '] = re.findall(cinemachildreg, cinemaservice)[1]
        except:
            cinemainfo['cinema_service_child '] = '-'

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


class Tools:
    menu_url = GetResponse.menu_url

    # 获取影院地址链接
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

    def MaoYanurlopen(self, link):
        request = urllib.request.Request(link)
        request.add_header('User-Agent', str(self.getUA(self)))
        request.add_header('Cookie',
                           '__mta=248954552.1533172087368.1534732553267.1534733685746.25"; _lxsdk_cuid=164f82d7537c8-0f989cd149666d-51422e1f-100200-164f82d7537c8; uuid_n_v=v1; uuid=84AB523095F011E883FE1F23FDFD6ADB1819195A754C410281F6435BC0E4293D; _lxsdk=84AB523095F011E883FE1F23FDFD6ADB1819195A754C410281F6435BC0E4293D; _csrf=d8e8905256c16f10cbd4629efc693c1df7c2221b9e4b90901125f75d1abff9d1; __mta=248954552.1533172087368.1533806526342.1533880670342.22; theme=moviepro; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ci=140; __mta=248954552.1533172087368.1533880670342.1534754983897.23"; _lxsdk_s=165566fc902-2e-3cc-73b%7C%7C35')
        response = urlopen(link).read()
        pageinfo = str(response, 'utf8').replace('\n', '')
        return pageinfo

        # 构建存储到mysql的入库语句

    def mysqlbuild(self, tbl, tablename:str):
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
        sql = "replace into %s (%s)VALUES %s;" % (Tbname, field, values)
        return sql

    def async(f):
        def wrapper(*args, **kwargs):
            thr = Thread(target=f, args=args, kwargs=kwargs)
            thr.start()

        return wrapper

    def getUA(self):
        ua = [
            "UCWEB7.0.2.37/28/999",
            "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
            "Opera/8.0 (Windows NT 5.1; U; en)",
            "Openwave/ UCWEB7.0.2.37/28/999",
            "NOKIA5700/ UCWEB7.0.2.37/28/999",
            "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0a1) Gecko/20110623 Firefox/7.0a1 Fennec/7.0a1",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ",
            "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0",
            "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
            "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.1812",
            "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; Redmi 3S Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko)Version/4.0 Chrome/37.0.0.0 MQQBrowser/7.3 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; U; Android 6.0.1; zh-cn; Redmi 3S Build/MMB29M) AppleWebKit/533.1 (KHTML, like Gecko) Mobile Safari/533.1",
            "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
            "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
            "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.",
            "Mozilla/5.0 (Linux; Android 6.0.1; Redmi 3S Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043124 Safari/537.36 MicroMessenger/6.5.7.1041 NetType/WIFI Language/zh_CN",
            "Mozilla/5.0 (Linux; Android 6.0.1; Redmi 3S Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.94 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 5.1.1; SAMSUNG SM-N9200 Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.4 Chrome/38.0.2125.102 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 4.4.4; en-us; Nexus 5 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2307.2 Mobile Safari/537.36",
            "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3 XiaoMi/MiuiBrowser/8.7.0",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7",
            "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/1A542a Safari/419.3",
            "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
            "Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10",
            "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER) ",
            "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E) ",
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50",
            "JUC (Linux; U; 2.3.7; zh-cn; MB200; 320*480) UCWEB7.9.3.103/139/999",
            "Dalvik/2.1.0 (Linux; U; Android 6.0.1; Redmi 3S MIUI/7.3.9)",
            "Dalvik/1.6.0 (Linux; U; Android 4.4; Nexus 5 Build/KRT16M)",
        ]

        useragent = random.choice(ua)
        return useragent


if __name__ == '__main__':
    filepath = './cinemainfo-%s' % str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    filepath2 = './MaoYanPlatforms-%s' % str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    addrinfo = GetResponse.getaddressinfo(GetResponse)
    print(addrinfo)

    cinemalinklist = GetResponse.getcinemaslink(GetResponse)
    # print(cinemalinklist)

    for cinemalink in cinemalinklist:
        cinemainfo = GetResponse.getcinemapageinfo(GetResponse, cinemalink)[0]
        print('正在获取 %s 影院的数据' % str(cinemainfo['cinema_name']))
        cinemainfoSQL = Tools.mysqlbuild(Tools,cinemainfo,'maoyan_cinema_info')
        with open(filepath, 'a+', encoding='utf-8') as f:
            f.writelines(str(cinemainfoSQL)+'\n')

        cinemashowes = GetResponse.getcinemapageinfo(GetResponse, cinemalink)[1]

        try:
            sqls = Tools.mysqlAllbuild(Tools, cinemashowes, 'maoyan_show_info')
        except:
            print('构建sql失败，源数据为：')
            print(cinemashowes)
            print('影院地址为：%s' % str(cinemalink))
            sqls = None
        with open(filepath2, 'a+', encoding='utf-8') as f1:
            f1.writelines(str(sqls) + '\n')
        # 按行生成sql
        # for cinemashow in cinemashowes:
        #     cinemashowSQL = Tools.mysqlbuild(Tools, cinemashow, 'maoyan_show_info')
        #     with open(filepath, 'a+',encoding='utf-8') as f:
        #         f.writelines(str(cinemashowSQL)+'\n')

    f.close()
    f1.close()
