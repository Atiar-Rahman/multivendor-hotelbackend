from django.urls import path, include
from rest_framework_nested import routers
from users.views import UserViewSet,MeViewSet,RoleUpdate
from hotels.views import VendorViewSet,VendorApproveViewSet,ContactViewSet

router = routers.SimpleRouter()

router.register(r'profile',UserViewSet,basename='super-user')
router.register(r'me',MeViewSet,basename='me')
router.register(r'rolechange',RoleUpdate,basename='role-change')
router.register(r'vendors', VendorViewSet, basename='vendor')
router.register(r'contacts',ContactViewSet, basename='contact')

vendor_nested = routers.NestedSimpleRouter(router,'vendors', lookup='vendor')
vendor_nested.register('approved', VendorApproveViewSet,basename='approved')

urlpatterns = [
    path('',include(router.urls)),
    path('',include(vendor_nested.urls)),
]
