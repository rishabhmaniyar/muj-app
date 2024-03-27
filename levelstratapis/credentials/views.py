from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Credentials
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class UserCredentialsView(View):
    def post(self, request):
        data = json.loads(request.body)
        appName = data.get('app_name')

        # Check if the username exists
        existing_user = Credentials.objects.filter(app_name=appName).first
        if len(Credentials.objects.filter(app_name=appName)) == 0:
            new_credentials = Credentials(**data)
            new_credentials.save()
            return JsonResponse({"message": "Saved new credentials successful"}, status=200)
        else:
            token = data.get('token')
            existing_user.token = token
            existing_user.save()
            return JsonResponse({"message": "Updated Token "}, status=200)
        # else:
        #     return JsonResponse({"message": "User not found"}, status=404)

    def get(self):

        users = Credentials.objects.all()
        return JsonResponse([user.app_name for user in users], safe=False)
