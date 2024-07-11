from django.shortcuts import render
from rest_framework import viewsets
from djangochamba.user.models import User,UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset         = User.objects.all()
    serializer_class = UserSerializer

@action(detain=False, methods=["POST"])
