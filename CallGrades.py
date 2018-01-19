import requests
from selenium import webdriver
from multiprocessing import Process
import time
import win32con
import win32api


def quitwin():
    time.sleep(1)
    win32api.keybd_event(13,0,0,0)
    win32api.keybd_event(13,0,win32con.KEYEVENTF_KEYUP,0)


def query_grades(username, password, xnm, xqm):
    browser = webdriver.Edge()
    browser.delete_all_cookies()
    browser.get('校内门户登录页')
    time.sleep(1)
    if browser.title != '校内门户名称':
        browser.refresh()
        print('执行页面刷新')
        time.sleep(2)
    if browser.title != '校内门户名称':
        browser.quit()
        print('无法连接到登陆页面')
        return
    elem = browser.find_element_by_id('uname')
    elem.send_keys(username)
    elem = browser.find_element_by_id('pwd')
    elem.send_keys(password)
    browser.find_element_by_id('portalLogin').click()
    time.sleep(1)
    # print(browser.get_cookies())
    browser.switch_to_window(browser.window_handles[-1])
    sleeptimes = 0
    while browser.title != '校内门户应用名称':
        time.sleep(1)
        sleeptimes += 1
        if sleeptimes == 3:
            browser.quit()
            print('无法连接到教务系统，可能是密码错误')
            return
    # print(browser.title)
    browser.find_elements_by_class_name('nav-box')[1].click()
    time.sleep(1)
    browser.switch_to.window(browser.window_handles[-1])
    cookie = browser.get_cookies()
    p = Process(target=quitwin)
    p.start()
    browser.quit()
    p.join()

    # print(cookie)
    jessionid = cookie[0]['value']
    onevalue = cookie[1]['value']
    xqdict = {
        '1': 3,
        '2': 12,
        '3': '',
    }
    url = '查分网址'
    cookie = {
        '1': onevalue,
        'JSESSIONID': jessionid,
    }
    data = {
        'queryModel.showCount': 50,
        'xnm': xnm,
        'xqm': xqdict[str(xqm)],# 上半学期3，下半学期12
    }
    header = {
        # '伪装头信息'
    }

    req = requests.post(url=url, headers=header, data=data, cookies=cookie).json()
    req_text = req['items']
    # print(req_text)
    if req_text:
        grades = req_text[0]['xm']+req_text[0]['xh']+req_text[0]['zymc']+'\n'
        for lessen in req_text:
            grades += lessen['kcmc']
            grades += ' '
            grades += lessen['cj']
            grades += '\n'
    else:
        grades = '未查询到任何成绩'
    return grades
