프로젝트 운영 기록

# 가상환경 구성 - OS가 달라서 장담은 못하지만 아래 명령어를 복붙하시면 될겁니다.
python -m venv venv
python -m pip install --upgrade pip
pip install flask pymongo dnspython requests awsebcli certifi PyJWT beautifulsoup4

# template 파일 구성
- Bootstrap CDN Link 추가
- jQuery CDN Link 추가
- 공통 CSS, JS 파일 연동
- favicon 이미지 적용

# app.py 파일 구성
- Mongo DB 연동 코드 추가
- 각 페이지로의 라우팅 연동
- 404 에러 핸들러 추가

# .gitignore 파일 구성
- venv는 공유하지 못하도록 설정 [각 사용자마다 OS가 다르기 때문]

# static 디렉토리 구성
- 차후 로고 추가를 염두해 구성
- 차후 일괄 CSS, JS 적용을 염두해 구성
- favicon 이미지 파일 예시를 위해 추가
