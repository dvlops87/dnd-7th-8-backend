from codecs import utf_16_be_decode, utf_16_be_encode
import tempfile
from django.http import JsonResponse
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from argon2 import PasswordHasher
import base64
import jwt
from datetime import datetime,timedelta
from .password_validcheck import password_validcheck
import uuid

JWT_SECRET_KEY = getattr(settings, 'SIMPLE_JWT', None)['SIGNING_KEY']

from util.db_conn import db_conn
@db_conn
def sql_cursor(sql, sql_args, cursor=None):
    cursor.execute(sql, sql_args)
    rows = cursor.fetchall()
    return rows

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
        sql_duplicate = "SELECT * FROM mazle_user WHERE email = %s limit 1;"
        rows = sql_cursor(sql_duplicate,search_email)[1]
        if rows:
            return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)
        else:
            sql_create = "insert into mazle_user (customer_uuid, email,passwd) values (%s,%s,%s)"
            sql_cursor(sql_create,(user_uuid,search_email,PasswordHasher().hash(passwd),))
            sql_select = "SELECT customer_uuid FROM mazle_user WHERE email = %s limit 1;"
            
            rows = sql_cursor(sql_select,(search_email,))[1][0]
            payload = {
                'id': rows['customer_uuid'],
                'exp': datetime.utcnow() + timedelta(hours=1)
            }
            token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')
            return Response({"token": token}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login(request):
    if request.method == 'POST':
        search_email = request.POST.get("email")
        password = request.POST.get("passwd")
        # SQL문 사용
        sql = "select email, passwd, customer_uuid from mazle_user where email=%s limit 1"
        
        rows = sql_cursor(sql,(search_email,))[1]
        if len(rows) == 0:
            raise AuthenticationFailed('User not found!') 
        try:
            PasswordHasher().verify(rows[0]['passwd'], password)
        except:
            raise AuthenticationFailed('Incorrect password!') 
        
        payload = {
            'id': rows[0]['customer_uuid'],
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        token = jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256').decode('utf-8')

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
        token = request.headers.get('token')
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_200_OK)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        # SQL문 사용
        sql_delete = "delete from mazle_user where customer_uuid=%s"
        sql_cursor(sql_delete,(payload['id'],))
        response = JsonResponse({
            "message" : "Withdrawal user"
        })
        response.delete_cookie('token')
        return response

@api_view(['PUT'])
@authentication_classes([])
@permission_classes([]) 
@csrf_exempt
def update(request) :
    if request.method == 'PUT' :
        token = request.headers.get('token')
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_200_OK)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        nickname = request.POST.get("nickname")
        birth = request.POST.get("birth")
        profile = base64.encodebytes(request.FILES["profile"].read())
        sql_update = "update mazle_user set nickname=%s, birth=%s, profile=%s where customer_uuid=%s"
        sql_cursor(sql_update,(nickname,birth,profile,payload['id']))
        return Response({"message": "Update user"}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@authentication_classes([])
@permission_classes([]) 
def update_password(request) :
    if request.method == 'PUT' :
        passwd = request.POST.get("passwd")
        token = request.COOKIES.get("token")
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_200_OK)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        # SQL문 사용
        sql_update = "update mazle_user set passwd=%s where customer_uuid=%s"
        sql_cursor(sql_update,(PasswordHasher().hash(passwd),payload['id']))
        return Response({"message": "Update user"}, status=status.HTTP_200_OK)

        
@authentication_classes([])
@permission_classes([]) 
class MyPageProfile(APIView):
    def get(self,request):
        token = request.COOKIES.get("token")
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_200_OK)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        sql_update = "select nickname, birth, profile, email, platform from mazle_user where customer_uuid=%s"
        rows = sql_cursor(sql_update,(payload['id'],))[1][0]
        if rows['profile'] is None:
            oo = "Not Exist"
        else:
            oo = base64.decodebytes(rows['profile']).decode('latin_1')
        data = {
            "nickname" : rows['nickname'],
            "birth" : rows['birth'],
            "profile" : oo,
            "email" : rows['email'],
            "platform" : rows['platform'],
        }
        # SQL에 저장된 파일 읽을 때
        # f = open("imageToSave.png",'wb')
        # f.write(oo.encode('latin_1'))
        # f.close()
        return JsonResponse({'data' : data})

        
@authentication_classes([])
@permission_classes([]) 
class MyPageReview(APIView):
    def get(self,request):
        token = request.COOKIES.get("token")
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_200_OK)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        sql_drink = "select * from drink_comment where customer_uuid=%s"
        rows_drink = sql_cursor(sql_drink,(payload['id'],))[1]
        sql_recipe = "select * from recipe_comment where customer_uuid=%s"
        rows_recipe = sql_cursor(sql_recipe,(payload['id'],))[1]
        data_recipe_list = []
        data_drink_list = []
        if len(rows_drink) != 0:
            for row in rows_drink:
                data_drink = {}
                data_drink["comment_id"] = row["comment_id"]
                data_drink["drink_id"] = row["drink_id"]
                data_drink["comment"] = row["comment"]
                data_drink["score"] = row["score"]
                data_drink_list.append(data_drink)
        else:
            data_drink_list.append("Not Exist Drink Comment")
        if len(rows_recipe) != 0:
            for row in rows_recipe:
                data_recipe = {}
                data_recipe["comment_id"] = row["comment_id"]
                data_recipe["recipe_id"] = row["recipe_id"]
                data_recipe["comment"] = row["comment"]
                data_recipe["score"] = row["score"]
                data_recipe_list.append(data_recipe)
        else:
            data_recipe_list.append("Not Exist Recipe Comment")
        return JsonResponse({'drink_comment' : data_drink_list, 'recipe_comment':data_recipe_list})

        
@authentication_classes([])
@permission_classes([]) 
class MyPageRecipe(APIView):
    def get(self,request):
        token = request.COOKIES.get("token")
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_200_OK)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        sql_update = "select * from recipe where customer_uuid=%s"
        rows = sql_cursor(sql_update,(payload['id'],))[1]
        if len(rows) == 0:
            return Response({"message": "Not Exist Recipe"}, status=status.HTTP_404_NOT_FOUND)
        else:
            data_list = []
            for row in rows:
                data = {}
                data["recipe_id"] = row["recipe_id"]
                data["recipe_name"] = row["recipe_name"]
                data["summary"] = row["summary"]
                data["description"] = row["description"]
                data["img"] = base64.decodebytes(row["img"]).decode('latin_1')
                data["price"] = row["price"]
                data["measure_standard"] = row["measure_standard"]
                data["tip"] = row["tip"]
                data["diff_score"] = row["diff_score"]
                data["price_score"] = row["price_score"]
                data["sweet_score"] = row["sweet_score"]
                data["alcohol_score"] = row["alcohol_score"]
                data_list.append(data)
            return JsonResponse({'data' : data_list})
