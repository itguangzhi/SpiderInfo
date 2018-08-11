# -*- coding: utf-8 -*-
import re
import time

import itchat
from Avideo.newVIDEO import saveDB

def getperson():
    friends = itchat.get_friends(update=True)
    friendList = []
    for f in friends:
        Finfo = {}
        Finfo['UserName'] = f['UserName']
        Finfo['NickName'] = f['NickName']
        Finfo['ContactFlag'] = f['ContactFlag']
        Finfo['MemberCount'] = f['MemberCount']
        Finfo['MemberList'] = str(f['MemberList'])
        Finfo['RemarkName'] = f['RemarkName']
        Finfo['HideInputBarFlag'] = f['HideInputBarFlag']
        Finfo['Sex'] = f['Sex']
        Finfo['Signature'] = f['Signature']
        Finfo['VerifyFlag'] = f['VerifyFlag']
        Finfo['OwnerUin'] = f['OwnerUin']
        Finfo['Statues'] = f['Statues']
        Finfo['AttrStatus'] = f['AttrStatus']
        Finfo['Province'] = f['Province']
        Finfo['City'] = f['City']
        Finfo['SnsFlag'] = f['SnsFlag']
        Finfo['UniFriend'] = f['UniFriend']
        Finfo['DisplayName'] = f['DisplayName']
        Finfo['ChatRoomId'] = f['ChatRoomId']
        Finfo['KeyWord'] = f['KeyWord']
        Finfo['IsOwner'] = f['IsOwner']
        friendList.append(Finfo)
    print(friendList)
    return friendList

# 获取当前微信号的所有群
def getroom(chatroomes):
    chatroomList = []
    for chatrooms in chatroomes:
        # print(chatrooms)
        Cinfo = {}
        Cinfo['UserName'] = chatrooms['UserName']
        Cinfo['NickName'] = filter_emoji(str(chatrooms['NickName']))
        Cinfo['MemberCount'] = chatrooms['MemberCount']
        Cinfo['HideInputBarFlag'] = chatrooms['HideInputBarFlag']
        Cinfo['Signature'] = chatrooms['Signature']
        Cinfo['VerifyFlag'] = chatrooms['VerifyFlag']
        Cinfo['RemarkName'] = chatrooms['RemarkName']
        Cinfo['Statues'] = chatrooms['Statues']
        Cinfo['AttrStatus'] = chatrooms['AttrStatus']
        Cinfo['Province'] = chatrooms['Province']
        Cinfo['City'] = chatrooms['City']
        Cinfo['SnsFlag'] = chatrooms['SnsFlag']
        Cinfo['KeyWord'] = chatrooms['KeyWord']
        Cinfo['OwnerUin'] = chatrooms['OwnerUin']
        Cinfo['isAdmin'] = chatrooms['isAdmin']

        chatroomList.append(Cinfo)
    return chatroomList


# 过滤掉名称中带有表情的符号
def filter_emoji(desstr,restr=''):
    '''
    过滤表情
    '''
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr, desstr)

# 将persion信息清洗成为可以用于存储到数据库的信息
def wishfriends(friends):
    friendList = []
    for f in friends:
        Finfo = {}
        Finfo['UserName'] = f['UserName']
        Finfo['NickName'] = filter_emoji(str(f['NickName']))
        Finfo['ContactFlag'] = f['ContactFlag']
        Finfo['MemberCount'] = f['MemberCount']
        Finfo['MemberList'] = str(f['MemberList'])
        Finfo['RemarkName'] = f['RemarkName']
        Finfo['HideInputBarFlag'] = f['HideInputBarFlag']
        Finfo['Sex'] = f['Sex']
        Finfo['Signature'] = filter_emoji(str(f['Signature'])).replace('\n', '').replace("'", '`')
        Finfo['VerifyFlag'] = f['VerifyFlag']
        Finfo['OwnerUin'] = f['OwnerUin']
        Finfo['Statues'] = f['Statues']
        Finfo['AttrStatus'] = f['AttrStatus']
        Finfo['Province'] = f['Province']
        Finfo['City'] = f['City']
        Finfo['SnsFlag'] = f['SnsFlag']
        Finfo['UniFriend'] = f['UniFriend']
        Finfo['DisplayName'] = f['DisplayName']
        Finfo['ChatRoomId'] = f['ChatRoomId']
        Finfo['KeyWord'] = f['KeyWord']
        Finfo['IsOwner'] = f['IsOwner']
        friendList.append(Finfo)
    return friendList

def savePersion(friends):
    friendList = wishfriends(friends)
    for p in friendList:
        sql = saveDB.mysqlbuild(saveDB, p, 'wx_chat_friends')
        saveDB.exec(saveDB, cur, conn, sql)
        time.sleep(1)
        print('ok')
    friendList = []

itchat.auto_login(hotReload=True)
# itchat.auto_login()

cur, conn = saveDB.connection(saveDB)



'''将人的信息存储到数据库中
# friends = itchat.get_friends(update=True)
# savePersion(friends)
'''

'''# 将群的信息存储到数据库中
chatroomes = itchat.get_chatrooms(update=True)
chatrooms = getroom(chatroomes)
for r in chatrooms:
    sql = saveDB.mysqlbuild(saveDB, r, 'wx_chat_chatrooms')
    saveDB.exec(saveDB, cur, conn, sql)
    time.sleep(1)
    print('ok')
'''
username = '@@2c0f5c652472dbe2da0279d794e0c1fdf0bc2de74d636508388568b0ee6e62ef'
file = r'‪D:\背景.png'
getmsg = itchat.get_msg()
msg = itchat.send_msg(msg=getmsg, toUserName=username)
imig = itchat.send_image(fileDir=file, toUserName=username)
print(getmsg)



itchat.run()