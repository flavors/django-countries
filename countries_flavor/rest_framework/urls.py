from rest_framework.routers import SimpleRouter

from . import views

app_name = 'countries_flavor.rest_framework'
router = SimpleRouter(trailing_slash=False)
router.register(r'countries', views.CountryViewSet)

urlpatterns = router.urls
