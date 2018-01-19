import re
import requests


def Face(fileDir):
    ans = '识别成功'
    url = 'face++api地址'
    api_key = '你的api_key'
    api_secret = '你的api_secret'

    data = {
        'api_key': api_key,
        'api_secret': api_secret,
        'return_landmark': 0,
        'return_attributes': 'gender,age,smiling,emotion,beauty,skinstatus',
    }
    emotion_dict = {
        'anger':'愤怒',
        'disgust':'厌恶',
        'fear':'恐惧',
        'happiness':'高兴',
        'neutral':'平静',
        'sadness':'伤心',
        'surprise':'惊讶',
    }
    skinstatus_dict = {
        'dark_circle': '黑眼圈',
        'stain': '色斑',
        'acne': '青春痘',
        'health': '健康'
    }

    n = 0
    while True:
        n += 1
        files = {'image_file': open(fileDir, 'rb')}
        request = requests.post(url=url, data=data, files=files).json()
        print(n, request)
        if 'error_message' not in request or n >= 10:
            break
    if n >= 10:
        return '访问超时，请稍后再试'
    face_info = request['faces'][0]['attributes']
    smile_value = (face_info['smile']['value']-int(face_info['smile']['value']))*1000
    ans = ans + '年龄：' + str(face_info['age']['value']) + '\n'
    if face_info['gender']['value'] == 'Male':
        ans = ans + '性别：男\n'
        ans = ans + '男性对他的颜值评价：' + str(face_info['beauty']['male_score']) + '\n'
        ans = ans + '女性对他的颜值评价：' + str(face_info['beauty']['female_score']) + '\n'
    else:
        ans = ans + '性别：女\n'
        ans = ans + '男性对她的颜值评价：' + str(face_info['beauty']['male_score']) + '\n'
        ans = ans + '女性对她的颜值评价：' + str(face_info['beauty']['female_score']) + '\n'
    ans = ans + '微笑指数：%d\n' % smile_value
    ans = ans + '情绪：' + emotion_dict[max(face_info['emotion'].items(), key=lambda x:x[1])[0]] + '\n'
    ans = ans + '皮肤特征：' + skinstatus_dict[max(face_info['skinstatus'].items(), key=lambda x:x[1])[0]] + '\n'
    print(ans)
    return ans
