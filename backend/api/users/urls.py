from rest_framework import routers

from api.users.views import UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
urlpatterns = router.urls
