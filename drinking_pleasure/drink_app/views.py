from rest_framework.decorators import   authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.exceptions import AuthenticationFailed
import base64
import pymysql
import jwt
from django.conf import settings

JWT_SECRET_KEY = getattr(settings, 'SIMPLE_JWT', None)['SIGNING_KEY']
DBCONFIG = getattr(settings, 'DBCONFIG', None)

@authentication_classes([])
@permission_classes([]) 
class DrinkGet(APIView):
    def get(self,request):
        conn = pymysql.connect(host='database-1.cvip8q7p6e3c.ap-northeast-2.rds.amazonaws.com', 
                        user='admin1234', passwd='admin1234', db='test', charset='utf8')
        drink_id = request.GET['drink_id']
        token = request.COOKIES.get('token')
        if not token :
            return HttpResponse("User doesn't have token", status=status.HTTP_200_OK)
        try :
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('UnAuthenticated!')
        # SQL문 사용
        curs = conn.cursor(pymysql.cursors.DictCursor)
        sql_delete = "call sp_drink_select(%s,%s)"
        curs.execute(sql_delete,(drink_id,payload['id']))
        conn.close()