from django.shortcuts import render
from rest_framework import viewsets
from djangochamba.user.models import User, UserSession
from djangochamba.user.serializer import UserSerializer
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response 
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK,HTTP_409_CONFLICT, HTTP_401_UNAUTHORIZED
from graphql_jwt.shortcuts import get_token
from djangochamba.utils import check_not_empty_params, get_user_json,get_current_user
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class UserViewSet(viewsets.ModelViewSet):
    queryset         = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["POST"], permission_classes = (AllowAny))
    def login(self, request):
        data = request.data

        email = data["email"] if "email" in data and data["email"] != "" else ""
        password = data["password"] if "password" in data and data["password"] != "" else ""

        check = check_not_empty_params({"email":email,"password":password})
        if check != None:
            return check
        
        user = User.objects.filter(email = email, password = password)
        if user.exists():
            user = user.get()
        
            if not check_password(password, user.password):
                content = {"Error":_("Incorrect password")}
                return Response(content, status=HTTP_404_NOT_FOUND)
            else:
                token = get_token(user)
                session = UserSession.objects.create(user = user)
                user.last_login = timezone.now()
                user.save()
                response = get_user_json(user)
        else:
            content = {"Error":_("Incorrect email")}
            return Response(content, status=HTTP_404_NOT_FOUND)
        return Response({"token":token, "data":response})
            