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
# @File  : Mtime_spider.py
# @Author: huguangzhi
# @ContactEmail : huguangzhi@ucsdigital.com.com 
# @ContactPhone : 13121961510 
# @Date  : 2018-07-30 - 09:19
# @Desc  : 第一版时光网爬虫，爬虫写的比较low，涉及的内容比较乱。
#          主要爬取的是影片详情页的内容，入库到SQLSERVER 和 MYSQL两种方式

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : access.py
# @Author: huguangzhi
# @ContactEmail : huguangzhi@ucsdigital.com
# @ContactPhone : 13121961510
# @Date  : 2018-04-28
# @Desc  : 爬虫获取即将上映的影片的信息，信息内容为Mtime网站上显示出来的相关信息，使用相关数据需要及时整理对应内容
import datetime
import html
import json
import pymssql
import random
import re
from urllib.request import urlopen
import pymysql
import time

# conn = pymysql.connect(host='192.168.30.111',
#                        user='root',
#                        passwd='123456',
#                        port=3306,
#                        db='spiderInc',
#                        charset='utf8')

# 链接sqlserver
conn = pymssql.connect(host="192.168.30.43",
                       user="sa",
                       password="SQLServer2008",
                       database="CH_NMSDB_20180607")


# #获取影片页面基本信息，传入参数为Mtime的movie_id，返回值为数据库的列明和值
def getMovieContent(x, page):
    Url = r'http://movie.mtime.com/%d/' % x
    # movie = urlopen(Url)
    # page = str(page, 'utf-8')
    # print(page)
    # 1 影片名称
    MovieNameReg = 'property="v:itemreviewed">(.*?)</h1>'
    MovieName = str(html.unescape(re.findall(MovieNameReg, page)[0]))
    # 2影片别名
    try:
        MovieNameOtherReg = '<p class="db_enname" style="font-size:25px;">(.*?)</p>'
        MovieNameOther = re.findall(MovieNameOtherReg, page, re.S)[0]
    except:
        MovieNameOther = '-'

    # 3影片海报
    MoviePostReg = '<img src="(.*?)" alt=".*?" rel="v:image" />'
    try:
        MoviePost = re.findall(MoviePostReg, page)[0]
    except:
        MoviePost = '-'

    # 4影片类型(多个)
    MovieTypeReg = 'property="v:genre">(.*?)</a>'
    MovieType = str(re.findall(MovieTypeReg, page)).replace('[', '').replace(']', '').replace('\'', '').replace(' ',
                                                                                                                '').replace(
        ',', '/')
    # MovieType = str(re.findall(MovieTypeReg, page)).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')

    # 5影片上映时间
    ReleasedDateReg = 'property="v:initialReleaseDate" content="(.*?)">'
    try:
        ReleasedDate = re.findall(ReleasedDateReg, page)[0]
    except:
        ReleasedDate = '-'

    # 6上映地区
    ReleasedAreaReg = 'property="v:initialReleaseDate" content=".*?">.*?</a>(.*?)上映</div>'
    try:
        ReleasedArea = re.findall(ReleasedAreaReg, page, re.S)[0]
    except:
        ReleasedArea = '-'

    # 7影片产地-GG <a href="http://movie.mtime.com/movie/search/section/?nation=Italy" target="_blank">意大利</a>
    MovieNationReg = r'<a href="http://movie.mtime.com/movie/search/section/\?nation=.*?" target="_blank">(.*?)</a>'
    try:
        MovieNation = html.unescape(re.findall(MovieNationReg, page, re.M)[0])
    except:
        MovieNation = '-'

    # 8导演
    try:
        MovieDirectorReg = ' rel="v:directedBy">(.*?)</a>'
        MovieDirector = html.unescape(
            str(re.findall(MovieDirectorReg, page)).replace('[', '').replace(']', '').replace('\'', '').replace(' ',
                                                                                                                '')).replace(
            ',', '，')

    except:
        MovieDirector = '-'
    # 9编剧 人员
    try:
        ScreenWriterReg = '  <a href="http://people.mtime.com/.*?/" target="_blank">(.*?)</a>'
        ScreenWriter = html.unescape(
            str(re.findall(ScreenWriterReg, page)).replace('[', '').replace(']', '').replace('\'', '').replace(' ',
                                                                                                               '').replace(
                ',', '，'))

    except:
        ScreenWriter = '-'

    # 10发行公司
    DistributionEnterpriseReg = '<a href="http://movie.mtime.com/company/.*?/" target="_blank">(.*?)</a>'
    try:
        DistributionEnterprise = str(html.unescape(re.findall(DistributionEnterpriseReg, page)[0]))
    except:
        DistributionEnterprise = '-'

        # 11剧情介绍(要求，去除段首的空格)
    MoviePlotReg = '<p class="mt6 lh18">(.*?)</p>'
    try:
        MoviePlot = str(html.unescape(
            str(re.findall(MoviePlotReg, page, re.S)[0]).replace('\r\n', '').replace('　', '').replace(' ', '')))
    except:
        MoviePlot = '-'

    # 12上映年份
    ReleasedYearReg = '<a  style="font-size:30px;" href=".*?" target="_blank">(.*?)</a>'
    try:
        ReleasedYear = str(re.findall(ReleasedYearReg, page)[0])
    except:
        ReleasedYear = '-'
    # ----------可以套用方法了

    # 13影片视频数量
    TrailerNumReg = '<span>(.*?)</span> 个视频</a>'
    TrailerUrlUrl = 'href="(.*?)"><span>.*?</span> 个视频</a><i>&nbsp;</i></dd>'
    TrailerNum = str(getNumUrl(page, TrailerNumReg, TrailerUrlUrl)[0])

    # 14影片视频详情url
    TrailerUrl = str(getNumUrl(page, TrailerNumReg, TrailerUrlUrl)[1])

    # 15演员数量
    ActorNumReg = '<span>(.*?)</span> 位演职员</a><i>&nbsp;</i></dd>'
    ActorUrlReg = '<a href="(.*?)"><span>.*?</span> 位演职员</a><i>&nbsp;</i></dd>'
    ActorNum = str(getNumUrl(page, ActorNumReg, ActorUrlReg)[0])

    # 16演员详情网页
    ActorUrl = str(getNumUrl(page, ActorNumReg, ActorUrlReg)[1])

    # 17图片数量
    ImageNumReg = '<span>(.*?)</span> 张图片</a><i>&nbsp;</i></dd>'
    ImageUrlReg = '<a href="(.*?)"><span>.*?</span> 张图片</a><i>&nbsp;</i></dd>'
    ImageNum = str(getNumUrl(page, ImageNumReg, ImageUrlReg)[0])

    # 18图片详情网页
    ImageUrl = str(getNumUrl(page, ImageNumReg, ImageUrlReg)[1])

    # 19影评数量
    CommentNumReg = '<span property="v:count" content=".*?">(.*?)</span> 条影评</a><i>&nbsp;</i></dd>'
    CommentUrlReg = '<a href="(.*?)"><span property="v:count" content=".*?">.*?</span> 条影评</a><i>&nbsp;</i></dd>'
    CommentNum = str(getNumUrl(page, CommentNumReg, CommentUrlReg)[0])

    # 20长影评网页
    CommentUrl = str(getNumUrl(page, CommentNumReg, CommentUrlReg)[1])

    # 21短影评网页
    CommentShortUrl = Url + 'reviews/short/new.html'

    # 22影片新闻数量
    NewsUrlNumReg = '<span>(.*?)</span> 条新闻</a><i>&nbsp;</i></dd>'
    NewsUrlReg = '<a href="(.*?)"><span>.*?</span> 条新闻</a><i>&nbsp;</i></dd>'
    NewsNum = str(getNumUrl(page, NewsUrlNumReg, NewsUrlReg)[0])
    # 22影片新闻数量
    NewsUrl = str(getNumUrl(page, NewsUrlNumReg, NewsUrlReg)[1])

    key = "'Movie_url','MovieName','MovieNameOther','MoviePost','MovieType','ReleasedDate','ReleasedArea','MovieNation','MovieDirector','ScreenWriter','DistributionEnterp','MoviePlot','ReleasedYear','TrailerNum','TrailerUrl','ActorNum','ActorUrl','ImageNum','ImageUrl','CommentNum','CommentUrl','CommentShortUrl','NewsNum','NewsUrl'"
    value = (
        Url, MovieName, MovieNameOther, MoviePost, MovieType, ReleasedDate, ReleasedArea, MovieNation, MovieDirector,
        ScreenWriter, DistributionEnterprise, MoviePlot, ReleasedYear, TrailerNum, TrailerUrl, ActorNum, ActorUrl,
        ImageNum,
        ImageUrl, CommentNum, CommentUrl, CommentShortUrl, NewsNum, NewsUrl)
    return key, value

    '''" \
              "movie_id," \
              "Movie_url," \
              "MovieName," \
              "MovieNameOther," \
              "MoviePost," \
              "MovieType," \
              "ReleasedDate," \
              "ReleasedArea," \
              "MovieNation," \
              "MovieDirector," \
              "ScreenWriter," \
              "DistributionEnterprise," \
              "MoviePlot," \
              "ReleasedYear," \
              "WantSeeNum," \
              "MarkNum," \
              "Score," \
              "TrailerNum," \
              "TrailerUrl," \
              "ActorNum," \
              "ActorUrl," \
              "ImageNum," \
              "ImageUrl," \
              "CommentNum," \
              "CommentUrl," \
              "CommentShortUrl," \
              "NewsNum," \
              "NewsUrl'''

    '''           int(x), str(MovieUrl), str(MovieName), str(MovieNameOther), str(MoviePost), str(MovieType),
                  str(ReleasedDate), str(ReleasedArea), str(MovieNation), str(MovieDirector), str(ScreenWriter),
                  str(DistributionEnterprise), str(MoviePlot), str(ReleasedYear), str(WantSeeNum), str(MarkNum),
                  str(Score),
                  str(TrailerNum), str(TrailerUrl), str(ActorNum), str(ActorUrl), str(ImageNum), str(ImageUrl),
                  str(CommentNum), str(CommentUrl), str(CommentShortUrl), str(NewsNum), str(NewsUrl)'''


