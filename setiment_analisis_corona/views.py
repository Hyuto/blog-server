from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from .apps import SetimentAnalisisCoronaConfig


class ModelView(APIView):
    def post(self, request):
        if request.method == "POST":
            pred = SetimentAnalisisCoronaConfig.model.analyst(request.data["words"])
            response = {"predicted": pred}
            return JsonResponse(response)
