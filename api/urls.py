from django.urls import path, include
from rest_framework_nested import routers
from users.views import UserViewSet,MeViewSet

router = routers.SimpleRouter()

router.register('profile',UserViewSet,basename='super-user')
router.register('me',MeViewSet,basename='me')

urlpatterns = [
    path('',include(router.urls))
]
