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
    browser.get('http://i.swu.edu.cn/portal_main/toPortalPage')
    time.sleep(1)
    if browser.title != '西南大学一站式服务门户':
        browser.refresh()
        print('执行页面刷新')
        time.sleep(2)
    if browser.title != '西南大学一站式服务门户':
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
    while browser.title != '我的应用':
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
    url = 'http://jw.swu.edu.cn/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005'
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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
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
