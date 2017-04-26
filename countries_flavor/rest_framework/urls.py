from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter(trailing_slash=False)
router.register(r'countries', views.CountryViewSet)

urlpatterns = router.urls
