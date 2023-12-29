from rest_framework.routers import DefaultRouter

from . import views


app_name = 'viber_filter'
router = DefaultRouter()
router.register(r'', views.ViberMessage, basename='viber_messages')
router.register(r'main', views.MainService, basename='main_service')

urlpatterns = router.urls
