import jwt
import base64
from django.conf import settings
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

import recipe_app.call_sp as call_sp


JWT_SECRET_KEY = getattr(settings, 'SIMPLE_JWT', None)['SIGNING_KEY']


class RecipeView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        try:
            offset = request.GET.get('offset', 0)
            limit = request.GET.get('limit', 10)
            search_keyword = request.GET.get('search_keyword', None)
            is_order = request.GET.get('is_order', None)
        except KeyError:
            offset = 0
            limit = 10
            search_keyword = None
            is_order = None

        sp_args = {
            'offset': offset,
            'limit': limit,
            'search_keyword': search_keyword,
            'order': is_order
        }
        is_suc, data = call_sp.call_sp_recipe_list_select(sp_args)
        if is_suc:
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)       


class RecipeDetailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk):
        try:
            token = request.COOKIES.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            customer_uuid = None

        sp_args = {
            'recipe_id': pk,
            'customer_uuid': customer_uuid,
        }
        is_suc, data = call_sp.call_sp_recipe_select(sp_args)
        if is_suc:
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            token = request.COOKIES.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            recipe_name = request.POST.get('recipe_name')
            summary = request.POST.get('summary')
            description = request.POST.get('description')
            img = request.POST.get('img')
            price = request.POST.get('price')
            mesaure_standard = request.POST.get('mesaure_standard')
            tip = request.POST.get('tip')
            diff_score = request.POST.get('diff_score')
            price_score = request.POST.get('price_score')
            sweet_score = request.POST.get('sweet_score')
            alcohol_score = request.POST.get('alcohol_score')
            main_meterial = request.POST.get('main_meterial')
            sub_meterial = request.POST.get('sub_meterial')

            main_meterial_list = main_meterial.split(',')
            sub_meterial_list = sub_meterial.split(',')
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        sp_args = {
            'customer_uuid': customer_uuid,
            'recipe_name': recipe_name,
            'summary': summary,
            'description': description,
            'img':  base64.decodebytes(img).decode('latin_1'),
            'price': price,
            'mesaure_standard': mesaure_standard,
            'tip': tip,
            'diff_score': diff_score,
            'price_score': price_score,
            'sweet_score': sweet_score,
            'alcohol_score': alcohol_score,
            'main_meterial': main_meterial_list,
            'sub_meterial': sub_meterial_list,
        }
        is_suc, _ = call_sp.call_sp_recipe_set(sp_args)

        if is_suc:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            token = request.COOKIES.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        sp_args = {
            'customer_uuid': customer_uuid,
            'recipe_id': pk,
        }
        is_suc, _ = call_sp.call_sp_recipe_delete(sp_args)
        if is_suc:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecipeReviewView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk):
        try:
            offset = request.GET.get('offset')
            limit = request.GET.get('limit')
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        sp_args = {
            'recipe_id': pk,
            'offset': offset,
            'limit': limit,
        }
        is_suc, data = call_sp.call_sp_recipe_review_select(sp_args)
        if is_suc:
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, pk):
        try:
            token = request.COOKIES.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:
            comment = request.POST.get('comment')
            score = request.POST.get('score')
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        sp_args = {
            'customer_uuid': customer_uuid,
            'recipe_id': pk,
            'comment': comment,
            'score': score,
        }
        is_suc, _ = call_sp.call_sp_recipe_review_set(sp_args)

        if is_suc:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RecipeLikeView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, recipe_id):
        '''
        유저가 해당 recipe_id에 좋아요 했는지 여부
        '''
        try:
            token = request.COOKIES.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        sp_args = {
            'customer_uuid': customer_uuid,
            'recipe_id': recipe_id,
        }
        is_suc, data = call_sp.call_sp_recipe_like_select(sp_args)

        if is_suc:
            return Response(status=status.HTTP_200_OK, data=data)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, recipe_id):
        try:
            token = request.COOKIES.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        sp_args = {
            'customer_uuid': customer_uuid,
            'recipe_id': recipe_id,
        }
        is_suc, _ = call_sp.call_sp_recipe_like_set(sp_args)

        if is_suc:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, recipe_id):
        try:
            token = request.COOKIES.get('token')
            user = jwt.decode(token, JWT_SECRET_KEY, algorithms='HS256')

            customer_uuid = user['id']
        except Exception:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        sp_args = {
            'customer_uuid': customer_uuid,
            'recipe_id': recipe_id,
        }
        is_suc, _ = call_sp.call_sp_recipe_like_delete(sp_args)

        if is_suc:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
