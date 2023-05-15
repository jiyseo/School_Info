# School_Info

https://www.schoolinfo.go.kr 사이트에서
전국의 약 100여개의 중학교에 대하여 학년별 학생수, 학년별 학급수, 학년별 학급당 학생수, 학급수, 학생수 등을 크롤링하는 코드입니다.

downloader.py
- 해당 중학교에 대하여 학교교육과정 편성ㆍ운영 및 평가에 관한 사항 파일을 다운로드

parse_info.py 
- https://www.schoolinfo.go.kr/openApi.do 의 모든 중학교 정보 xml로 저장 후 파싱 -> csv 파일로 저장

load_studentnum.py 
- 원하는 중학교에 대해서만 정보 얻기
