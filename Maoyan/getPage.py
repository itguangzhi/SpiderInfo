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


class Information:
    city_info = ['150:150:阿拉善盟', '151:151:鞍山', '197:197:安庆', '238:238:安阳', '319:319:阿坝', '324:324:安顺', '359:359:安康',
                 '400:400:阿勒泰', '394:394:阿克苏', '490:490:安吉', '588:588:安丘', '699:699:安岳', '807:807:安平', '873:873:安宁',
                 '844:844:安溪', '1008:1008:安化', '1126:1126:阿勒泰市', '1068:1068:安福', '1:1:北京', '84:84:保定', '88:88:蚌埠',
                 '140:140:包头', '153:153:本溪', '146:146:巴彦淖尔', '167:167:白城', '165:165:白山', '204:204:亳州', '233:233:滨州',
                 '317:317:巴中', '292:292:北海', '297:297:百色', '327:327:毕节', '332:332:保山', '353:353:宝鸡', '363:363:白银',
                 '393:393:巴州', '392:392:博尔塔拉', '533:533:滨海', '602:602:宝应', '681:681:北流', '698:698:博爱', '731:731:北碚',
                 '783:783:宝丰', '887:887:泌阳', '852:852:博兴', '952:952:博山', '946:946:璧山', '915:915:彬县', '994:994:宾阳',
                 '1102:1102:博白县', '1098:1098:博罗县', '1141:1141:北镇市', '1074:1074:泊头市', '1165:1165:北安市', '1193:1193:巴彦县',
                 '45:45:重庆', '59:59:成都', '70:70:长沙', '89:89:常州', '116:116:长春', '127:127:沧州', '126:126:承德', '142:142:赤峰',
                 '131:131:长治', '160:160:朝阳', '205:205:池州', '202:202:巢湖', '199:199:滁州', '287:287:潮州', '271:271:郴州',
                 '268:268:常德', '301:301:崇左', '337:337:楚雄', '391:391:昌吉', '421:421:从化', '422:422:常熟', '463:463:长乐',
                 '452:452:长兴', '451:451:慈溪', '527:527:昌邑', '627:627:长葛', '624:624:苍南', '700:700:承德县', '653:653:赤壁',
                 '646:646:崇州', '660:660:淳安', '746:746:曹妃甸', '737:737:昌乐', '767:767:磁县', '801:801:昌黎', '811:811:岑溪',
                 '798:798:成安', '795:795:长垣', '883:883:曹县', '890:890:城阳', '877:877:茌平', '954:954:长汀', '909:909:城固',
                 '1018:1018:赤水', '993:993:常山', '981:981:长寿', '970:970:潮安', '969:969:潮阳', '968:968:澄海', '1100:1100:长丰县',
                 '1097:1097:茶陵', '1092:1092:常宁市', '1150:1150:苍溪县', '1078:1078:慈利', '1157:1157:长清区', '1164:1164:崇明区',
                 '1201:1201:成武县', '1205:1205:澄江县', '65:65:大连', '91:91:东莞', '90:90:大庆', '129:129:大同', '154:154:丹东',
                 '178:178:大兴安岭', '223:223:东营', '231:231:德州', '305:305:德阳', '315:315:达州', '342:342:德宏', '341:341:大理',
                 '344:344:迪庆', '370:370:定西', '434:434:敦煌', '431:431:丹阳', '478:478:东台', '477:477:大丰', '467:467:德清',
                 '455:455:东阳', '491:491:当阳', '552:552:登封', '571:571:儋州', '539:539:东港', '635:635:东兴', '576:576:都江堰',
                 '599:599:大石桥', '600:600:大冶', '686:686:东方', '679:679:大通', '651:651:灯塔', '642:642:调兵山', '662:662:邓州',
                 '750:750:电白', '738:738:东平', '765:765:定州', '754:754:东海', '874:874:达拉特旗', '835:835:郸城', '836:836:大荔',
                 '945:945:大洼', '910:910:大竹', '999:999:东光', '978:978:敦化', '971:971:大邑', '974:974:砀山', '1035:1035:道县',
                 '1076:1076:大安市', '1168:1168:定安县', '1203:1203:东明县', '1204:1204:定陶区', '1208:1208:定边县', '144:144:鄂尔多斯',
                 '254:254:鄂州', '261:261:恩施', '417:417:峨眉山', '568:568:额尔古纳', '989:989:恩平', '1172:1172:额敏县', '44:44:福州',
                 '92:92:佛山', '152:152:抚顺', '156:156:阜新', '200:200:阜阳', '220:220:抚州', '293:293:防城港', '427:427:涪陵',
                 '416:416:富阳', '462:462:福清', '480:480:凤凰', '545:545:肥城', '535:535:阜宁', '540:540:奉化', '677:677:汾阳',
                 '689:689:阜康', '665:665:凤城', '742:742:范县', '735:735:丰城', '827:827:封丘', '792:792:肥乡', '774:774:繁昌',
                 '888:888:富顺', '869:869:抚松', '862:862:丰县', '861:861:扶风', '937:937:扶沟', '924:924:丰宁', '921:921:佛冈',
                 '916:916:费县', '980:980:凤台', '1142:1142:肥西县', '1031:1031:奉新', '1052:1052:方城', '1066:1066:富源县',
                 '1070:1070:分宜', '1084:1084:扶绥县', '1152:1152:凤翔县', '1195:1195:福安', '1202:1202:福鼎市', '1209:1209:府谷县',
                 '20:20:广州', '93:93:桂林', '107:107:贵阳', '217:217:赣州', '307:307:广元', '314:314:广安', '295:295:贵港',
                 '320:320:甘孜', '373:373:甘南', '385:385:固原', '553:553:巩义', '570:570:桂平', '521:521:高邮', '541:541:广饶',
                 '631:631:高州', '630:630:个旧', '629:629:高碑店', '638:638:盖州', '581:581:公主岭', '589:589:高密', '593:593:广汉',
                 '595:595:藁城', '601:601:高平', '702:702:格尔木', '691:691:古交', '751:751:灌云', '752:752:灌南', '753:753:赣榆',
                 '787:787:共青城', '771:771:高安', '780:780:广德', '866:866:高陵', '854:854:高阳', '911:911:公安', '1104:1104:固始县',
                 '1174:1174:光泽', '50:50:杭州', '56:56:合肥', '95:95:葫芦岛', '94:94:海口', '105:105:哈尔滨', '123:123:邯郸',
                 '139:139:呼和浩特', '128:128:衡水', '145:145:呼伦贝尔', '170:170:鹤岗', '186:186:湖州', '176:176:黑河', '180:180:淮安',
                 '198:198:黄山', '193:193:淮南', '195:195:淮北', '239:239:鹤壁', '234:234:菏泽', '250:250:黄石', '273:273:怀化',
                 '281:281:惠州', '284:284:河源', '258:258:黄冈', '265:265:衡阳', '298:298:贺州', '299:299:河池', '338:338:红河',
                 '375:375:海东', '381:381:海西', '378:378:海南州', '357:357:汉中', '410:410:花都', '390:390:哈密', '424:424:海宁',
                 '472:472:惠阳', '471:471:惠东', '464:464:黄岛', '504:504:鹤山', '505:505:桦甸', '506:506:海城', '564:564:华阴',
                 '575:575:霸州', '573:573:海阳', '519:519:海门', '623:623:海安', '579:579:侯马', '598:598:河津', '685:685:海林',
                 '672:672:化州', '650:650:黄骅', '645:645:霍州', '758:758:淮阳', '732:732:合川', '726:726:海盐', '816:816:滑县',
                 '825:825:惠安', '806:806:怀仁', '800:800:辉县', '799:799:户县', '794:794:和县', '793:793:含山', '772:772:汉阴',
                 '881:881:河口', '894:894:辉南', '867:867:洪洞', '851:851:横店', '856:856:华亭', '832:832:韩城', '928:928:洪湖',
                 '1005:1005:怀宁', '977:977:珲春', '975:975:霍邱', '964:964:海沧', '1103:1103:潢川县', '1088:1088:衡阳县',
                 '1090:1090:衡山县', '1091:1091:衡东县', '1105:1105:贺兰县', '1130:1130:海伦市', '1124:1124:汉南区', '1145:1145:合江县',
                 '1042:1042:怀远县', '1065:1065:会泽县', '1080:1080:河间市', '1086:1086:合浦县', '1185:1185:环县', '1206:1206:黄陵县',
                 '8001:8001:华容', '98:98:锦州', '96:96:济南', '97:97:焦作', '115:115:九江', '132:132:晋城', '134:134:晋中',
                 '169:169:鸡西', '173:173:佳木斯', '161:161:吉林', '185:185:嘉兴', '188:188:金华', '218:218:吉安', '213:213:景德镇',
                 '225:225:济宁', '255:255:荆门', '249:249:济源', '277:277:江门', '257:257:荆州', '288:288:揭阳', '368:368:酒泉',
                 '362:362:金昌', '409:409:嘉峪关', '404:404:江阴', '439:439:靖江', '420:420:晋江', '460:460:金坛', '510:510:江山',
                 '489:489:嘉善', '544:544:晋州', '515:515:句容', '536:536:建湖', '636:636:介休', '583:583:胶州', '594:594:建德',
                 '605:605:简阳', '678:678:集安', '664:664:即墨', '756:756:建阳', '725:725:蛟河', '831:831:监利', '785:785:郏县',
                 '882:882:巨野', '871:871:江津', '956:956:金湖', '948:948:江都', '941:941:莒南', '927:927:江油', '918:918:京山',
                 '913:913:缙云', '900:900:金乡', '899:899:嘉祥', '1001:1001:金沙', '1003:1003:泾县', '963:963:集美',
                 '1134:1134:鄄城县', '1146:1146:靖边', '1032:1032:江川县', '1038:1038:江华瑶族自治县', '1028:1028:吉安县',
                 '1029:1029:吉水县', '1059:1059:晋宁县', '1061:1061:江永', '1085:1085:建水县', '1153:1153:嘉鱼县', '1188:1188:祁县',
                 '1194:1194:精河县', '1197:1197:靖西县', '114:114:昆明', '235:235:开封', '403:403:昆山', '396:396:喀什地区',
                 '388:388:克拉玛依', '502:502:开平', '603:603:库尔勒', '643:643:奎屯', '748:748:开州区', '880:880:垦利', '925:925:宽城',
                 '1002:1002:开阳', '990:990:开化', '106:106:廊坊', '137:137:临汾', '138:138:吕梁', '157:157:辽阳', '163:163:辽源',
                 '179:179:连云港', '203:203:六安', '192:192:丽水', '211:211:龙岩', '236:236:洛阳', '232:232:聊城', '230:230:临沂',
                 '229:229:莱芜', '242:242:漯河', '274:274:娄底', '304:304:泸州', '310:310:乐山', '290:290:柳州', '300:300:来宾',
                 '336:336:临沧', '345:345:拉萨', '322:322:六盘水', '321:321:凉山', '334:334:丽江', '372:372:临夏', '371:371:陇南',
                 '361:361:兰州', '476:476:兰溪', '461:461:临海', '450:450:溧阳', '509:509:耒阳', '492:492:龙口', '567:567:陆丰',
                 '561:561:莱阳', '513:513:乐昌', '529:529:莱州', '542:542:临安', '537:537:临清', '611:611:乐陵', '618:618:龙海',
                 '619:619:醴陵', '617:617:浏阳', '620:620:莱西', '628:628:廉江', '634:634:阆中', '632:632:乐平', '596:596:灵宝',
                 '606:606:冷水江', '683:683:连州', '675:675:灵山', '674:674:滦南', '690:690:临江', '688:688:陵水', '652:652:鹿泉',
                 '655:655:利川', '670:670:凌海', '659:659:老河口', '745:745:滦县', '744:744:乐亭', '739:739:临朐', '766:766:栾城',
                 '724:724:连江', '823:823:隆昌', '815:815:林州', '808:808:临潼', '809:809:蓝田', '791:791:临漳', '789:789:灵石',
                 '786:786:鲁山', '889:889:临猗', '868:868:柳河', '839:839:鹿邑', '951:951:临沭', '939:939:兰陵', '938:938:龙游',
                 '935:935:栾川', '934:934:雷州', '930:930:隆尧', '919:919:陵川', '912:912:龙泉', '905:905:临邑', '902:902:利津',
                 '896:896:梁山', '1010:1010:澧县', '1011:1011:辽中', '976:976:涟水', '1119:1119:临澧', '1110:1110:兰考县',
                 '1133:1133:灵丘县', '1121:1121:利辛', '1147:1147:洛川县', '1144:1144:泸县', '1143:1143:溧水区', '1138:1138:禄丰县',
                 '1034:1034:罗平县', '1037:1037:涟源市', '1040:1040:庐江县', '1064:1064:隆回', '1056:1056:临颍', '1060:1060:蓝山',
                 '1083:1083:隆化县', '1087:1087:洛宁', '1073:1073:芦溪', '1079:1079:卢氏县', '1163:1163:罗定市', '1171:1171:乐东',
                 '1178:1178:梁平', '1183:1183:临高县', '1184:1184:罗源县', '175:175:牡丹江', '194:194:马鞍山', '279:279:茂名',
                 '282:282:梅州', '306:306:绵阳', '312:312:眉山', '566:566:密山', '563:563:漠河', '572:572:满洲里', '610:610:明光',
                 '584:584:梅河口', '694:694:孟州', '668:668:麻城', '872:872:渑池', '848:848:眉县', '860:860:民权', '838:838:孟津',
                 '846:846:牟平', '944:944:蒙阴', '906:906:绵竹', '1116:1116:蒙自市', '1122:1122:蒙城', '1222:1222:明水县',
                 '1216:1216:米易县', '1219:1219:闽侯县', '1210:1210:勐腊县', '51:51:宁波', '55:55:南京', '83:83:南昌', '82:82:南通',
                 '99:99:南宁', '212:212:宁德', '210:210:南平', '244:244:南阳', '309:309:内江', '311:311:南充', '343:343:怒江',
                 '547:547:南沙', '512:512:宁海', '520:520:宁乡', '621:621:南安', '687:687:南雄', '682:682:讷河', '741:741:南乐',
                 '820:820:宁津', '813:813:宁晋', '775:775:南陵', '781:781:宁国', '779:779:宁阳', '931:931:内丘', '1013:1013:南和',
                 '979:979:内黄', '1112:1112:宁陵', '1053:1053:南部县', '1075:1075:南皮县', '1224:1224:宁远县', '1166:1166:嫩江县',
                 '158:158:盘锦', '207:207:莆田', '214:214:萍乡', '237:237:平顶山', '240:240:濮阳', '303:303:攀枝花', '335:335:普洱',
                 '367:367:平凉', '493:493:邳州', '546:546:普宁', '524:524:平湖', '582:582:平度', '585:585:彭州', '587:587:蓬莱',
                 '701:701:鄱阳', '761:761:磐石', '730:730:浦江', '805:805:平潭', '777:777:平原', '893:893:平山', '849:849:濮阳县',
                 '833:833:沛县', '837:837:蒲城', '842:842:盘县', '847:847:平江', '950:950:平邑', '987:987:平遥', '991:991:平果',
                 '972:972:平阳', '960:960:平舆', '1106:1106:平罗县', '1156:1156:平阴县', '1214:1214:平昌县', '60:60:青岛',
                 '110:110:泉州', '109:109:齐齐哈尔', '122:122:秦皇岛', '174:174:七台河', '189:189:衢州', '286:286:清远', '294:294:钦州',
                 '326:326:黔西南', '330:330:曲靖', '328:328:黔东南', '329:329:黔南', '369:369:庆阳', '430:430:迁安', '418:418:琼海',
                 '507:507:曲阜', '500:500:启东', '496:496:青州', '550:550:潜江', '644:644:沁阳', '647:647:邛崃', '740:740:清丰',
                 '727:727:齐河', '864:864:淇县', '865:865:全椒', '929:929:清河', '922:922:青田', '914:914:栖霞', '1020:1020:青县',
                 '1004:1004:潜山', '998:998:庆云', '1089:1089:祁东县', '1115:1115:杞县', '1107:1107:庆安县', '1131:1131:青冈县',
                 '1139:1139:岐山县', '1220:1220:青阳县', '228:228:日照', '348:348:日喀则', '475:475:仁怀', '469:469:瑞安',
                 '501:501:如皋', '497:497:荣成', '499:499:乳山', '616:616:汝州', '639:639:瑞金', '657:657:瑞昌', '749:749:仁寿',
                 '917:917:任丘', '988:988:如东', '966:966:汝阳', '1101:1101:容县', '1095:1095:汝城县', '1114:1114:荣昌区', '10:10:上海',
                 '30:30:深圳', '66:66:沈阳', '76:76:石家庄', '80:80:苏州', '111:111:三亚', '117:117:汕头', '133:133:朔州',
                 '171:171:双鸭山', '162:162:四平', '166:166:松原', '187:187:绍兴', '184:184:宿迁', '177:177:绥化', '201:201:宿州',
                 '221:221:上饶', '208:208:三明', '251:251:十堰', '245:245:商丘', '243:243:三门峡', '276:276:韶关', '283:283:汕尾',
                 '260:260:随州', '266:266:邵阳', '308:308:遂宁', '383:383:石嘴山', '360:360:商洛', '408:408:石河子', '406:406:顺德',
                 '440:440:石狮', '456:456:上虞', '495:495:寿光', '487:487:神农架', '569:569:韶山', '532:532:射阳', '531:531:沭阳',
                 '530:530:嵊州', '538:538:三河', '613:613:沙河', '633:633:四会', '648:648:松滋', '669:669:舒兰', '736:736:邵东',
                 '762:762:沙湾', '760:760:泗阳', '755:755:睢县', '819:819:石泉', '830:830:单县', '824:824:泗洪', '804:804:上高',
                 '797:797:绥中', '796:796:神木', '768:768:涉县', '886:886:上蔡', '895:895:遂昌', '875:875:睢宁', '840:840:沈丘',
                 '845:845:三门', '953:953:什邡', '955:955:上杭', '907:907:石岛', '1017:1017:泗水', '1022:1022:社旗', '1015:1015:商河',
                 '992:992:射洪', '982:982:舒城', '965:965:嵩县', '1118:1118:石门', '1113:1113:桑植', '1108:1108:商城县',
                 '1120:1120:鄯善县', '1039:1039:深州市', '1024:1024:泗县', '1055:1055:商水县', '1045:1045:上林县', '1067:1067:遂川',
                 '1071:1071:上栗', '1062:1062:双峰', '1081:1081:肃宁县', '1077:1077:莎车县', '1155:1155:绥德县', '1158:1158:沙县',
                 '1176:1176:深泽县', '1180:1180:石柱', '1189:1189:邵武', '1192:1192:寿县', '1211:1211:三台县', '40:40:天津',
                 '101:101:太原', '121:121:唐山', '143:143:通辽', '159:159:铁岭', '164:164:通化', '191:191:台州', '183:183:泰州',
                 '196:196:铜陵', '226:226:泰安', '325:325:铜仁', '352:352:铜川', '364:364:天水', '399:399:塔城', '389:389:吐鲁番',
                 '432:432:太仓', '425:425:桐乡', '503:503:台山', '482:482:腾冲', '549:549:滕州', '554:554:桐庐', '518:518:泰兴',
                 '626:626:天长', '578:578:天门', '673:673:桐城', '666:666:洮南', '743:743:台前', '759:759:太和', '817:817:汤阴',
                 '812:812:藤县', '790:790:太谷', '782:782:天台', '879:879:土默特右旗', '947:947:铜梁', '942:942:郯城', '1009:1009:桃源',
                 '962:962:同安', '1111:1111:通许县', '1135:1135:通榆县', '1132:1132:通海县', '1136:1136:唐河', '1030:1030:泰和县',
                 '1054:1054:太康县', '1041:1041:铜鼓', '1044:1044:田东县', '1215:1215:通江县', '52:52:无锡', '57:57:武汉',
                 '102:102:芜湖', '112:112:温州', '141:141:乌海', '147:147:乌兰察布', '227:227:威海', '224:224:潍坊', '291:291:梧州',
                 '339:339:文山', '355:355:渭南', '365:365:武威', '387:387:乌鲁木齐', '384:384:吴忠', '443:443:武夷山', '433:433:吴江',
                 '428:428:万州', '479:479:婺源', '457:457:温岭', '449:449:武安', '498:498:文登', '551:551:乌镇', '592:592:吴川',
                 '607:607:文昌', '684:684:舞钢', '680:680:万宁', '696:696:温县', '697:697:武陟', '667:667:武穴', '747:747:乌苏',
                 '826:826:卫辉', '773:773:芜湖县', '769:769:无为', '850:850:乌拉特前旗', '926:926:围场', '904:904:武城', '898:898:汶上',
                 '897:897:微山', '1019:1019:无极', '1023:1023:万荣', '1014:1014:舞阳', '1006:1006:威宁', '995:995:武鸣',
                 '973:973:武义', '967:967:瓦房店', '1109:1109:尉氏县', '1128:1128:武隆县', '1025:1025:万载', '1049:1049:武平县',
                 '1046:1046:威县', '1223:1223:武冈市', '1217:1217:望奎县', '1187:1187:五常市', '1207:1207:旺苍县', '42:42:西安',
                 '62:62:厦门', '103:103:新乡', '119:119:徐州', '124:124:邢台', '136:136:忻州', '148:148:兴安盟', '149:149:锡林郭勒',
                 '206:206:宣城', '215:215:新余', '253:253:襄阳', '246:246:信阳', '241:241:许昌', '275:275:湘西', '259:259:咸宁',
                 '256:256:孝感', '264:264:湘潭', '340:340:西双版纳', '374:374:西宁', '354:354:咸阳', '412:412:仙桃', '484:484:香格里拉',
                 '548:548:新沂', '556:556:新密', '557:557:荥阳', '555:555:新郑', '562:562:兴宁', '560:560:西塘', '574:574:新民',
                 '517:517:兴化', '525:525:湘阴', '523:523:新泰', '534:534:响水', '543:543:辛集', '614:614:湘乡', '580:580:项城',
                 '604:604:孝义', '695:695:修武', '692:692:象山', '641:641:兴城', '661:661:兴平', '764:764:仙居', '728:728:夏津',
                 '729:729:信宜', '734:734:新化', '818:818:新安', '828:828:新乡县', '802:802:宣威', '810:810:霞浦', '776:776:襄垣',
                 '885:885:西平', '892:892:新乐', '870:870:西乡', '853:853:徐闻', '857:857:夏邑', '863:863:浚县', '843:843:盱眙',
                 '957:957:香河', '959:959:信丰', '949:949:浠水', '936:936:西华', '920:920:薛城', '903:903:新昌', '1021:1021:淅川',
                 '996:996:溆浦', '961:961:新蔡', '1129:1129:秀山土家族苗族自治县', '1123:1123:新洲区', '1149:1149:仙游县', '1137:1137:新野',
                 '1033:1033:兴国县', '1036:1036:新田', '1026:1026:新干', '1051:1051:祥云县', '1050:1050:寻乌县', '1057:1057:襄城县',
                 '1063:1063:新宁', '1082:1082:献县', '1167:1167:新津县', '1213:1213:旬阳县', '104:104:烟台', '120:120:扬州',
                 '130:130:阳泉', '135:135:运城', '155:155:营口', '168:168:延边', '172:172:伊春', '181:181:盐城', '216:216:鹰潭',
                 '219:219:宜春', '252:252:宜昌', '272:272:永州', '285:285:阳江', '267:267:岳阳', '270:270:益阳', '313:313:宜宾',
                 '316:316:雅安', '289:289:云浮', '296:296:玉林', '331:331:玉溪', '382:382:银川', '356:356:延安', '358:358:榆林',
                 '405:405:义乌', '398:398:伊犁', '470:470:乐清', '466:466:阳朔', '459:459:余姚', '458:458:永康', '454:454:宜兴',
                 '453:453:兖州', '559:559:扬中', '516:516:伊川', '514:514:英德', '522:522:仪征', '528:528:偃师', '608:608:禹城',
                 '609:609:禹州', '622:622:伊宁', '625:625:宜城', '637:637:原平', '577:577:永城', '597:597:永济', '693:693:玉环',
                 '656:656:宜都', '658:658:沅江', '763:763:永年', '733:733:永川', '822:822:阎良', '829:829:原阳', '803:803:易县',
                 '814:814:宜阳', '784:784:叶县', '770:770:阳城', '778:778:云阳', '884:884:郓城', '876:876:玉山', '878:878:阳谷',
                 '859:859:虞城', '958:958:于都', '940:940:沂水', '943:943:沂南', '908:908:杨凌', '901:901:伊金霍洛旗', '1096:1096:攸县',
                 '1099:1099:永顺县', '1094:1094:永兴县', '1127:1127:酉阳土家族苗族自治县', '1151:1151:应县', '1027:1027:宜丰',
                 '1043:1043:营山县', '1047:1047:永安', '1069:1069:永丰', '1058:1058:鄢陵', '1072:1072:永新', '1218:1218:宜良县',
                 '1159:1159:阳山县', '1160:1160:榆树市', '1162:1162:沅陵县', '1169:1169:永登县', '1181:1181:鱼台县', '1182:1182:宜州市',
                 '1186:1186:义马市', '1199:1199:盂县', '1198:1198:永嘉县', '73:73:郑州', '81:81:淄博', '108:108:珠海', '113:113:中山',
                 '125:125:张家口', '190:190:舟山', '182:182:镇江', '222:222:枣庄', '209:209:漳州', '248:248:驻马店', '247:247:周口',
                 '278:278:湛江', '280:280:肇庆', '263:263:株洲', '269:269:张家界', '318:318:资阳', '302:302:自贡', '323:323:遵义',
                 '333:333:昭通', '366:366:张掖', '386:386:中卫', '426:426:涿州', '419:419:张家港', '474:474:增城', '468:468:诸暨',
                 '465:465:章丘', '508:508:邹平', '494:494:枣阳', '558:558:庄河', '526:526:诸城', '612:612:钟祥', '586:586:招远',
                 '591:591:遵化', '654:654:枝江', '671:671:樟树', '663:663:漳浦', '757:757:正定', '821:821:中牟', '891:891:准格尔旗',
                 '858:858:柘城', '834:834:邹城', '841:841:赵县', '1007:1007:织金', '997:997:芷江', '985:985:周至', '1093:1093:资兴市',
                 '1140:1140:扎兰屯市', '1048:1048:漳平', '1179:1179:忠县', '1196:1196:柘荣', '1200:1200:中江县']

    def listTOdict(self, listinfo):
        dicts = []
        for i in listinfo:
            cityinfo = {}
            cityinfolist = str(i).split(':')
            cityinfo['city_id'] = cityinfolist[0]
            cityinfo['city_name'] = cityinfolist[-1]
            cityinfo['last_update_time'] = str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
            dicts.append(cityinfo)
        return dicts


