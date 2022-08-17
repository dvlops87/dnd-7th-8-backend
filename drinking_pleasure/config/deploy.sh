#!/bin/bash

# settings 파일 이동
cp /home/ubuntu/my_settings.py /usr/share/Mazle/drinking_pleasure/drinking_pleasure/

cd /usr/share/Mazle/drinking_pleasure

# 가상환경설정
python3 -m venv .venv
source /usr/share/Mazle/drinking_pleasure/.venv/bin/activate
pip install -r /usr/share/Mazle/drinking_pleasure/requirements.txt

# uwsgi 설정
uwsgi --ini /usr/share/Mazle/drinking_pleasure/config/uwsgi/uwsgi.ini

# nginx 재시작
sudo service nginx restart


# Installing docker engine if not exists
# if ! type docker > /dev/null #docker를 깔아주는 코드, EC2 인스턴스에는 아무것도 없기 때문에 직접 깔아줘야 한다.
# then
#   echo "docker does not exist"
#   echo "Start installing docker"
#   sudo apt-get update
#   sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
#   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
#   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
#   sudo apt update
#   apt-cache policy docker-ce
#   sudo apt install -y docker-ce
# fi

# Installing docker-compose if not exists
# if ! type docker-compose > /dev/null #docker-compose를 깔아주는 코드
# then
#   echo "docker-compose does not exist"
#   echo "Start installing docker-compose"
#   sudo curl -L "https://github.com/docker/compose/releases/download/1.27.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
#   sudo chmod +x /usr/local/bin/docker-compose
# fi

# echo "start docker-compose up: ubuntu"
# sudo docker-compose -f /usr/share/Mazle/drinking_pleasure/docker-compose.yml up --build -d
