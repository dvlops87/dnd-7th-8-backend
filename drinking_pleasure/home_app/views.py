from rest_framework.permissions import AllowAny
from util.db_conn import db_conn
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
from rest_framework.views import APIView
import base64

@db_conn
def sql_cursor(sql,  cursor=None):
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows


@permission_classes([AllowAny]) 
class RecipeType(APIView):
    def get(self,request):
        # SQL문 사용
        sql_select = "select (recipe.diff_score+recipe.price_score+recipe.sweet_score)/3 as total_score, recipe.recipe_id, recipe.recipe_name, recipe.img \
        from recipe \
        order by rand() \
        limit 5;"
        rows = sql_cursor(sql_select)[1]
        data_list = []
        for row in rows:
            data = dict()
            data["recipe_id"] = row['recipe_id']
            data["recipe_name"] = row['recipe_name']
            data["total_score"] = row['total_score']
            if row["img"] is None or len(row["img"]) == 0:
                data["img"] = "Not Exist"
            else:
                data["img"] = base64.decodebytes(row['img']).decode('latin_1')
            data_list.append(data)
        return JsonResponse({'data' : data_list})


@permission_classes([AllowAny]) 
class HotRecipe(APIView):
    def get(self,request):
        # SQL문 사용
        sql_select = "call mazle.sp_home_recipe_select(10, @o_out_code);"
        rows = sql_cursor(sql_select)[1]
        data_list = []
        for row in rows:
            data = dict()
            data["recipe_id"] = row['recipe_id']
            data["nickname"] = row['nickname']
            data["recipe_name"] = row['recipe_name']
            if row["img"] is None or len(row["img"]) == 0:
                data["img"] = "Not Exist"
            else:
                data["img"] = base64.decodebytes(row['img']).decode('latin_1')
            data["price"] = row['price']
            data["tag"] = row['tag']
            data["like_cnt"] = row['like_cnt']
            data_list.append(data)
        return JsonResponse({'data' : data_list})


@permission_classes([AllowAny]) 
class HotReview(APIView):
    def get(self,request):
        # SQL문 사용
        sql_select = "select count(drink_comment_like.customer_uuid) as like_cnt, drink_comment_like.comment_id \
            from drink_comment \
            left join drink_comment_like on drink_comment.comment_id = drink_comment_like.comment_id \
            group by drink_comment_like.comment_id \
            limit 10;"
        rows = sql_cursor(sql_select)[1]
        data_list = []
        for row in rows:
            data = dict()
            if row['comment_id'] is None:
                continue
            data["comment_id"] = row['comment_id']
            data["like_cnt"] = row['like_cnt']
            data_list.append(data)
        return JsonResponse({'data' : data_list})