class DataSave:

    def connectionDB(self):
        import pymysql
        conn = pymysql.connect(
            host='192。168.30.111',
            port=3306,
            user='root',
            passwd='123456',
            charset='utf8',
            database='spiderInc'
        )
        return conn

    @Tools.async
    def execSQL(self, sql):
        conn = DataSave.connectionDB(DataSave)
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return res

    @Tools.async
    def savechannel(self, execlist: list):
        if len(execlist) == 0:
            print('当前没有数据要执行')
        else:
            for execinfo in execlist:
                try:
                    DataSave.execSQL(DataSave, execinfo)
                    execlist.remove(execinfo)
                except:
                    print('[ Error ]' + str(execinfo) + '执行失败')


if __name__ == '__main__':
    nowdatetime = str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    print('爬虫开始%s' % nowdatetime)
    filepath = './cinemainfo-%s.txt' % str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    filepath2 = './platforms-%s.txt' % str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    # addrinfo = GetResponse.getaddressinfo(GetResponse)
    # print(addrinfo)

    city = Information.listTOdict(Information, Information.city_info)
    citysql = Tools.mysqlAllbuild(Tools, city, 'maoyan_city_info')
    # print(citysql)
    DataSave.execSQL(DataSave, citysql)

    cinemalinklist = GetResponse.getcinemaslink(GetResponse)
    # print(cinemalinklist)

    for cinemalink in cinemalinklist:
        cinemainfo = GetResponse.getcinemapageinfo(GetResponse, cinemalink)[0]
        print('正在获取 %s 影院的数据' % str(cinemainfo['cinema_name']))
        cinemainfoSQL = Tools.mysqlbuild(Tools, cinemainfo, 'maoyan_cinema_info')

        DataSave.execSQL(DataSave, cinemainfoSQL)
        # with open(filepath, 'a+', encoding='utf-8') as f:
        #     f.writelines(str(cinemainfoSQL) + '\n')

        cinemashowes = GetResponse.getcinemapageinfo(GetResponse, cinemalink)[1]

        try:
            showSQL = Tools.mysqlAllbuild(Tools, cinemashowes, 'maoyan_show_info')
        except:
            print('构建sql失败，源数据为：')
            print(cinemashowes)
            print('影院地址为：%s' % str(cinemalink))
            continue

        DataSave.execSQL(DataSave, showSQL)
        # with open(filepath2, 'a+', encoding='utf-8') as f1:
        #     f1.writelines(str(sqls) + '\n')
        # 按行生成sql
        # for cinemashow in cinemashowes:
        #     cinemashowSQL = Tools.mysqlbuild(Tools, cinemashow, 'maoyan_show_info')
        #     with open(filepath, 'a+',encoding='utf-8') as f:
        #         f.writelines(str(cinemashowSQL)+'\n')

    # f.close()
    # f1.close()
    enddatetime = str(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S'))
    print('爬虫结束%s' % enddatetime)
