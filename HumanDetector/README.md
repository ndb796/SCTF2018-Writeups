### Setup
* AWS EC2 구성 및 접속
```
# AWS Ubuntu Server 18.04 - t2.micro Basic - SSH Connect
```
* Python, Jupyter 설치
```
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install notebook
```
* Jupyter 접속 비밀번호 설정
```
python3
>> from notebook.auth import passwd
>> passwd()
# 비밀번호 설정한 뒤에 SHA1 값 기록하기
```
* Jupyter 환경 설정
```
c = get_config()
c.NotebookApp.password = u'sha1:{해시 값}'
c.NotebookApp.ip = '{내부 아이피}'
c.NotebookApp.notebook_dir = '/'
# 내부 아이피로는 SSH로 접속했을 때 콘솔 창에 나오는 아이피를 입력하기
```
* Jupyter HTTPS 적용
```
cd /home/ubuntu
mkdir ssl
cd ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout "cert.key" -out "cert.pem" -batch
sudo vi /home/ubuntu/.jupyter/jupyter_notebook_config.py
# 다음의 내용 입력하기
c.NotebookApp.certfile = u'/home/ubuntu/ssl/cert.pem'
c.NotebookApp.keyfile = u'/home/ubuntu/ssl/cert.key'
```
* Jupyter System Service로 등록
```
# 실행 중인 Jupyter 서버 종료하기
# jupyter-notebook 실행 파일 경로 찾기
which jupyter-notebook
# jupyter.service 작성하기
sudo vi /etc/systemd/system/jupyter.service
# Jupyter Notebook 서비스 작성하기
[Unit]
Description=Jupyter Notebook Server

[Service]
Type=simple
User=ubuntu
ExecStart=/usr/bin/sudo /usr/local/bin/jupyter-notebook --allow-root --config=/home/ubuntu/.jupyter/jupyter_notebook_config.py

[Install]
WantedBy=multi-user.target
# Jupyter 서비스 구동시키기
sudo systemctl daemon-reload
sudo systemctl enable jupyter
sudo systemctl start jupyter
# Jupyter 서비스 상태 확인하기
sudo systemctl status jupyter
# 오류 발생시 jupyter_notebook_config.py에서 IP 주소 확인하기
# Jupyter 서비스 재시작 방법
sudo systemctl restart jupyter
```
* Docker 설치하기
```
# 시작하기 전에 볼륨 크기 넉넉하게 만들기
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
# 설치 완료 후에 도커 상태 확인
sudo systemctl status docker
# Hello World 이미지 다운로드 및 실행
docker pull hello-world
docker images
docker run hello-world
docker ps -a
docker rm {Container ID}
# 모든 컨테이너 삭제
docker rm -f `docker ps -a -q`
# 모든 이미지 삭제
docker rmi -f `docker images`
# 실행 중인 도커 접속
docker attach {Container ID}
```