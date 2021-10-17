from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .apps import SetimentAnalisisCoronaConfig


class ModelView(APIView):
    def post(self, request):
        if request.method == "POST":
            try:
                pred = SetimentAnalisisCoronaConfig.model.analyst(request.data["words"])
                response = {"predicted": pred}
                return JsonResponse(response)
            except:
                return JsonResponse({"message": "Only POST allowed with 'words' argument"})
        return JsonResponse({"message": "Only POST allowed"})
