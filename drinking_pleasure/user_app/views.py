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
from .password_validcheck import password_validcheck
import uuid
from mysql.connector import pooling
from django.contrib.auth.decorators import login_required

dbconfig = getattr(settings, 'DBCONFIG', None)
JWT_SECRET_KEY = getattr(settings, 'SIMPLE_JWT', None)['SIGNING_KEY']
pool= pooling.MySQLConnectionPool(pool_name = "mypool",pool_size = 20,**dbconfig)

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        search_email = request.POST.get("email")
        passwd = request.POST.get("passwd")
        if password_validcheck(passwd) == False:
            return Response({"message": "check your password"}, status=status.HTTP_400_BAD_REQUEST)
        user_uuid = str(uuid.uuid4())
        # # SQL 문
        con = pool.get_connection()
        curs = con.cursor(buffered=False)
        sql_duplicate = "SELECT * FROM mazle_user WHERE email = %s limit 1;"
        curs.execute(sql_duplicate,(search_email,))
        rows = (curs.fetchall())
        if rows:
            curs.close()
            con.close()
            return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)
        else:
            sql_create = "insert into mazle_user (customer_uuid, email,passwd) values (%s,%s,%s)"
            curs.execute(sql_create,(user_uuid,search_email,PasswordHasher().hash(passwd),))
            sql_select = "SELECT customer_uuid FROM mazle_user WHERE email = %s limit 1;"
            curs.execute(sql_select,(search_email,))
            rows = (curs.fetchall())
            con.commit()
            curs.close()
            con.close()
            payload = {
                'id': rows[0][0],
                'exp': datetime.utcnow() + timedelta(hours=1)
            }
            token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')
            return Response({"token": token}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login(request):
    if request.method == 'POST':
        con = pool.get_connection()
        curs = con.cursor()
        search_email = request.POST.get("email")
        password = request.POST.get("passwd")
        # SQL문 사용
        sql = "select email, passwd, customer_uuid from mazle_user where email=%s limit 1"
        curs.execute(sql,(search_email,))
        rows = curs.fetchall()
        if rows[0][0] is None:
            curs.close()
            con.close()
            raise AuthenticationFailed('User not found!') 
        try:
            PasswordHasher().verify(rows[0][1], password)
        except:
            curs.close()
            con.close()
            raise AuthenticationFailed('Incorrect password!') 
        
        payload = {
            'id': rows[0][2],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')
        curs.close()
        con.close()
        response = Response({
            "token":token
        }, status=status.HTTP_200_OK)
        response.set_cookie(key ='token', value= token, httponly=True) 

        return response


# @login_required
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
        con = pool.get_connection()
        curs = con.cursor()
        token = request.COOKIES.get('token')
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_200_OK)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        # SQL문 사용
        curs = con.cursor(pymysql.cursors.DictCursor)
        sql_delete = "delete from mazle_user where customer_uuid=%s"
        curs.execute(sql_delete,(payload['id'],))
        curs.close()
        con.commit()
        con.close()
        return JsonResponse({
            "message" : "Withdrawal user"
        })


@api_view(['PUT'])
@authentication_classes([])
@permission_classes([]) 
@csrf_exempt
def update(request) :
    if request.method == 'PUT' :
        con = pool.get_connection()
        curs = con.cursor()
        token = request.COOKIES.get('token')
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        nickname = request.POST.get("nickname")
        birth = request.POST.get("birth")
        profile = base64.encodebytes(request.FILES["profile"].read())
        sql_update = "update mazle_user set nickname=%s, birth=%s, profile=%s where customer_uuid=%s"
        curs.execute(sql_update,(nickname,birth,profile,payload['id']))
        con.commit()
        curs.close()
        con.close()

        return Response({"message": "Update user"}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([])
@permission_classes([]) 
def update_password(request) :
    if request.method == 'PUT' :
        con = pool.get_connection()
        curs = con.cursor()
        passwd = request.POST.get("passwd")
        token = request.COOKIES.get("token")
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        # SQL문 사용
        sql_update = "update mazle_user set passwd=%s where customer_uuid=%s"
        curs.execute(sql_update,(PasswordHasher().hash(passwd),payload['id']))
        con.commit()
        curs.close()
        con.close()

        return Response({"message": "Update user"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([]) 
def mypage(request) :
    if request.method == 'GET' :
        con = pool.get_connection()
        curs = con.cursor()
        token = request.COOKIES.get("token")
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        sql_update = "select nickname, birth, profile, email, platform from mazle_user where customer_uuid=%s"
        curs.execute(sql_update,(payload['id'],))
        rows = curs.fetchall()
        oo = base64.decodebytes(rows[0][2]).decode('latin_1')
        curs.close()
        con.close()
        data = {
            "nickname" : rows[0][0],
            "birth" : rows[0][1],
            "profile" : oo,
            "email" : rows[0][3],
            "platform" : rows[0][4],
        }
        # SQL에 저장된 파일 읽을 때
        # f = open("imageToSave.png",'wb')
        # f.write(oo.encode('latin_1'))
        # f.close()
        return JsonResponse({'data' : data})