# 获取影片评分信息，传入参数为Mtime的movie_id，返回值为数据库的列明和值
def getRatings(x):
    """
    该方法为获取影片评分和时光票房信息
    :param x:需要传入影片ID
    :return:
            返回信息结果为元祖的形式
    """
    # http://service.library.mtime.com/Movie.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&Ajax_CallBackArgument0=219106&Ajax_CallBackMethod=GetMovieOverviewRating
    '''信息展示
    isRelease 上映情况
    movieRating 影片评级信息 【】
        MovieId         影片id  int
        RatingFinal     影片评分 int
        RDirectorFinal  导演评分 int
        ROtherFinal     音乐评分 int
        RPictureFinal   画面评分 int
        RShowFinal
        RStoryFinal     故事情节评分 int
        RTotalFinal
        Usercount       参与评分人数 int
        AttitudeCount   想看人数 int
        UserId
        EnterTime
        JustTotal
        RatingCount
        TitleCn
        TitleEn
        Year
        Id
    movieTitle  影片名
    tweetId
    userLastComment
    userLastCommentUrl
    releaseType 上映情况 1是已经上映，0是未上映
    boxOffice   票房信息   【】
        Rank                    当前影片总票房排名 int
        TotalBoxOffice          当前票房总计
        TotalBoxOfficeUnit      单位
        TodayBoxOffice          实时票房总计
        TodayBoxOfficeUnit      单位
        ShowDays                上映天数 int
        EndDate                 统计时间 (每五分钟更新一次)
        FirstDayBoxOffice       上映首日票房
        FirstDayBoxOfficeUnit   单位
    '''
    try:
        ratingsurl = 'http://service.library.mtime.com/Movie.api?Ajax_CallBack=true&Ajax_CallBackType=Mtime.Library.Services&Ajax_CallBackArgument0=%d&Ajax_CallBackMethod=GetMovieOverviewRating' % x
        movie = urlopen(ratingsurl)
        page = str(movie.read(), 'utf-8').replace('var movieOverviewRatingResult = ', '').replace(';', '')
        # 接口返回内容
        result = json.loads(page)['value']
        # 影片评级信息
        movieRating = result['movieRating']
        # =======================↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓以下为数据信息↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓=============================
        movie_Id = str(x)
        # 评级信息内容-影片评分
        try:
            RatingFinal = str(movieRating['RatingFinal'])
        except:
            RatingFinal = '-'
        # 评级信息内容-参与评分人数
        try:
            Usercount = str(movieRating['Usercount'])
        except:
            Usercount = '-'
        # 评级信息内容-想看影片人数
        try:
            AttitudeCount = str(movieRating['AttitudeCount'])
        except:
            AttitudeCount = '-'
        # =======================↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑以上为数据信息↑↑↑↑↑↑↑↑↑↑↑↑↑↑=============================
        # 影片票房信息

        try:
            boxOffice = result['boxOffice']
        except:
            boxOffice = ''

        # =======================↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓以下为数据信息↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓=============================
        # 影片票房信息-当前影片总票房排名
        try:
            Rank = str(boxOffice['Rank'])
        except:
            Rank = '-'
        # 影片票房信息-当前票房总计
        try:
            TotalBoxOffice = str(boxOffice['TotalBoxOffice']) + str(boxOffice['TotalBoxOfficeUnit'])
        except:
            TotalBoxOffice = '-'
        # 影片票房信息-实时票房总计
        try:
            TodayBoxOffice = str(boxOffice['TodayBoxOffice']) + str(boxOffice['TodayBoxOfficeUnit'])
        except:
            TodayBoxOffice = '-'
        # 影片票房信息-上映天数
        try:
            ShowDays = str(boxOffice['ShowDays'])
        except:
            ShowDays = '-'
        # 影片票房信息-统计时间(每五分钟更新)
        try:
            EndDate = str(boxOffice['EndDate'])
        except:
            EndDate = '-'
        # 影片票房信息-上映首日票房
        try:
            FirstDayBoxOffice = str(boxOffice['FirstDayBoxOffice']) + str(boxOffice['FirstDayBoxOfficeUnit'])
        except:
            FirstDayBoxOffice = '-'
        # 上映情况
        try:
            releaseType = str(result['releaseType'])
        except:
            releaseType = '-'
        # =======================↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑以上为数据信息↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑=============================
        # 输出信息
        key = "'movie_id','RatingFinal','Usercount','AttitudeCount','Rank','TotalBoxOffice','TodayBoxOffice','ShowDays','EndDate','FirstDayBoxOffice','releaseType'"
        value = (
        movie_Id, RatingFinal, Usercount, AttitudeCount, Rank, TotalBoxOffice, TodayBoxOffice, ShowDays, EndDate,
        FirstDayBoxOffice, releaseType)
        return key, value
    except Exception as f:
        print(str(x) + '### Error-000004 ' + f)
        pass


