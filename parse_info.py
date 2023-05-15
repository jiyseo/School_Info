# 라이브러리 import
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from dotenv import load_dotenv
import os 
 
load_dotenv()

# 요청url 잘게 자르기
url = "https://www.schoolinfo.go.kr/openApi.do"
serviceKey = os.environ.get('Servicekey')
info = "&apiType=09"
data_year = "&pbanYr=2022"
school_code = "&schulKndCode=03"


# 항목 parsing 함수작성하기
def parse():
    try:
        ADRCD_NM = item.get("ADRCD_NM")
        SCHUL_NM = item.get("SCHUL_NM")
        COL_C1 = item.get("COL_C1")
        COL_S1 = item.get("COL_S1")
        COL_1 = item.get("COL_1")
        COL_C2 = item.get("COL_C2")
        COL_S2 = item.get("COL_S2")
        COL_2 = item.get("COL_2")
        COL_C3 = item.get("COL_C3")
        COL_S3 = item.get("COL_S3")
        COL_3 = item.get("COL_3")
        COL_C_SUM = item.get("COL_C_SUM")
        COL_S_SUM = item.get("COL_S_SUM")
        COL_SUM = item.get("COL_SUM")

        return {
            "지역": ADRCD_NM,
            "학교명": SCHUL_NM,
            "1학년학급수": COL_C1,
            "1학년학생수": COL_S1,
            "1학년학급당학생수": COL_1,
            "2학년학급수": COL_C2,
            "2학년학생수": COL_S2,
            "2학년학급당학생수": COL_2,
            "3학년학급수": COL_C3,
            "3학년학생수": COL_S3,
            "3학년학급당학생수": COL_3,
            "학급수(계)": COL_C_SUM,
            "학생수(계)":COL_S_SUM,
            "학급당학생수(계)": COL_SUM

        }
    except AttributeError as e:
        return {
            "지역": None,
            "학교명": None,
            "1학년학급수": None,
            "1학년학생수": None,
            "1학년학급당학생수": None,
            "2학년학급수": None,
            "2학년학생수": None,
            "2학년학급당학생수": None,
            "3학년학급수": None,
            "3학년학생수": None,
            "3학년학급당학생수": None,
            "학급수(계)": None,
            "학생수(계)": None,
            "학급당학생수(계)": None
        }


# parsing 하기
url = url + serviceKey + info + data_year + school_code
result = requests.get(url)
sc_info = json.loads(result.text)
row = []
for item in sc_info["list"]:
    row.append(parse())

# pandas 데이터프레임에 넣기
df = pd.DataFrame(row)

# csv 파일로 저장하기
df.to_csv("school_info.csv", mode='w')

# csv 파일 불러오기
data = pd.read_csv("school_info.csv", index_col=0)
df2 = pd.DataFrame(data)