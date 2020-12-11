# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 08:53:39 2020

@author: 정한민
"""


import requests
import re
import os
import time
import pandas as pd
from bs4 import BeautifulSoup


#가져올 목록 문서파일
tour1Df = pd.read_csv('tour_강릉_202001.csv',   thousands=',')

#search URL
restaurant_url = 'https://m.place.naver.com/restaurant/'

#search url query
query_url = 'https://m.place.naver.com/place/list?query='

#헤더파일
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}

# 조건문 맥스값
SEARCH_LIST_MAX = 7
NOT_FIND_SEARCH = -1
CAN_NOT_LOOP = 0
LENGTH_CHECK = 1


#키워드를 얻어온다.
def thema_keyword(soup):
    # 테마 키워드 
    thema_element = str(soup.find_all('li',attrs={"class":"_3Ryhx"}))
    thema_element = re.sub('<.+?>', '', thema_element, 0).strip()
    
    # print(thema_element)
    
    
    thema_element = thema_element.replace("분위기","분위기,")
    thema_element = thema_element.replace("인기토픽","인기토픽,")
    thema_element = thema_element.replace("찾는목적","찾는목적,")
    thema_element = thema_element.replace(" ","")
    thema_element = thema_element.replace("[","")
    thema_element = thema_element.replace("]","")
    return thema_element

#키워드를 항목별로 정제한다.
def set_thema_keyword(thema_element):
    find_list_index = thema_element.find('찾는목적')
    thema_list = ['','','']
    
    move_string = ''
    find_list_string = []
    if find_list_index != NOT_FIND_SEARCH:
        find_list_string = thema_element.split('찾는목적')
        # print(find_list_string[0])
        # print(find_list_string[1])
        move_string = find_list_string[0]
        find_list_string = find_list_string[1]
        find_list_string = find_list_string.replace(",","/")
        thema_list[2] = find_list_string
        thema_element = move_string
    else :
        thema_list[2] = None
    
    find_list_index = thema_element.find('인기토픽')
    
    if find_list_index != NOT_FIND_SEARCH:
        find_list_string = thema_element.split('인기토픽')
        move_string = find_list_string[0]
        # print(find_list_string[0])
        # print(find_list_string[1])
        # print(move_string)
    
        find_list_string = find_list_string[1]
        find_list_string = find_list_string.replace(",","/")
        thema_list[1] = find_list_string
        thema_element = move_string
    else :
        thema_list[1] = None
    
    find_list_index = thema_element.find('분위기')
    
    if find_list_index != NOT_FIND_SEARCH:
        find_list_string = thema_element.split('분위기')
        move_string = find_list_string[0]
    
        find_list_string = find_list_string[1]
        
        find_list_string = find_list_string.replace(",","/")
        thema_list[0] = find_list_string
    else :
        thema_list[0] = None
        
    return thema_list

#카테고리를 얻어옴
def category(soup):
    category_element = str(soup.find_all('span',attrs={"class":"_3ocDE"}))
    category_element = re.sub('<.+?>', '', category_element, 0).strip()
    category_element = category_element.replace("[","")
    category_element = category_element.replace("]","")
    return category_element

#타이틀을 얻어옴
def get_title(soup):
    # 타이틀
    maintitle_element_title = str(soup.find_all('span',attrs={"class":"_3XamX"}))
    maintitle_element_title = re.sub('<.+?>', '', maintitle_element_title, 0).strip()
    maintitle_element_title = maintitle_element_title.replace("[","")
    maintitle_element_title = maintitle_element_title.replace("]","")
    return maintitle_element_title

#주소를 얻어옴
def get_address(soup):
    address_string = str(soup.find_all('span',attrs={"class":"_2yqUQ"}))
    address_string = re.sub('<.+?>', '', address_string, 0).strip()
    address_string = address_string.replace("[","")
    address_string = address_string.replace("]","")
    address_string = address_string.replace("가격표 사진을 올려주세요.","")
    address_string = address_string.replace("이용시간을 알려주세요.","")
    address_string = address_string.replace(",","")
    return address_string

#평점을 얻어옴
def get_avg_count(soup):
    main_avg_count = soup.find_all('div',attrs={"class":"_3XpyR"})
    string =''
    for strin in main_avg_count:
        string = str(strin.find_all('em',limit=3))
    
    maintitle_element = re.sub('<.+?>', '', string, 0).strip()
    maintitle_element = maintitle_element.replace("[","")
    maintitle_element = maintitle_element.replace("]","")
    return maintitle_element


#이미지를 얻어옴
def get_imag_URL(soup):
    img_string = str(soup.find_all('div',attrs={"class":"cb7hz _div"}))           
    image_element_list = re.findall('\(([^)]+)', img_string)
    return image_element_list

#스타트 인덱스
iStart = 0


for i in range(iStart, len(tour1Df)):
        
    name = tour1Df.loc[i, "여행지 이름"]
    place_id = tour1Df.loc[i, "여행지 아이디"]
        
    #검색이 되는곳
    response = requests.get(query_url + "강릉 " + name)
    html = response.content.decode('utf-8','replace') 
    soup = BeautifulSoup(html, 'html.parser')
    
    
    #스크립트를 잘라오는 곳
    script = soup.find_all("script")
    
    # print(soup)
    parse_string = str(script).split('window.__APOLLO_STATE__ = ')
    parse_string = parse_string[1].split('categoryCodeList')
    parse_string = parse_string[0].split('items')
    
    
    url_id_string = re.findall("\d+", parse_string[1])

    # =============================================================================================
    url_id_string = list(set(url_id_string))
    

    # 포문이 추가 되어야 한다. 
    for cnt, url_string in enumerate(url_id_string):
        # url_string = url_id_string[0]
        # url_string = '1600881513'
        time.sleep(2)   
        if cnt > SEARCH_LIST_MAX:
            break
        
        response = requests.get(restaurant_url + url_string + '/home')
        
        print('# =============================================================================================')
        print('url_경로:',restaurant_url + url_string + '/home')   
        
        print('장소 ID',place_id)
        print('가져올 이름:',name)
            
        html = response.content.decode('utf-8','replace')    
        soup = BeautifulSoup(html, 'html.parser')   
        
        
        string_image_element = ''                
        image_element_list = get_imag_URL(soup)
                    
        if len(image_element_list) > LENGTH_CHECK:
            string_image_element = image_element_list[0]

        # 주소
        address_string = get_address(soup)
        
        #주소체크
        #강원 강릉 이 없으면 더이상 진행하지 않는다.
        file_check_address = address_string.find('강릉')
        if (file_check_address < CAN_NOT_LOOP):
            continue
        
        #타이틀
        maintitle_element_title = get_title(soup)
        #타이틀을 공백으로 잘라서
        #해당 단어가 있으면 더이상 진행하지 않는다.
        nameList = name.split(' ')
        bCheck = False
        for nl in nameList:
            if (maintitle_element_title.find(nl) < CAN_NOT_LOOP):
                bCheck = True
                
        if (bCheck == True ):
            continue
        
        #평점
        maintitle_element = get_avg_count(soup)
        
        check_count = maintitle_element.find('.')
        count_list = maintitle_element.split(',')
        
        blog_reaview =''
        avg_string = ''
        
        if check_count != NOT_FIND_SEARCH:

            avg_string = count_list[0]
            blog_reaview = count_list[1]
        else:
            avg_string = None
            if len(count_list)>0:
                blog_reaview = count_list[0]
            else:
                blog_reaview = None
        
        # 카테고리
        category_element = category(soup)
        
        # 테마
        thema_element = thema_keyword(soup)

        # 테마 리스트 셋
        thema_list = set_thema_keyword(thema_element)

        #주소에 면으로 교체, 강원이 없으면 넣지 않는다.
        #if file_check_address != -1 and file_check_city_address != -1:
        if (file_check_address > 0):
        # =============================================================================================
        # 파일을 넣을 위치
            list_b = { '여행지 ID' : place_id, 'naver_id': url_string, '타이틀' : maintitle_element_title, '주소' : address_string, '종류' : category_element, '평점' : avg_string, '투표' : blog_reaview , '분위기' : thema_list[0],
                      '인기토픽' : thema_list[1], '찾는목적' : thema_list[2], '메인 img_url' : string_image_element}
            
            df = pd.DataFrame(list_b,index = [0])
            if not os.path.exists('C:\output.csv'):
                df.to_csv('C:\output.csv', index=False, mode='w', encoding='utf-8-sig')
            else:
                df.to_csv('C:\output.csv', index=False, mode='a', encoding='utf-8-sig', header=False)