# 通过正则过滤的方法，获取影片媒介数量通用方法，返回影片媒介数量和媒介的url
def getNumUrl(page, NumReg, UrlReg):
    Num = re.findall(NumReg, page)[0]
    if int(Num.replace('+', '')) < 1:
        Url = '-'
    else:
        Url = re.findall(UrlReg, page)[0]
    return Num, Url


# 过滤网址是不是可以正常访问且网页内容包含影片信息，传入值为影片ID，返回网页文本信息
def FilterUnit(input):
    try:
        html_page_note = 'http://movie.mtime.com/%d/' % input
        html = urlopen(html_page_note)
        status = html.code
        # 判断是否能正常访问
        if status == 200:
            page = str(html.read(), encoding='utf-8')
            info404reg = '<h2 class="(.*?)">'
            try:
                info404 = re.findall(info404reg, page)[0]
                with open(r'./Error/404page.txt', 'a+') as saveError404:
                    saveError404.writelines(html_page_note + '\n')
                    print(html_page_note + '网页是404页面')
            except:
                with open(r'./Access/access.txt', 'a+') as saveAccess:
                    saveAccess.writelines(html_page_note + '\n')
                    # print(html_page_note+'可以正常访问')
                    # print(page)
                    return page
        else:
            res = '####Error-000001:网址无法正常访问.\t'
            print(res + html_page_note)
            with open(r'./Error/UnaccessUrl.txt', 'a+')as saveErrorUrl:
                saveErrorUrl.writelines(res + html_page_note + '\n')
    except Exception as errortion:
        print('Package:getMovieUrl  ID=' + str(input) + ' 出现错误 ' + str(errortion) + 'Package:getMovieUrl')
        with open(r'./Error/SystemError.txt', 'a+')as saveError:
            saveError.writelines(str(errortion) + '\n')


