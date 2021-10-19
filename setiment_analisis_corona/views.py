from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .apps import SetimentAnalisisCoronaConfig


class ModelView(APIView):
    def post(self, request):
        if request.method == "POST":
            try:
                pred = SetimentAnalisisCoronaConfig.model.analyst(request.data["words"])
                return JsonResponse(pred)
            except:
                return JsonResponse({"message": "Only POST allowed with 'words' argument"})
        return JsonResponse({"message": "Only POST allowed"})
