import datetime

import jwt
from django.contrib.auth.hashers import make_password, check_password
from django.db import IntegrityError
from .models import Login

# Create your views here.
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # Check if the username exists
        existing_user = Login.objects.filter(username=username).first()

        if existing_user:
            # If the user exists, perform login check
            if check_password(password, existing_user.password):
                # Generate JWT token
                jwt_payload = {
                    'user_id': existing_user.username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
                }
                jwt_token = jwt.encode(jwt_payload, 'your_secret_key', algorithm='HS256')

                return JsonResponse({"message": "Login successful", "token": jwt_token})
            else:
                return JsonResponse({"message": "Invalid password"}, status=401)
        else:
            return JsonResponse({"message": "User not found"}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def get(self, request, username=None):
        if username:
            user = get_object_or_404(Login, username=username)
            return JsonResponse({"username": user.username, "password": user.password})
        else:
            users = Login.objects.all()
            return JsonResponse([user.username for user in users], safe=False)

    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # Check if the username already exists
        existing_user = Login.objects.filter(username=username).first()

        if existing_user:
            return JsonResponse({"message": "Username already exists"}, status=400)
        else:
            # Create a new account
            hashed_password = make_password(password)
            new_user = Login(username=username, password=hashed_password)
            new_user.save()
            return JsonResponse({"message": "Account created successfully"})

    def put(self, request, username):
        user = get_object_or_404(Login, username=username)
        data = json.loads(request.body)
        for key, value in data.items():
            setattr(user, key, value)
        user.save()
        return JsonResponse({"message": "User updated successfully"})

    def delete(self, request, username):
        user = get_object_or_404(Login, username=username)
        user.delete()
        return JsonResponse({"message": "User deleted successfully"})