# 链接数据库并执行sql
def saveMoviedata(sql):
    # conn = pymysql.connect(host='192.168.30.111', user='root', passwd='123456', port=3306,
    #                        db='spiderInc', charset='utf8')
    try:
        cur = conn.cursor()
    except:
        print('-------------连接数据库失败-------------')
    # 执行sql
    else:
        try:
            # print(sql)
            # mysql执行sql语句
            cur.execute(sql)
        except:
            print('-------------sql语法错误，执行失败-------------')
            print(sql)

        else:
            conn.commit()
            # print('执行成功，数据成功写入')


# 执行sql并返回执行结果
def getSQLResult(sql):
    try:
        cur = conn.cursor()
    except:
        print('-------------连接数据库失败-------------')
    # 执行sql
    else:
        try:
            # print(sql)
            # mysql执行sql语句
            cur.execute(sql)
            # 获取数据库的内容
            result = cur.fetchall()
        except:
            print('-------------sql语法错误，执行失败-------------')
            print(sql)

        else:
            conn.commit()
            # 返回数据库的结果
            return result
            # print('执行成功，数据成功写入')


# 生成sql
def makeSql(tablename, field, value):
    # 拼串写sql
    list2 = field.strip(',').split(',')
    list1 = value.strip(',').split(',')
    # print(len(list1))
    # print(len(list2))

    line = ''
    for i in range(0, len(list1)):
        tb = list1[i] + ' as ' + list2[i]
        # print(tb)
        line = line + ',' + tb

    useing = list(line)
    useing[0] = 'select '
    using = ''.join(useing)

    lines = ''
    for i in range(0, len(list1)):

        if list2[i] == 'movie_id':
            continue
        else:
            tb = list2[i] + '=' + list1[i]
            # print(tb)
            lines = lines + ',' + tb

    updat = list(lines)
    updat[0] = ' '
    updatedata = ''.join(updat)

    newsql = "merge into " + tablename + " as a " \
                                         " using (" + using + ") as b " \
                                                              " on a.movie_id = b.movie_id " \
                                                              " when matched then " \
                                                              " update set " + updatedata + \
             " when not matched then " \
             " insert (%s)VALUES(%s);" % (field, value)
    # print('==================================================')
    # print(newsql)
    # print('==================================================')

    # mysqlsql = "insert into %s (%s)VALUES(%s);" % (tablename, field, value)
    return newsql


