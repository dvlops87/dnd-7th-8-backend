from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

import requests
import pymysql

from .serializers import UserCreateSerializer
from .password_validcheck import password_validcheck
from .models import User

JWT_SECRET_KEY = getattr(settings, 'SIMPLE_JWT', None)['SIGNING_KEY']
conn = pymysql.connect(host='database-1.cvip8q7p6e3c.ap-northeast-2.rds.amazonaws.com', 
                        user='admin1234', password='admin1234', db='test', charset='utf8')

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        if password_validcheck(serializer.validated_data['password']) == False:
            return Response({"message": "check your password valid"}, status=status.HTTP_409_CONFLICT)
            
        # SQL 문
        # curs = conn.cursor(pymysql.cursors.DictCursor)
        # sql = "insert into user_app_user(email,password) values (%s,%s)"
        # curs.execute(sql,(serializer.validated_data['email'],serializer.validated_data['password']))
        # conn.close()

        if User.objects.filter(email=serializer.validated_data['email']).first() is None:
            serializer.save()
            return Response({"message": "Good email for use"}, status=status.HTTP_201_CREATED)
        return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        search_email = request.POST.get("email")
        password = request.POST.get("password")

        # SQL문 사용
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select * from user_app_user where email=%s limit 1"
        curs.execute(sql,search_email)
        rows = curs.fetchall()
        conn.close()
        if rows[0]['email'] is None:
            raise AuthenticationFailed('User not found!') 
        user = User.objects.get(email=rows[0]['email'])
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!') 

        # 쿼리문 사용
        # user = User.objects.get(email=search_email)
        # if user is None:
        #     raise AuthenticationFailed('User not found!') 
        # if not user.check_password(password):
        #     raise AuthenticationFailed('Incorrect password!') 

        data = {"email": search_email, "password": password}
        response_token = requests.post("http://127.0.0.1:8000/users/api-jwt-auth/", data=data)
        response_token = response_token.json()
        response = JsonResponse({
            'message' : 'ok',
            'jwt':response_token["access"]
        })

        response.set_cookie(key ='jwt', value= response_token, httponly=True) 

        return response


@csrf_exempt
def logout(request) :
    if request.method == 'POST' :
        response = JsonResponse({
            "message" : "success"
        })
        response.delete_cookie('jwt')
        return response
