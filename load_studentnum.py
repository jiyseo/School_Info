# Created or modified on Nov 16
# Author: jiyseo

import pandas as pd
import numpy as np
import csv

# csv 파일에서 불러오기
s_cols = ['지역', '학교명', '1학년학급수', '1학년학생수', '1학년학급당학생수', '2학년학급수', '2학년학생수', '2학년학급당학생수', '3학년학급수', '3학년학생수', '3학년학급당학생수', '학급수(계)', '학생수(계)', '학급당학생수(계)']

school = pd.read_csv('./school_info.csv', names=s_cols)
school=school.iloc[1:]
i_cols = ['시도', '행정구역', '학교']
info = pd.read_csv('./school.csv', names=i_cols)
info=info.iloc[1:]

sido_table = {
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
csv_data_cnt = len(info)

from pandas.core.groupby.groupby import DataFrame
first_c = []
first_s = []
first_cs = []
second_c = []
second_s = []
second_cs = []
third_c = []
third_s = []
third_cs = []
total_c = []
total_s = []
total_cs = []
sido_name = []
name = []
res = DataFrame()
index = -1
while True:
    index = index + 1
    if index >= csv_data_cnt: break
    row = info.iloc[index]     # csv data의 index 번째 row data
    sido = sido_table[row[0]] # 시도
    gu = row[1]               # 행정구역
    school_name = row[2]      # 학교
    if (gu == "여주군"): gu = "여주시"
    if (gu == "진해시"): gu = "창원시 진해구"
    if (gu == "성남시") and (school_name == "성남여자중학교"): gu = "성남시 수정구"
    if (gu == "성남시") and (school_name == "숭신여자중학교"): gu = "성남시 중원구"
    if (gu == "수원시"): gu = "수원시 팔달구"
    if (gu == "안산시"): gu = "안산시 단원구"
    if (gu == "용인시"): gu = "용인시 기흥구"
    if (gu == "천안시"): gu = "천안시 동남구"
    if (school_name == "경덕중학교") : school_name = "대전경덕중학교"
    if (school_name == "대성여자중학교"): school_name = "대전대성여자중학교"
    if (school_name == "계광중학교"): school_name = "천안계광중학교"
    if (school_name == "삼척여자중학교"): school_name = "청아중학교"
    if (school_name == "경복중학교"): school_name = "협성경복중학교"
    sido = sido + ' ' + gu
    cnt = 0
    for i in range (1, len(school) - 1) :
      s_name = school['학교명'][i]
      s_sido = school['지역'][i]
      if s_name == school_name and s_sido == sido:
        cnt = 1
        name.append(school_name)
        sido_name.append(sido)
        first_c.append(school['1학년학급수'][i])
        first_s.append(school['1학년학생수'][i])
        first_cs.append(school['1학년학급당학생수'][i])
        second_c.append(school['2학년학급수'][i])
        second_s.append(school['2학년학생수'][i])
        second_cs.append(school['2학년학급당학생수'][i])
        third_c.append(school['3학년학급수'][i])
        third_s.append(school['3학년학생수'][i])
        third_cs.append(school['3학년학급당학생수'][i])
        total_c.append(school['학급수(계)'][i])
        total_s.append(school['학생수(계)'][i])
        total_cs.append(school['학급당학생수(계)'][i])
    if cnt == 0 :
      cnt = 1
      name.append(school_name)
      sido_name.append(sido)
      total_c.append("none")
      total_s.append("none")
      total_cs.append("none")
      first_c.append("none")
      first_s.append("none")
      first_cs.append("none")
      second_c.append("none")
      second_s.append("none")
      second_cs.append("none")
      third_c.append("none")
      third_s.append("none")
      third_cs.append("none")

res = res.assign(sido_name = sido_name)
res = res.assign(name = name)
res = res.assign(total_c = total_c)
res = res.assign(total_s = total_s)
res = res.assign(total_cs = total_cs)
res = res.assign(first_c = first_c)
res = res.assign(first_s = first_s)
res = res.assign(first_cs = first_cs)
res = res.assign(second_c = second_c)
res = res.assign(second_s = second_s)
res = res.assign(second_cs = second_cs)
res = res.assign(third_c = third_c)
res = res.assign(third_s = third_s)
res = res.assign(third_cs = third_cs)


print(res)
res.to_csv("./school_res.csv", index = False)