from django.db import IntegrityError
from .models import User

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json


@method_decorator(csrf_exempt, name='dispatch')
class UserView(View):
    def get(self, request, username=None):
        if username:
            user = get_object_or_404(User, username=username)
            return JsonResponse({"username": user.username, "phone": user.phone})
        else:
            users = User.objects.all()
            return JsonResponse([user.username for user in users], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        new_user = User(**data)
        try:
            new_user.save()
            return JsonResponse({"message": "User created successfully"})
        except IntegrityError:
            return JsonResponse({"message": "Username or token already exists"}, status=400)

    def put(self, request, username):
        user = get_object_or_404(User, username=username)
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return JsonResponse({"message": "User updated successfully"})

    def delete(self, request, username):
        user = get_object_or_404(User, username=username)
        user.delete()
        return JsonResponse({"message": "User deleted successfully"})
