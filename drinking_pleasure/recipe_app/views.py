from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from recipe_app import call_sp


class RecipeDetailView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk):
        try:
            user = request.user

            customer_uuid = user.customer_uuid
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
            customer_uuid = request.user.customer_uuid

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
            sub_meterial = request.POST.get('pricsub_meteriale_score')

            main_meterial_list = main_meterial.split(',')
            sub_meterial_list = sub_meterial.split(',')
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        sp_args = {
            'customer_uuid': customer_uuid,
            'recipe_name': recipe_name,
            'summary': summary,
            'description': description,
            'img': img,
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
            user = request.user

            customer_uuid = user.customer_uuid
        except Exception:
            customer_uuid = None

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
            customer_uuid = request.user.customer_uuid

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