# 合并字段及值
def addContent(value1, value2):
    values = []
    key = (value1[0] + ',' + value2[0])
    keys = str(key).replace('\'', '')
    values.extend(list(value1[1]))
    values.extend(list(value2[1]))

    return keys, values


## 获取即将上映影片ID,数据来源时光网首页的即将上映的信息
def getupcomingRegionList(url):
    conmminRegin = urlopen(url).read()
    # print(conmminRegin)
    coming = str(conmminRegin, encoding='utf-8')
    # print(coming)
    reg = r'<div id="upcomingRegion" class="i_swwantlist" mids="(.*?)">'
    mid = re.findall(reg, coming)[0]
    movieID = eval(mid)
    return movieID


# 关联moviecode,获取影片名对应的moviecode
def connectMovieCode():
    moviename = getMovieContent.MovieName
    updateSQL = "UPDATE UCS_Mtime_MovieInfo_Page SET movie_code = (select Movie_Code from UCS_MovieInfo where Movie_official_name ='%s') WHERE MovieName = '%s'" % (
    moviename, moviename)
    return updateSQL


## 获取即将上映影片ID，数据来源于http://movie.mtime.com/comingsoon/#comingsoon
def getfulturemovieUrl():
    commingRegionUrl = 'http://movie.mtime.com/comingsoon/'
    conmminRegin = urlopen(commingRegionUrl).read()
    # print(conmminRegin)
    coming = str(conmminRegin, encoding='utf-8')
    # 过滤只需要即将上映的内容
    regPage = r'<dl class="tab1" data-index="\d+" data-parent-name="tab1">(.*?)</dl>'
    ownpage = re.findall(regPage, coming)
    pagelist = []
    for i in ownpage:
        # 过滤获取影片URLID号
        reg = r'<a href="http://movie.mtime.com/(\d+)" target="_blank">.*?</a>'
        mid = re.findall(reg, i)
        pagelist.extend(mid)
        # movieID = eval(mid)
    return set(pagelist)


