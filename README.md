# nrise_backend

<img src="https://img.shields.io/badge/coverage-97%25-green">
<img src="https://img.shields.io/badge/license-MIT-green">

### 1. local 파일 세팅
- local_sample.py -> local.py 변경
- local.py - database 설정

### 2. 환경변수 세팅
> DJANGO_SETTINGS_MODEULE = conf.settings.local

### 3. requirements 설치
> pip install -r /requirements/api.txt

### 4. migrate
> ./manage.py migrate

### 5. TDD
* pytest-django
* pytest-cov
* pytest-xdist

### 6. DataBase
* MySQL

