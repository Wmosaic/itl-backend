from djangochamba.professor import Professor
from djangochamba.student   import Student
from djangochamba.classroom import Classroom
from djangochamba.user      import User
from rest_framework.authentication import get_authorization_header
from rest_framework import permissions
from utils import jwt_decode

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token = str(get_authorization_header(request))
            token = token.split()[1].replace('','')
            if token != "":
                try:
                    payload = jwt_decode(token)
                    user = User.objects.filter(email = payload['email'])
                    if user.exist():
                        user = user.get()
                        if user.is_superuser or user.is_staff or user.user_type == User.USER_ADMIN:
                            return user.is_active
                except Exception as error:
                    print(error)
                    return False
        except Exception as error:
            print(error)
            return False
        
    def has_object_permission(self, request, view, obj):
        return False
        
class IsProfessor(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            token = str(get_authorization_header(request))
            token = token.split()[1].replace('','')
            if token != "":
                try:
                    payload = jwt_decode(token)
                    user = User.objects.filter(email = payload['email'])
                    if user.exist():
                        user = user.get()
                        if user.user_type == User.USER_PROFESSOR:
                            return user.is_active
                except Exception as error:
                    print(error)
                    return False
        except Exception as error:
            print(error)
            return False
        
    def has_object_permission(self, request, view, obj):
        return False
        
class IsStudent(permissions.BasePermission, ):
    def has_permission(self, request, view):
        try:
            token = str(get_authorization_header(request))
            token = token.split()[1].replace('','')
            if token != "":
                try:
                    payload = jwt_decode(token)
                    user = User.objects.filter(email = payload['email'])
                    if user.exist():
                        user = user.get()
                        if user.user_type == User.USER_STUDENT:
                            return user.is_active
                except Exception as error:
                    print(error)
                    return False
        except Exception as error:
            print(error)
            return False
        
    def has_object_permission(self, request, view, obj):
        return False
