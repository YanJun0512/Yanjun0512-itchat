import itchat
import time
import requests
import hashlib
import re
import CallGrades
import FaceRecognition

# 图灵机器人api


def get_response(msg, FromUserName):
    msg_match = re.match(r'^成绩(\d{15})(.*)$', msg)
    if msg_match:
        username = msg_match.group(1)
        password = msg_match.group(2)
        return CallGrades.query_grades(username, password, 2017, 3)

    api_url = 'http://www.tuling123.com/openapi/api'
    apikey = 'cb7ef07f100a4a73a192685bd52f116b'
    hash = hashlib.md5()
    userid = hash.update(FromUserName.encode('utf-8'))
    # print('userid=', userid)
    data = {'key': apikey,
            'info': msg,
            'userid': userid
            }
    try:
        req = requests.post(api_url, data=data).json()
        return req.get('text')
    except:
        return

itchat.auto_login()
swatch = 1
# 个人聊天


@itchat.msg_register(['Text', 'Map', 'Card', 'Note', 'Sharing'])
def Tuling_robot(msg):
    print('发送者：', msg['FromUserName'])
    response = get_response(msg['Content'], msg['FromUserName'])
    itchat.send(response, msg['FromUserName'])


# 返回图片录音视频


@itchat.msg_register(['Recording', 'Attachment', 'Video'])
def download_files(msg):
    fileDir = '%s%s'%(msg['Type'], int(time.time()))
    msg['Text'](fileDir)
    itchat.send('%s received 2333' % msg['Type'], msg['FromUserName'])
    itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'file', fileDir), msg['FromUserName'])


@itchat.msg_register(['Picture'])
def how_old(msg):
    fileDir = '%s%s.jpg' % (msg['Type'], int(time.time()))
    msg['Text'](fileDir)

    try:
        ans = FaceRecognition.Face(fileDir)
        itchat.send(ans, msg['FromUserName'])
    except:
        itchat.send('你长得真好看~', msg['FromUserName'])
        itchat.send('%s received 2333' % msg['Type'], msg['FromUserName'])
        itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'file', fileDir), msg['FromUserName'])


# 同意陌生人好友申请

@itchat.msg_register(['Friend'])
def add_friend(msg):
    itchat.add_friend(msg)
    itchat.send_msg('Nice To Meet You !', msg['RecommendInfo']['UserName'])



# 群聊
Message = '震惊！西大官微居然做出这种事'
GroupsContainer = set()

'''
@itchat.msg_register('Text', isGroupChat=True)
def broadcast(msg):
    response = get_response(msg['Content'], msg['FromUserName'])
    itchat.send(response, msg['FromUserName'])
    print('发送群：', msg['FromUserName'])
    groups_json_list = itchat.get_chatrooms()
    groupsName = [nm.get('UserName') for nm in groups_json_list]
    groupsName = set(groupsName)
    for grpn in groupsName:
        GroupsContainer.add(grpn)
    current_time = time.localtime(time.time())
    if (current_time.tm_hour == 15 and swatch == 1):
        for grn in GroupsContainer:
            itchat.send(Message, grn)
        swatch = 0'''

if __name__ == '__main__':
    itchat.run()
