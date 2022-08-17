from pickle import EMPTY_DICT
from rest_framework.decorators import   authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
import base64
import jwt
from django.conf import settings
from mysql.connector import pooling
import uuid
from rest_framework.permissions import AllowAny

JWT_SECRET_KEY = getattr(settings, 'SIMPLE_JWT', None)['SIGNING_KEY']
dbconfig = getattr(settings, 'DBCONFIG', None)
pool= pooling.MySQLConnectionPool(pool_name = "mypool",pool_size = 20,**dbconfig)

@permission_classes([AllowAny]) 
class DrinkGetList(APIView):
    def get(self,request):
        con = pool.get_connection()
        curs = con.cursor(dictionary=True)
        # SQL문 사용
        sql_delete = "select * from drink"
        curs.execute(sql_delete)
        rows = curs.fetchall()
        curs.close()
        data_list = []
        for row in rows:
            data = dict()
            data["drink_id"] = row['drink_id']
            data["drink_name"] = row['drink_name']
            data["description"] = row['description']
            data["calorie"] = row['calorie']
            data["manufacture"] = row['manufacture']
            data["price"] = row['price']
            data["large_category"] = row['large_category']
            data["medium_category"] = row['medium_category']
            data["small_category"] = row['small_category']
            data["img"] = base64.decodebytes(row['img']).decode('latin_1')
            data["alcohol"] = row['alcohol']
            data["measure"] = row['measure']
            data["caffeine"] = row['caffeine']
            data_list.append(data)
        return JsonResponse({'data' : data_list})



@authentication_classes([])
@permission_classes([]) 
class DrinkDetail(APIView):
    def get(self,request, pk):
        con = pool.get_connection()
        curs = con.cursor(dictionary=True)
        token = request.COOKIES.get('token')
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_403_FORBIDDEN)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        # SQL문 사용
        sql_get = "call sp_drink_select(%s,%s,@o)"
        curs.execute(sql_get,(pk,payload['id']))
        rows = curs.fetchall()
        curs.close()
        data = {
            "drink_name" : rows[0]['drink_name'],
            "description" : rows[0]['description'],
            "calorie" : rows[0]['calorie'],
            "manufacture" : rows[0]['manufacture'],
            "price" : rows[0]['price'],
            "large_category" : rows[0]['large_category'],
            "medium_category" : rows[0]['medium_category'],
            "small_category" : rows[0]['small_category'],
            "img" : base64.decodebytes(rows[0]['img']).decode('latin_1'),
            "alcohol" : rows[0]['alcohol'],
            "measure" : rows[0]['measure'],
            "caffeine" : rows[0]['caffeine'],
            "tag" : rows[0]['tag'],
            "like_cnt" : rows[0]['like_cnt'],
        }
        return JsonResponse({'data' : data})

    def post(self,request):
        con = pool.get_connection()
        curs = con.cursor(dictionary=True)
        drink_name = request.POST.get['drink_name']
        description = request.POST.get['description']
        calorie = request.POST.get['calorie']
        manufacture = request.POST.get['manufacture']
        price = request.POST.get['price']
        large_category = request.POST.get['large_category']
        medium_category = request.POST.get['medium_category']
        small_category = request.POST.get['small_category']
        img = request.FILES['img']
        alcohol = request.POST.get['alcohol']
        measure = request.POST.get['measure']
        caffeine = request.POST.get['caffeine']
        token = request.COOKIES.get('token')
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_403_FORBIDDEN)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:   
            raise AuthenticationFailed('UnAuthenticated!')
        sql_insert = "call sp_drink_set(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,@o_id,@o_code)"
        curs.execute(sql_insert,(drink_name,description,calorie,manufacture,price,large_category,medium_category,small_category,img,alcohol,measure,caffeine))
        curs.close()
        con.commit()
        return Response({"message": "success create comment"}, status=status.HTTP_201_CREATED)


        
@authentication_classes([])
@permission_classes([]) 
class DrinkReview(APIView):
    def get(self,request, pk):
        con = pool.get_connection()
        curs = con.cursor(dictionary=True)
        sql = "call sp_drink_comment_select(%s,@o)"
        curs.execute(sql,(pk,))
        rows = curs.fetchall()
        curs.close()
        data_list = []
        if len(rows) == 0:
            return Response({"message" : "No data in comment"}, status=status.HTTP_404_NOT_FOUND)
        for row in rows:
            data = dict()
            data["nickname"] = row['nickname']
            data["comment"] = row['comment']
            data["score"] = row['score']
            data["like_cnt"] = row['like_cnt']
            data_list.append(data)
        return JsonResponse({'data' : data_list})

    def post(self,request, pk):
        con = pool.get_connection()
        curs = con.cursor(dictionary=True)
        comment = request.GET['comment']
        score = request.GET['score']
        token = request.COOKIES.get('token')
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_200_OK)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:   
            raise AuthenticationFailed('UnAuthenticated!')
        # SQL문 사용
        sql_delete = "insert into drink_comment (drink_id, customer_uuid, comment, score) values (%s,%s,%s,%s)"
        curs.execute(sql_delete,(pk,payload['id'],comment,score))
        curs.close()
        con.commit()
        return Response({"message": "success create comment"}, status=status.HTTP_201_CREATED)


        
@authentication_classes([])
@permission_classes([]) 
class DrinkLike(APIView):
    def post(self,request, pk):
        con = pool.get_connection()
        curs = con.cursor(dictionary=True)
        token = request.COOKIES.get('token')
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_200_OK)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:   
            raise AuthenticationFailed('UnAuthenticated!')
        sql_exist = "select * from drink_like where customer_uuid=%s"
        curs.execute(sql_exist,(payload['id'],))
        rows = curs.fetchall()
        if len(rows) == 0:
            sql_insert = "insert into drink_like (drink_id, customer_uuid) values (%s,%s)"
            curs.execute(sql_insert,(pk,payload['id']))
            curs.close()
            con.commit()
            return Response({"message": "success create like"}, status=status.HTTP_201_CREATED)
        else:
            sql_delete = "delete from drink_like where drink_id=%s and customer_uuid=%s"
            curs.execute(sql_delete,(pk,payload['id']))
            curs.close()
            con.commit()
            return Response({"message": "success delete like"}, status=status.HTTP_200_OK)