if __name__ == '__main__':

    moiveIdList = getfulturemovieUrl()
    # 更新数据库中，影片图片数量错误的部分
    # imgsql = "SELECT movie_id FROM Mtime_movieinfo_page  WHERE ImageNum='http://movi' ORDER BY CONVERT(movie_id,SIGNED)"
    # imgerrlist = saveMoviedata(imgsql)
    # print(imgerrlist)
    for indext in moiveIdList:
        x = int(indext)
        # x = 255796
        print('#####################################')
        print('Start [01] : ' + str(x))
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在

        # for x in range(100000,100003):
        Content1 = None
        Content2 = None
        Content = None
        sql = None
        try:
            page = FilterUnit(x)
            # print('=== === === === ==== === ===== ===== ==== ====== == ===============')
            # print(page)
            try:

                try:
                    print('Start [02] : Filter Release Date')
                    releasedate = getMovieContent(x, page)[1][5]
                    if releasedate.split('-')[-1] == '0' or releasedate.split('-')[-2] == '0':
                        continue
                except:
                    continue
                print('Start [03] : Get Movie Content')
                Content1 = getMovieContent(x, page)


            except Exception as e:
                print(str(x) + ' [ Error-000002 ]: getMovieContent Error   ' + str(e))
                continue
            try:
                print('Start [04] : Get Ratings')
                Content2 = getRatings(x)
            except Exception as e:
                print(str(x) + ' [ Error-000003 ]: getRatings Error   ' + str(e) + '   影片不存在评分信息')
                continue
            try:
                print('Start [05] : Add Content')
                Content = addContent(Content1, Content2)
            except Exception as e:
                print(str(x) + ' [ Error-000004 ]: addContent Error   ' + str(e))
                continue
            Tbname = 'UCS_Mtime_MovieInfo_Page'
            Fields = Content[0]
            Values = str(Content[1]).replace('[', '').replace(']', '')
            # print(Values)
            try:
                print('Start [06] : Make Sql')
                sql = makeSql(tablename=Tbname, field=Fields, value=Values)
            except Exception as e:
                print(str(x) + ' [ Error-000005 ]: makeSql Error)   ' + str(e))
                continue

            try:
                print('Start [07] : Save Movie Data')
                res = saveMoviedata(sql)
                # saveMoviedata(str(connectMovieCode()))
            except Exception as e:
                print(str(x) + ' [ Error-000006 ]: saveMoviedata Error ' + str(e))
                continue
            print('[ %s ]' % str(x) + ' Keep Going ！' + str(nowTime))
        except:
            # print('解析错误:'+str(x))
            with open(r'./Error/Err.txt', 'a+')as f:
                f.writelines(str(x) + '\n')
            continue
        # time.sleep(random.randint(0, 4))

        # saveMoviedata(data)
