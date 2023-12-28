from rest_framework.routers import DefaultRouter

from . import views


app_name = 'viber_filter'
router = DefaultRouter()
router.register(r'', views.ViberMessage, basename='viber_messages')
urlpatterns = router.urls
