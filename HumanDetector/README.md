### Setup
* AWS EC2 ���� �� ����
```
# AWS Ubuntu Server 18.04 - t2.micro Basic - SSH Connect
```
* Python, Jupyter ��ġ
```
sudo apt-get update
sudo apt-get install python3-pip
sudo pip3 install notebook
```
* Jupyter ���� ��й�ȣ ����
```
python3
>> from notebook.auth import passwd
>> passwd()
# ��й�ȣ ������ �ڿ� SHA1 �� ����ϱ�
```
* Jupyter ȯ�� ����
```
c = get_config()
c.NotebookApp.password = u'sha1:{�ؽ� ��}'
c.NotebookApp.ip = '{���� ������}'
c.NotebookApp.notebook_dir = '/'
# ���� �����Ƿδ� SSH�� �������� �� �ܼ� â�� ������ �����Ǹ� �Է��ϱ�
```
* Jupyter HTTPS ����
```
cd /home/ubuntu
mkdir ssl
cd ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout "cert.key" -out "cert.pem" -batch
sudo vi /home/ubuntu/.jupyter/jupyter_notebook_config.py
# ������ ���� �Է��ϱ�
c.NotebookApp.certfile = u'/home/ubuntu/ssl/cert.pem'
c.NotebookApp.keyfile = u'/home/ubuntu/ssl/cert.key'
```
* Jupyter System Service�� ���
```
# ���� ���� Jupyter ���� �����ϱ�
# jupyter-notebook ���� ���� ��� ã��
which jupyter-notebook
# jupyter.service �ۼ��ϱ�
sudo vi /etc/systemd/system/jupyter.service
# Jupyter Notebook ���� �ۼ��ϱ�
[Unit]
Description=Jupyter Notebook Server

[Service]
Type=simple
User=ubuntu
ExecStart=/usr/bin/sudo /usr/local/bin/jupyter-notebook --allow-root --config=/home/ubuntu/.jupyter/jupyter_notebook_config.py

[Install]
WantedBy=multi-user.target
# Jupyter ���� ������Ű��
sudo systemctl daemon-reload
sudo systemctl enable jupyter
sudo systemctl start jupyter
# Jupyter ���� ���� Ȯ���ϱ�
sudo systemctl status jupyter
# ���� �߻��� jupyter_notebook_config.py���� IP �ּ� Ȯ���ϱ�
# Jupyter ���� ����� ���
sudo systemctl restart jupyter
```
* Docker ��ġ�ϱ�
```
# �����ϱ� ���� ���� ũ�� �˳��ϰ� �����
sudo apt update
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
sudo apt update
apt-cache policy docker-ce
sudo apt install docker-ce
# ��ġ �Ϸ� �Ŀ� ��Ŀ ���� Ȯ��
sudo systemctl status docker
# Hello World �̹��� �ٿ�ε� �� ����
docker pull hello-world
docker images
docker run hello-world
docker ps -a
docker rm {Container ID}
# ��� �����̳� ����
docker rm -f `docker ps -a -q`
# ��� �̹��� ����
docker rmi -f `docker images`
# ���� ���� ��Ŀ ����
docker attach {Container ID}
```