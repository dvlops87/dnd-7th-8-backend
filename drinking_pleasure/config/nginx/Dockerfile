FROM nginx:latest

# 기존 도커의 nginx 설정 파일 변경
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx-app.conf /etc/nginx/conf.d/
