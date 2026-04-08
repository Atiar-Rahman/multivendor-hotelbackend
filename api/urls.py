from django.urls import path, include
from rest_framework_nested import routers
from users.views import UserViewSet,MeViewSet,RoleUpdate

router = routers.SimpleRouter()

router.register('profile',UserViewSet,basename='super-user')
router.register('me',MeViewSet,basename='me')
router.register('rolechange',RoleUpdate,basename='role-change')


urlpatterns = [
    path('',include(router.urls))
]
