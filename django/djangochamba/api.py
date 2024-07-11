from rest_framework import routers
from djangochamba.user import views as user_views

router = routers.DefaultRouter()
router.register(r"user", user_views.UserViewSet)
