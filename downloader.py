# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 00:59:16 2022

@author: jiyseo
"""

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import re
import sys

while True:
    try:
        num = int(input("선택(1=test, 2=download, 0=exit): "))
    except:
        continue
    if num == 0: sys.exit()
    if num >= 1 and num <= 2: break

if num == 2:
    download_mode = True
    print("download mode")
else:
    download_mode = False
    print("test mode")
print()

driver = webdriver.Chrome()
driver.get("https://www.schoolinfo.go.kr/")
action = ActionChains(driver)

def get_parent(elem):
    return elem.find_element(By.XPATH, "..") # driver.execute_script("return arguments[0].parentNode;", elem)

def wait_element(find_tuple, elem = None, timeout=5):
    if elem == None: elem = driver
    return WebDriverWait(elem, timeout).until(
        EC.presence_of_element_located(find_tuple)
    )

def find_link(text, elem = None):
    return wait_element(("link text", text), elem)

def mouse_move(elem):
    action.move_to_element(elem).perform()

def hangmok_check(elem_or_id):
    if isinstance(elem_or_id, str):
        elem = driver.find_element(By.ID, elem_or_id)
    else:
        elem = elem_or_id
    if not elem.is_selected():
        get_parent(elem).find_element(By.TAG_NAME, "label").click()

hakinfo_link = find_link("전국학교정보") # 전국학교정보 link element 얻기
hakinfo_parent = get_parent(hakinfo_link) # 전국학교정보 link 부모 tag 얻기

# mouse_move()를 했는데 submenu 표시후 가끔 hide되는 경우가 발생하고 이런 경우
# '항목별 공시정보'링크가 invisible 상태여서 find_link("항목별 공시정보") 할때
# 에러가 발생하기 때문에 3회 재시도 하도록 변경함

success = False
for retry in range(3):
    try:
        mouse_move(hakinfo_link) # mouse pointer를 전국학교정보로 옮김
        find_link("항목별 공시정보", hakinfo_parent).click() # 항목별 공시정보 링크를 클릭
        success = True
        break
    except:
       continue

if not success:
    print("항목별 공시정보 클릭 에러") # 3회 재시도 후에도 클릭하지 못한 경우
    sys.exit()

find_link("교육활동").click() # 교육활동 클릭

hangmok_check("hangmokCd_14") # '학교교육과정 편성ㆍ운영 및 평가에 관한 사항' 클릭하여 체크함
hangmok_check("hgJongryuGb_jung") # 중학교 선택

sido_convert_table = { # 시ㆍ도 변환 테이블
    "서울" : "서울특별시",
    "부산" : "부산광역시",
    "대구" : "대구광역시",
    "인천" : "인천광역시",
    "광주" : "광주광역시",
    "대전" : "대전광역시",
    "울산" : "울산광역시",
    "세종" : "세종특별자치시",
    "경기" : "경기도",
    "강원" : "강원도",
    "충북" : "충청북도",
    "충남" : "충청남도",
    "전북" : "전라북도",
    "전남" : "전라남도",
    "경북" : "경상북도",
    "경남" : "경상남도",
    "제주" : "제주특별자치도",
}

gu_convert_table = { # 시ㆍ군ㆍ구 변환 테이블
    "여주군"  : "여주시",
    "진해시"  : "창원시 진해구",
}

school_convert_table = { # 학교명 변환 테이블
    "경덕중학교"     : "대전경덕중학교",
    "대성여자중학교"  : "대전대성여자중학교",
    "계광중학교"     : "천안계광중학교",
    "삼척여자중학교"  : "청아중학교",
    "경복중학교"     : "협성경복중학교",
    "부천북중학교"     : "도당중학교"
}

csv = pd.read_csv("./school.csv")
csv = csv.sort_values(by=["시도", "행정구역", "학교"], ascending=True)
csv_data_cnt = len(csv)

sel_sido = Select(driver.find_element(By.ID, "sidoCode")) # 시ㆍ도 select tag
sel_sigunguCode = Select(driver.find_element(By.ID, "sigunguCode")) # 시ㆍ군ㆍ구 select tag
search_form = driver.find_element(By.ID, "searchForm")
search_button = search_form.find_element(By.XPATH, "//input[@value='검색']") # 검색 버튼
index = -1
currArea = "" # 시도+행정구역 비교용
div_list = driver.find_element(By.CLASS_NAME, "bbs-list") # 학교 목록 div tag
ok_cnt = 0
err_cnt = 0
closed_cnt = 0
attached_cnt = 0
unattached_cnt = 0
file_cnt = 0
while True:
    index = index + 1
    if index >= csv_data_cnt: break
    row = csv.iloc[index]     # csv data의 index 번째 row data

    sido = sido_convert_table.get(row[0]) # 시도
    if sido == None:
        print("[Error] 시도명 '" + row[0] + "' 없음")
        err_cnt = err_cnt + 1
        continue

    gu = gu_convert_table.get(row[1]) # 행정구역
    if gu == None:
        gu = row[1]        # 시ㆍ군ㆍ구 변환 테이블에 없는 경우
    #else:
    #    print("(" + gu + ")", end=" ") # 변경된 시ㆍ군ㆍ구 출력

    school_name = school_convert_table.get(row[2]) # 학교명
    if school_name == None:
        school_name = row[2]          # 학교명 변환 테이블에 없는 경우
    #else:
    #    print("(" + school_name + ")", end=" ") # 변경된 학교명 출력
    print(index + 1, ":", row[0], school_name, end=" -> ")
    area = sido + gu
    if area != currArea:      # 시도+행정구역이 다른 경우
        currArea = area       # 새로운 시도+행정구역을 저장
        sel_sido.select_by_visible_text(sido)      # 시ㆍ도를 선택함
        sel_sigunguCode.select_by_visible_text(gu) # 시ㆍ군ㆍ구를 선택함
        search_button.click()  # 검색 버튼 클릭

    find_cond = "//td[text()='" + school_name + "']"  # 학교명이 있는 td의 text에 대한 검색조건
    try:
        td_text_elem = wait_element((By.XPATH, find_cond), div_list) # td tag 내의 text element
    except:
        err_cnt = err_cnt + 1
        print("[Error] 학교명 '" + school_name + "' 없음")
        continue

    td_tag = get_parent(td_text_elem)             # td_text_elem의 부모인 td tag element
    sel_tag = Select(td_tag.find_element(By.TAG_NAME, "select")) # 해당 학교의 select tag
    sel_tag.select_by_visible_text("학교교육과정 편성ㆍ운영 및 평가에 관한 사항") # 이 항목 선택

    att_div = wait_element((By.CSS_SELECTOR, ".attached_file, .empty"), div_list) # 첨부파일 div tag
    if att_div.get_attribute("class") != "attached_file": # 폐교인 경우 empty class만 있음
        closed_cnt = closed_cnt + 1
        print("[폐교] 첨부파일 없음")
        continue

    att_files = att_div.find_elements(By.CLASS_NAME, "file_name") # 첨부파일 element 배열
    att_cnt = 0
    for file in att_files:
        txt = re.sub(" |-|_|\+|\.", "", file.text) # 정규식(Regular Expression)으로 ' ','-','_','+','.'를 제거함
        if "교육과정" in txt or "계획" in txt: # '교육과정' 또는 '계획'이 포함된 파일명만
            if download_mode: file.click() # 첨부파일 다운받기
            if att_cnt > 0: print(" , ", end="")
            att_cnt = att_cnt + 1
            print(file.text, end="")

    if att_cnt > 0:
        attached_cnt = attached_cnt + 1
    else:
        unattached_cnt = unattached_cnt + 1
        print("[첨부파일 없음]", end="")

    file_cnt = file_cnt + att_cnt
    ok_cnt = ok_cnt + 1
    print()

print("\n학교수", csv_data_cnt, ", 성공", ok_cnt, end=" , ")
if closed_cnt > 0: print("폐교", closed_cnt, end=" , ")
print("첨부", attached_cnt, end=" , ")
if unattached_cnt > 0: print("미첨부", unattached_cnt, end=" , ")
print("파일", file_cnt, end=" , ")
if err_cnt > 0:
    print("에러", err_cnt)

#driver.close() # 창을 닫는다

print("작업을 완료했습니다.")