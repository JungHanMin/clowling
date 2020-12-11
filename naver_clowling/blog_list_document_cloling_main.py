# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 12:54:33 2020

@author: 정한민
"""

import re
import os
import time
import requests
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

range_off_error_check = 1
string_find_check = -1
title_length_check = 4

#크롬 패스
chrome_path = 'C:/Developer/python/chromedriver'
#검색URL
#226705277
restaurant_url = 'https://m.place.naver.com/restaurant/'
#헤더
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}

span_key_string = 'span'

title_key_string = 'pcol1 itemSubjectBoldfont'

# 실질적으로 검색이 되는 함수
#BeautifulSoup 을 리턴한다.
def clowling_request(search_name):
    response = requests.get('https://m.place.naver.com/place/list?query=' + search_name)
    html = response.content.decode('utf-8','replace') 
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_naverURL_id(soup):
    script = soup.find_all("script")

    parse_string = str(script).split('window.__APOLLO_STATE__ = ')
    parse_string = parse_string[1].split('categoryCodeList')
    parse_string = parse_string[0].split('items')
    
    url_id_list = re.findall("\d+", parse_string[1])
    
    return url_id_list
    
def get_blog_list(url_string):
    response = requests.get(restaurant_url + url_string + '/home')

    html = response.content.decode('utf-8','replace') 
    soup = BeautifulSoup(html, 'html.parser')
    script = soup.find_all("script")
    parse_string = str(script).split('window.__APOLLO_STATE__ =')
    change_string_list = []
    if len(parse_string) > range_off_error_check:
        parse_string = parse_string[1].split('window.__PLACE_STATE__ =')
        parse_string = parse_string[0].split('__typename":"SasImage"},"ROOT_QUERY.sasImages')
        
        # print(len(parse_string))
        
        # if len(parse_string) == 1:
        #     print(parse_string)
        parse_list = []
        section_split_list = []
        if len(parse_string) > range_off_error_check:
            
            parse_string_list = parse_string[1].split(',\"link\":')
            # print(parse_string_list[0])
            # print(len(parse_string_list))
            
            for list_string in parse_string_list:
                # if list_string:
                # list_string = parse_string_list[1]    
                blog_index = list_string.find('blog.naver.com')
                # print(blog_index)
                if blog_index > string_find_check:
                    parse_list = list_string.split(',\"section\":')
                    
                    section_split_list.append(parse_list[0])
            # print(parse_list)
        
        # string_change
        for change_string in section_split_list:
            change_string = str(change_string).replace('u002F','')
            change_string = str(change_string).replace('"','')
            change_string = str(change_string).replace('\\','/')
            
            change_string_list.append(change_string)
            
    return change_string_list

def get_blog_contents(soup, blog_number):
    
    # print(time_soup_string)
    title_soup_string = ''
    title_soup_string = str(soup.find_all('span',attrs={"class":"se-fs- se-ff-"}))
    title_soup_string = re.sub('<.+?>', '', title_soup_string, 0).strip()
    title_soup_string = title_soup_string.replace("[","")
    title_soup_string = title_soup_string.replace("]","")
    
    # # contents_string = str(soup.find_all('p'))
    # # contents_string = re.sub('<.+?>', '', contents_string, 0).strip()
    # print(title_soup_string)
    # # print(contents_string)
    
    contents_list = []
    title_list = title_soup_string.split(',')
    mobile_title = ''
    hashtag_string = ''
    contents_string = ''
    delete_hash_string = ''
    delete_small_hash_string = ''
    contents_string = ''
    if len(title_list) > title_length_check:
        mobile_title = title_list[0]
        hashtag_string = title_list[len(title_list) - 1] + title_list[len(title_list) - 2]
        delete_hash_string = title_list[len(title_list) - 1]
        delete_small_hash_string = title_list[len(title_list) - 2]
        # title_list = list(set(title_list))
        contents_string = str(title_list)
        contents_string = contents_string.replace("[","")
        contents_string = contents_string.replace("]","")
        contents_string = contents_string.replace("'","")
        contents_string = contents_string.replace(delete_hash_string,"")
        contents_string = contents_string.replace(delete_small_hash_string,"")
        contents_string = contents_string.replace(","," ")
        contents_string = contents_string.replace("&nsp;"," ")
        
    else:
        title_soup_string = str(soup.find('div',attrs={"id":"post-view" + blog_number}))
        title_soup_string = re.sub('<.+?>', '', title_soup_string, 0).strip()
        title_soup_string = title_soup_string.replace("[","")
        title_soup_string = title_soup_string.replace("]","")
        title_soup_string = title_soup_string.replace("                 ","")
        title_soup_string = title_soup_string.replace('\n','')
        title_soup_string = title_soup_string.replace('지도보기','')
        title_soup_string = title_soup_string.replace('본문','')
        title_soup_string = title_soup_string.replace('기타','')
        title_soup_string = title_soup_string.replace('기능지도로 보기','')
        title_soup_string = title_soup_string.replace('전체지도','')
        title_soup_string = title_soup_string.replace('닫기','')
        title_soup_string = title_soup_string.replace('번역보기','')
        title_soup_string = title_soup_string.replace('위치','')
        title_soup_string = title_soup_string.replace('복사','')
        title_soup_string = title_soup_string.replace('이웃추가','')
        title_soup_string = title_soup_string.replace(","," ")
        title_soup_string = title_soup_string.replace("&nsp;"," ")
        
        
        # title_soup_string = re.sub("^\s+|\s+$","",title_soup_string, flags=re.UNICODE)
        
        contents_string = title_soup_string
        
        # print(title_soup_string)
    if len(title_soup_string) < 14:
        title_soup_string = str(soup.find_all('p'))
        title_soup_string = re.sub('<.+?>', '', title_soup_string, 0).strip()

        title_soup_string = title_soup_string.replace("                 ","")
        title_soup_string = title_soup_string.replace("\n","")
        title_soup_string = title_soup_string.replace("[","")
        title_soup_string = title_soup_string.replace("]","")
        title_soup_string = title_soup_string.replace("_님로그아웃","")
        title_soup_string = title_soup_string.replace("네이버 멤버쉽","")
        title_soup_string = title_soup_string.replace("알림을 모두 삭제하시겠습니까?","")
        title_soup_string = title_soup_string.replace("지금 떠오른 생각을 퀵에디터로 메모해보세요.","")
        title_soup_string = title_soup_string.replace("   ","")
        
        contents_list = title_soup_string.split(',')
        # contents_list.remove('\'')
        # contents_list = set(contents_list)
        title_soup_string = title_soup_string.replace(",","")
        # print(contents_list[7])
        # print(title_soup_string)
        contents_string = title_soup_string
        mobile_title = contents_list[7]
    # print(title_soup_string)
    # print(contents_string)
    # print('모바일 타이틀_title',mobile_title)
    # print('모바일 타이틀_title',len(mobile_title))
    
    if len(mobile_title) < title_length_check:
        # pcol1 itemSubjectBoldfont
        # pcol1 itemSubjectBoldfont
        mobile_title = str(soup.find_all('td',attrs={"class":"bcc"}))
        # mobile_title = str(soup.find('span'))
        mobile_title = re.sub('<.+?>', '', mobile_title, 0).strip()
        mobile_title = mobile_title.replace('\n','')

        mobile_title = mobile_title.replace("[","")
        mobile_title = mobile_title.replace("]","")
        # print('모바일 타이틀',mobile_title)
        
        
    # print(mobile_title)
    
    hashtag_string = str(soup.find('div',attrs={"class":"post_footer_contents"}))
    hashtag_string = re.sub('<.+?>', '', hashtag_string, 0).strip()
    hashtag_string = hashtag_string.replace("[","")
    hashtag_string = hashtag_string.replace("]","")
    hashtag_string = hashtag_string.replace("취소","")
    hashtag_string = hashtag_string.replace("확인","")
    hashtag_string = hashtag_string.replace('\n','')
    hashtag_string = hashtag_string.replace("                 ","")
    hashtag_string = hashtag_string.replace('저작자 명시 필수영리적 사용 불가내용 변경 불가','')
    hashtag_string = hashtag_string.replace('저작자 명시 필수','')
    hashtag_string = hashtag_string.replace('- 영리적 사용 불가','')
    hashtag_string = hashtag_string.replace('- 내용 변경 불가','')
    
    sympathy_soup_string = str(soup.find_all('em',attrs={"class":"u_cnt _count"}))
    sympathy_soup_string = re.sub('<.+?>', '', sympathy_soup_string, 0).strip()
    sympathy_soup_string = sympathy_soup_string.replace("[","")
    sympathy_soup_string = sympathy_soup_string.replace("]","")
    
    return mobile_title, hashtag_string, contents_string, sympathy_soup_string
    
def get_blog_time(soup):
    # p class date fil5 pcol2 _postAddDate
    time_soup_string = str(soup.find_all('span',attrs={"class":"se_publishDate pcol2"}))
    time_soup_string = re.sub('<.+?>', '', time_soup_string, 0).strip()
    time_soup_string = time_soup_string.replace("[","")
    time_soup_string = time_soup_string.replace("]","")
    
    if len(time_soup_string) < title_length_check:
        time_soup_string = str(soup.find_all('span',attrs={"class":"date fil5 pcol2 _postAddDate"}))
        time_soup_string = re.sub('<.+?>', '', time_soup_string, 0).strip()
        time_soup_string = time_soup_string.replace("[","")
        time_soup_string = time_soup_string.replace("]","")    
        
        
    return time_soup_string


iStart = 0
# tour1Df = pd.read_csv('blog_list.csv',   thousands=',')


naver_id = 10968214
traval_id = 24355


# 블로그 리스트 를 얻어오므로 for 문을 돌려야한다.
# for now_csv_count in range(iStart, len(tour1Df)):
#     blog_url_string = tour1Df.loc[now_csv_count, "blog URL"]

blog_url_string = 'https://blog.naver.com/mgchoice?Redirect=Log&logNo=222158117642'

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")

driver = webdriver.Chrome(chrome_path, chrome_options=options)
driver.get(blog_url_string)

driver.switch_to.frame("mainFrame")

blog_url_list = blog_url_string.split('/')

blog_number = blog_url_list[len(blog_url_list) - 1]


time.sleep(2)
selenium_string = driver.page_source

soup = BeautifulSoup(selenium_string, 'html.parser')

#시간을 얻어온다.
time_soup_string = get_blog_time(soup)

mobile_title, hashtag_string, contents_string, sympathy_soup_string = get_blog_contents(soup ,blog_number)


# =============================================================================================
print('지금카운트')
# print(now_csv_count)
# 파일을 넣을 위치
list_b = {'여행지 아이디' : traval_id, 'blog_URL' : blog_url_string, '날짜' : time_soup_string, '네이버 아이디' : naver_id,'블로그 제목' : mobile_title, 'HashTag': hashtag_string,
          '블로그 내용' : contents_string, '공감' : sympathy_soup_string }

df = pd.DataFrame(list_b,index = [0])
if not os.path.exists('C:\output.csv'):
    df.to_csv('C:\output.csv', index=False, mode='w', encoding='utf-8-sig')
else:
    df.to_csv('C:\output.csv', index=False, mode='a', encoding='utf-8-sig', header=False)
print('들어가는지 체크해준다.')
driver.close()




























