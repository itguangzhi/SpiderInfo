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
# @File  : Util.py
# @Author: huguangzhi
# @design: HP
# @ContactEmail : huguangzhi@ucsdigital.com.com
# @ContactPhone : 13121961510
# @Date  : 2018/8/19 - 23:15
# @Desc  : 工具包
import re
from urllib.request import urlopen
from Maoyan.getPage import GetResponse

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

    def MaoYanurlopen(self, link):
        response = urlopen(link).read()
        pageinfo = str(response, 'utf8').replace('\n', '')
        return pageinfo

        # 构建存储到mysql的入库语句
    def mysqlbuild(self, tbl):
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

            Tbname = ''
            sql = "replace into %s (%s)VALUES(%s);" % (Tbname, field, values)
            return sql