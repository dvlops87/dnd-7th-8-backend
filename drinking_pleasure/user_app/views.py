from codecs import utf_16_be_decode, utf_16_be_encode
import tempfile
from tokenize import Token
from django.http import JsonResponse
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from argon2 import PasswordHasher
import base64
import pymysql
import jwt
from datetime import datetime,timedelta
from .serializers import UserCreateSerializer, UserSerializer
from .password_validcheck import password_validcheck

JWT_SECRET_KEY = getattr(settings, 'SIMPLE_JWT', None)['SIGNING_KEY']

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        conn = pymysql.connect(host='database-1.cvip8q7p6e3c.ap-northeast-2.rds.amazonaws.com', 
                        user='admin1234', passwd='admin1234', db='test', charset='utf8')
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        if password_validcheck(serializer.validated_data['passwd']) == False:
            return Response({"message": "check your password valid"}, status=status.HTTP_409_CONFLICT)
        # # SQL 문
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql_dublicate = "select * from mazle_user where email=%s limit 1"
        curs.execute(sql_dublicate,serializer.validated_data['email'])
        rows = (curs.fetchall())
        if rows:
            conn.close()
            return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)
        else:
            sql_create = "insert into mazle_user(email,passwd) values (%s,%s)"
            curs.execute(sql_create,(serializer.validated_data['email'],PasswordHasher().hash(serializer.validated_data['passwd'])))
            curs.execute(sql_dublicate,serializer.validated_data['email'])
            rows = (curs.fetchall())
            conn.commit()
            conn.close()
            payload = {
                'id': rows[0]['customer_uuid'],
                'exp': datetime.utcnow() + timedelta(hours=1)
            }
            token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')
            return Response({"token": token}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login(request):
    if request.method == 'POST':
        conn = pymysql.connect(host='database-1.cvip8q7p6e3c.ap-northeast-2.rds.amazonaws.com', 
                        user='admin1234', passwd='admin1234', db='test', charset='utf8')
        search_email = request.POST.get("email")
        password = request.POST.get("passwd")
        # SQL문 사용
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql = "select email, passwd, customer_uuid from mazle_user where email=%s limit 1"
        curs.execute(sql,search_email)
        rows = curs.fetchall()
        if rows[0]['email'] is None:
            conn.close()
            raise AuthenticationFailed('User not found!') 
        try:
            PasswordHasher().verify(rows[0]['passwd'], password)
        except:
            conn.close()
            raise AuthenticationFailed('Incorrect password!') 
        
        payload = {
            'id': rows[0]['customer_uuid'],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')
        conn.close()
        response = Response({
            "token":token
        }, status=status.HTTP_200_OK)
        response.set_cookie(key ='token', value= token, httponly=True) 

        return response


@csrf_exempt
def logout(request) :
    if request.method == 'POST' :
        response = JsonResponse({
            "message" : "success"
        })
        response.delete_cookie('token')
        return response


@csrf_exempt
def wdrl(request) :
    if request.method == 'POST' :
        conn = pymysql.connect(host='database-1.cvip8q7p6e3c.ap-northeast-2.rds.amazonaws.com', 
                        user='admin1234', passwd='admin1234', db='test', charset='utf8')
        token = request.COOKIES.get('token')
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_200_OK)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        # SQL문 사용
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql_delete = "delete from mazle_user where customer_uuid=%s"
        curs.execute(sql_delete,payload['id'])
        conn.commit()
        conn.close()
        return JsonResponse({
            "message" : "Withdrawal user"
        })


@api_view(['PUT'])
@authentication_classes([])
@permission_classes([]) 
@csrf_exempt
def update(request) :
    if request.method == 'PUT' :
        conn = pymysql.connect(host='database-1.cvip8q7p6e3c.ap-northeast-2.rds.amazonaws.com', 
                        user='admin1234', passwd='admin1234', db='test', charset='utf8')
        token = request.COOKIES.get('token')
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        nickname = request.POST.get("nickname")
        birth = request.POST.get("birth")
        profile = base64.encodebytes(request.FILES["profile"].read())
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql_update = "update mazle_user set nickname=%s, birth=%s, profile=%s where customer_uuid=%s"
        curs.execute(sql_update,(nickname,birth,profile,payload['id']))
        conn.commit()
        conn.close()

        return Response({"message": "Update user"}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([])
@permission_classes([]) 
def update_password(request) :
    if request.method == 'PUT' :
        conn = pymysql.connect(host='database-1.cvip8q7p6e3c.ap-northeast-2.rds.amazonaws.com', 
                        user='admin1234', passwd='admin1234', db='test', charset='utf8')
        passwd = request.POST.get("passwd")
        token = request.COOKIES.get("token")
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        # SQL문 사용
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql_update = "update mazle_user set passwd=%s where customer_uuid=%s"
        curs.execute(sql_update,(PasswordHasher().hash(passwd),payload['id']))
        conn.commit()
        conn.close()

        return Response({"message": "Update user"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([]) 
def mypage(request) :
    if request.method == 'GET' :
        conn = pymysql.connect(host='database-1.cvip8q7p6e3c.ap-northeast-2.rds.amazonaws.com', 
                        user='admin1234', passwd='admin1234', db='test', charset='utf8')
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        token = request.COOKIES.get("token")
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql_update = "select nickname, birth, profile, email, platform from mazle_user where customer_uuid=%s"
        curs.execute(sql_update,payload['id'])
        rows = curs.fetchall()
        oo = base64.decodebytes(rows[0]['profile']).decode('latin_1')
        conn.close()
        data = {
            "nickname" : rows[0]['nickname'],
            "birth" : rows[0]['birth'],
            "profile" : oo,
            "email" : rows[0]['email'],
            "platform" : rows[0]['platform'],
        }
        # SQL에 저장된 파일 읽을 때
        # f = open("imageToSave.png",'wb')
        # f.write(oo.encode('latin_1'))
        # f.close()
        return JsonResponse({'data' : data})
